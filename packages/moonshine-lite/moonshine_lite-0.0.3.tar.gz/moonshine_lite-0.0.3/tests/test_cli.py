import pytest

from moonshine_lite.cli import main
from moonshine_lite.moonshine import WAV_PATH


def test_transcribe_command(capsys, monkeypatch):
    # Mock sys.argv
    test_args = ["moonshine", "transcribe", WAV_PATH]
    monkeypatch.setattr("sys.argv", test_args)

    # Run CLI
    main()

    # Check output
    captured = capsys.readouterr()
    assert "ever failed" in captured.out.lower()


def test_transcribe_nonexistent_file(capsys, monkeypatch):
    # Mock sys.argv with non-existent file
    test_args = ["moonshine", "transcribe", "nonexistent.wav"]
    monkeypatch.setattr("sys.argv", test_args)

    # Run CLI and expect system exit
    with pytest.raises(SystemExit):
        main()

    # Check error message
    captured = capsys.readouterr()
    assert "file not found" in captured.err.lower()
