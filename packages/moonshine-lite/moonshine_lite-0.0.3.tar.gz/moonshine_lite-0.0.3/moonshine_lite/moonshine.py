"""Live captions from microphone using Moonshine and SileroVAD ONNX models."""

import argparse
import logging
import time
import wave
from importlib.resources import files
from pathlib import Path
from queue import Empty, Queue
from threading import Event
from typing import Callable, Optional

import numpy as np
from pynput import keyboard
from pynput.keyboard import Controller, Key, KeyCode
from silero_vad import VADIterator, load_silero_vad
from sounddevice import InputStream
from tokenizers import Tokenizer

TOKENIZER_PATH = str(files("moonshine_lite.data").joinpath("tokenizer.json"))
WAV_PATH = str(files("moonshine_lite.data").joinpath("beckett.wav"))

SAMPLING_RATE = 16000

CHUNK_SIZE = 512  # Silero VAD requirement with sampling rate 16000.
LOOKBACK_CHUNKS = 5
MAX_LINE_LENGTH = 80

# These affect live caption updating - adjust for your platform speed and model.
MAX_SPEECH_SECS = 15
MIN_REFRESH_SECS = 0.2

MAX_SPEECH_BUFFER_SIZE = MAX_SPEECH_SECS * SAMPLING_RATE

# Add this at the module level (before any functions)
caption_cache = []

logger = logging.getLogger(__name__)

DEFAULT_ACTIVATION_KEY = keyboard.Key.cmd  # Default to Command/Windows key


