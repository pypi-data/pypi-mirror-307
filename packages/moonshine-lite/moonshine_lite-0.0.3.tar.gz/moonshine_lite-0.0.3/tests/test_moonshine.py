import numpy as np
import pytest

from moonshine_lite.moonshine import WAV_PATH, Moonshine, caption_cache, end_recording


@pytest.fixture
def moonshine():
    return Moonshine(model_name="moonshine/base")


@pytest.fixture
def sample_audio():
    # Create 1 second of silence
    return np.zeros(16000, dtype=np.float32)


def test_moonshine_initialization(moonshine):
    assert moonshine.transcriber is not None
    assert moonshine.vad_model is not None


def test_end_recording(moonshine, sample_audio, capsys):
    # Clear caption cache
    caption_cache.clear()

    # Test without printing
    end_recording(sample_audio, moonshine, do_print=False)
    assert len(caption_cache) == 1

    # Test with printing
    end_recording(sample_audio, moonshine, do_print=True)
    captured = capsys.readouterr()
    assert len(captured.out) > 0
    assert len(caption_cache) == 2


def test_transcribe(moonshine, sample_audio):
    text = moonshine.transcribe(WAV_PATH)
    print(text)
    assert text == "Ever tried ever failed, no matter try again fail again fail better."


if __name__ == "__main__":
    # run pytest with capture output
    pytest.main(["-s"])
