import argparse
import logging
import sys
from pathlib import Path

from moonshine_lite.moonshine import Moonshine, caption_cache

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the moonshine CLI."""
    parser = argparse.ArgumentParser(
        prog="moonshine",
        description="Moonshine speech-to-text transcription tool",
    )

    parser.add_argument(
        "--model",
        help="Model to use for transcription",
        default="moonshine/base",
        choices=["moonshine/base", "moonshine/tiny"],
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Transcribe command
    transcribe_parser = subparsers.add_parser("transcribe", help="Transcribe an audio file")
    transcribe_parser.add_argument("file", type=Path, help="Path to WAV file to transcribe")

    # Listen command
    listen_parser = subparsers.add_parser("listen", help="Start live transcription from microphone")

    args = parser.parse_args()

    try:
        logger.info(f"Loading Moonshine model '{args.model}' (using ONNX runtime) ...")
        moonshine = Moonshine(model_name=args.model)

        if args.command == "transcribe":
            if not args.file.exists():
                logger.error(f"File not found: {args.file}")
                sys.exit(1)
            text = moonshine.transcribe(args.file)
            print(text)

        elif args.command == "listen":
            print("Press Ctrl+C to quit live transcription.\n")
            try:
                moonshine.listen()
            except KeyboardInterrupt:
                print(f"""

                 model_name :  {args.model}
           number inferences :  {moonshine.transcriber.number_inferences}
        mean inference time :  {(moonshine.transcriber.inference_secs / moonshine.transcriber.number_inferences):.2f}s
        model realtime factor :  {(moonshine.transcriber.speech_secs / moonshine.transcriber.inference_secs):0.2f}x
                """)
                if caption_cache:
                    print(f"Cached captions.\n{' '.join(caption_cache)}")
        else:
            parser.print_help()
            sys.exit(1)

    except Exception:
        logger.exception("Error running Moonshine")
        sys.exit(1)


if __name__ == "__main__":
    main()