logging.basicConfig(
    level=logging.WARNING,  # Default to WARNING level
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Dictionary mapping string names to keyboard keys
ACTIVATION_KEYS = {
    "cmd": Key.cmd,
    "ctrl": Key.ctrl,
    "shift": Key.shift,
    "alt": Key.alt,
    "space": Key.space,
    "tab": Key.tab,
    "caps_lock": Key.caps_lock,
}


class InvalidWaveFormatError(Exception):
    """Raised when wave file format is invalid."""

    pass


class MoonshineOnnxModel:
    def __init__(self, models_dir=None, model_name=None):
        import onnxruntime

        if models_dir is None and model_name is None:
            raise ValueError("Either models_dir or model_name must be specified")

        if models_dir is None:
            preprocess, encode, uncached_decode, cached_decode = self._load_weights_from_hf_hub(model_name)
        else:
            preprocess, encode, uncached_decode, cached_decode = (
                f"{models_dir}/{x}.onnx" for x in ["preprocess", "encode", "uncached_decode", "cached_decode"]
            )
        self.preprocess = onnxruntime.InferenceSession(preprocess)
        self.encode = onnxruntime.InferenceSession(encode)
        self.uncached_decode = onnxruntime.InferenceSession(uncached_decode)
        self.cached_decode = onnxruntime.InferenceSession(cached_decode)

    def _get_onnx_weights(self, model_name):
        from huggingface_hub import hf_hub_download

        repo = "UsefulSensors/moonshine"

        return (
            hf_hub_download(repo, f"{x}.onnx", subfolder=f"onnx/{model_name}")
            for x in ("preprocess", "encode", "uncached_decode", "cached_decode")
        )

    def _load_weights_from_hf_hub(self, model_name):
        model_name = model_name.split("/")[-1]
        return self._get_onnx_weights(model_name)

    def generate(self, audio, max_len=None):
        "audio has to be a numpy array of shape [1, num_audio_samples]"
        if max_len is None:
            # max 6 tokens per second of audio
            max_len = int((audio.shape[-1] / 16_000) * 6)
        preprocessed = self.preprocess.run([], {"args_0": audio})[0]
        seq_len = [preprocessed.shape[-2]]

        context = self.encode.run([], {"args_0": preprocessed, "args_1": seq_len})[0]
        inputs = [[1]]
        seq_len = [1]

        tokens = [1]
        logits, *cache = self.uncached_decode.run([], {"args_0": inputs, "args_1": context, "args_2": seq_len})
        for i in range(max_len):
            next_token = logits.squeeze().argmax()
            tokens.extend([next_token])
            if next_token == 2:
                break

            seq_len[0] += 1
            inputs = [[next_token]]
            logits, *cache = self.cached_decode.run(
                [],
                {
                    "args_0": inputs,
                    "args_1": context,
                    "args_2": seq_len,
                    **{f"args_{i + 3}": x for i, x in enumerate(cache)},
                },
            )
        return [tokens]


class Transcriber:
    def __init__(self, model_name, rate=16000):
        if rate != SAMPLING_RATE:
            raise ValueError(f"Invalid sampling rate. Expected {SAMPLING_RATE}")
        self.model = MoonshineOnnxModel(model_name=model_name)
        self.rate = rate
        self.tokenizer = Tokenizer.from_file(TOKENIZER_PATH)

        self.inference_secs = 0
        self.number_inferences = 0
        self.speech_secs = 0
        self.__call__(np.zeros(int(rate), dtype=np.float32))  # Warmup.

    def __call__(self, speech: np.ndarray) -> str:
        """Returns string containing Moonshine transcription of speech."""
        self.number_inferences += 1
        self.speech_secs += len(speech) / self.rate
        start_time = time.time()

        tokens = self.model.generate(speech[np.newaxis, :].astype(np.float32))
        text = self.tokenizer.decode_batch(tokens)[0]

        self.inference_secs += time.time() - start_time
        return text

    def generate(self, audio: np.ndarray, max_len: Optional[int] = None) -> list[list[int]]:
        "audio has to be a numpy array of shape [1, num_audio_samples]"
        if max_len is None:
            # max 6 tokens per second of audio
            max_len = int((audio.shape[-1] / 16_000) * 6)
        preprocessed = self.model.preprocess.run([], dict(args_0=audio))[0]
        seq_len = [preprocessed.shape[-2]]

        context = self.model.encode.run([], dict(args_0=preprocessed, args_1=seq_len))[0]
        inputs = [[1]]
        seq_len = [1]

        tokens = [1]
        logits, *cache = self.model.uncached_decode.run([], dict(args_0=inputs, args_1=context, args_2=seq_len))
        for i in range(max_len):
            next_token = logits.squeeze().argmax()
            tokens.extend([next_token])
            if next_token == 2:
                break

            seq_len[0] += 1
            inputs = [[next_token]]
            logits, *cache = self.model.cached_decode.run(
                [],
                dict(
                    args_0=inputs,
                    args_1=context,
                    args_2=seq_len,
                    **{f"args_{i + 3}": x for i, x in enumerate(cache)},
                ),
            )
        return [tokens]


class Moonshine:
    """Simple wrapper for Moonshine transcription functionality.

    Examples:
        >>> moonshine = Moonshine(model_name="moonshine/base")
        >>> text = moonshine.transcribe("audio.wav")
        >>> print(text)

        # Or for live transcription:
        >>> moonshine.listen(lambda text: print(text))
    """

    def __init__(self, model_name: str = "moonshine/base", activation_key=DEFAULT_ACTIVATION_KEY):
        """Initialize Moonshine with specified model.

        Args:
            model_name: Name of the model to use. Either "moonshine/base" or "moonshine/tiny"
            activation_key: Key that needs to be held to activate listening (default: Command/Windows key)
        """
        try:
            self.transcriber = Transcriber(model_name=model_name, rate=SAMPLING_RATE)
            self.vad_model = load_silero_vad(onnx=True)
            self.keyboard = Controller()
            self.activation_key = activation_key
            self.is_active = Event()
            self.recording = False
            self.audio_queue = Queue()  # Queue for audio chunks
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Moonshine: {e!s}")

    def _on_key_press(self, key):
        """Handle key press events"""
        if key == self.activation_key:
            logger.info("Activation key pressed - activating listening!")
            self.is_active.set()
            self.recording = False
            logger.debug("Listening activated")

    def _on_key_release(self, key):
        """Handle key release events"""
        if key == self.activation_key:
            logger.info("Activation key released - deactivating listening!")
            self.is_active.clear()
            self.recording = False
            logger.debug("Listening deactivated")
            return  # Stop processing audio when key is released

    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream"""
        if status:
            logger.error(f"Error during audio capture: {status}")
        # Only queue audio data if activation key is pressed
        if self.is_active.is_set():
            self.audio_queue.put((indata.copy().flatten(), status))

    def transcribe(self, path_to_wav: str | Path) -> str:
        """Transcribe audio from a WAV file.

        Args:
            path_to_wav: Path to WAV file to transcribe

        Returns:
            str: Transcribed text
        """
        with wave.open(str(path_to_wav)) as f:
            params = f.getparams()
            if not (params.nchannels == 1 and params.framerate == SAMPLING_RATE and params.sampwidth == 2):
                raise InvalidWaveFormatError(f"Wave file must have 1 channel, {SAMPLING_RATE}Hz, and int16 format")  # noqa: TRY003
            audio = f.readframes(params.nframes)

        # Convert to float32 in range [-1, 1]
        audio = np.frombuffer(audio, np.int16) / 32768.0
        audio = audio.astype(np.float32)[None, ...]

        tokens = self.transcriber.model.generate(audio)
        text = self.transcriber.tokenizer.decode_batch(tokens)
        if text:
            return text[0]
        return ""

    def listen(self, callback: Optional[Callable[[str], None]] = None) -> None:  # noqa: C901
        """Start listening and transcribing from microphone when activation key is pressed."""
        if callback is None:
            callback = self.type

        stream = InputStream(
            samplerate=SAMPLING_RATE,
            channels=1,
            blocksize=CHUNK_SIZE,
            dtype=np.float32,
            callback=self._audio_callback,
        )

        # Set up keyboard listener
        logger.info(f"Initializing keyboard listener for activation key: {self.activation_key}")
        key_listener = keyboard.Listener(on_press=self._on_key_press, on_release=self._on_key_release)
        key_listener.start()
        logger.info("Keyboard listener started")

        vad_iterator = VADIterator(
            model=self.vad_model,
            sampling_rate=SAMPLING_RATE,
            threshold=0.5,
            min_silence_duration_ms=300,
        )

        speech = np.empty(0, dtype=np.float32)
        lookback_size = LOOKBACK_CHUNKS * CHUNK_SIZE

        stream.start()

        with stream:
            try:
                while True:
                    # Check if activation key is pressed
                    if not self.is_active.is_set():
                        continue  # Skip processing if key is not pressed

                    # Try to get audio from the queue
                    try:
                        chunk, status = self.audio_queue.get(timeout=0.1)
                    except Empty:
                        continue

                    if status:
                        logger.error(f"Error during transcription: {status}")

                    speech = np.concatenate((speech, chunk))
                    if not self.recording:
                        speech = speech[-lookback_size:]

                    if len(speech) > MAX_SPEECH_BUFFER_SIZE:
                        speech = speech[-MAX_SPEECH_BUFFER_SIZE:]

                    speech_dict = vad_iterator(chunk)
                    if speech_dict:
                        if "start" in speech_dict and not self.recording:
                            self.recording = True

                        if "end" in speech_dict and self.recording:
                            self.recording = False
                            text = self.transcriber(speech)
                            callback(text)
                            speech = np.empty(0, dtype=np.float32)

                    elif self.recording:
                        if (len(speech) / SAMPLING_RATE) > MAX_SPEECH_SECS:
                            self.recording = False
                            text = self.transcriber(speech)
                            callback(text)
                            speech = np.empty(0, dtype=np.float32)
                            soft_reset(vad_iterator)

            except KeyboardInterrupt:
                pass
            finally:
                key_listener.stop()
                stream.stop()
                stream.close()

    def type(self, text: str) -> None:
        self.keyboard.type(text)


def create_input_callback(q):
    """Callback method for sounddevice InputStream."""

    def input_callback(data, frames, time, status):
        if status:
            logger.error(f"Error during transcription: {status}")
        q.put((data.copy().flatten(), status))

    return input_callback


def soft_reset(vad_iterator):
    """Soft resets Silero VADIterator without affecting VAD model state."""
    vad_iterator.triggered = False
    vad_iterator.temp_end = 0
    vad_iterator.current_sample = 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Moonshine Speech Recognition")
    parser.add_argument(
        "--activation-key",
        choices=list(ACTIVATION_KEYS.keys()),
        default="cmd",
        help="Key to hold down to activate listening (default: cmd)",
    )
    parser.add_argument("--custom-key", help="Custom single-character key to use for activation (e.g., 'a', '1', etc.)")
    parser.add_argument("--transcribe", help="Path to WAV file to transcribe instead of using microphone")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging output")

    args = parser.parse_args()

    # Set logging level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.info("Verbose logging enabled")

    # Determine activation key
    activation_key = KeyCode.from_char(args.custom_key) if args.custom_key else ACTIVATION_KEYS[args.activation_key]

    moonshine = Moonshine(activation_key=activation_key)

    if args.transcribe:
        print(moonshine.transcribe(args.transcribe))
    else:
        print(f"Press and hold {args.custom_key or args.activation_key} to activate listening")
        print("Press Ctrl+C to quit live captions.\n")
        moonshine.listen()
