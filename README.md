# speak-tts

Voice cloning CLI for Mac (Apple Silicon) using F5-TTS.

## Installation

### Via Homebrew

```bash
brew tap danielsinai/speak-tts
brew install speak-tts
```

### Via pipx

```bash
pipx install speak-tts
```

### Via pip

```bash
pip install speak-tts
```

## Requirements

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.10+

## Usage

### Add a Voice Profile

```bash
speak --add-profile daniel --voice ~/voice.wav --text-file ~/reference.txt
```

The reference audio should be a clear WAV recording (24kHz) of the voice you want to clone, and the text file should contain an exact transcript.

### Generate Speech

Plays audio directly (no file saved):

```bash
speak daniel "Hello, this is a test!"
```

Save to a file:

```bash
speak daniel "Hello world" --output ~/Desktop/hello.wav
```

### List Profiles

```bash
speak --list
```

### Play Audio

```bash
speak --play output.wav
```

## Profile Storage

Profiles stored in `~/.speak/profiles/<name>/` with:
- `reference.wav` - Voice sample
- `reference.txt` - Transcript

## Tips

- **Reference Audio**: 5-15 seconds, 24kHz, minimal background noise
- **Reference Text**: Exact transcript of the audio
- **First Run**: Downloads F5-TTS model (~1GB)

## Development

```bash
git clone https://github.com/danielsinai/homebrew-speak-tts
cd homebrew-speak-tts
python3 -m venv venv
source venv/bin/activate
pip install -e .
speak --help
```

## Releasing a New Version

1. Update version in `pyproject.toml` and `speak_tts/__init__.py`

2. Commit and create a GitHub release:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

3. Get the SHA256 of the release tarball:
   ```bash
   curl -sL https://github.com/danielsinai/homebrew-speak-tts/archive/refs/tags/v0.1.0.tar.gz | shasum -a 256
   ```

4. Update `Formula/speak-tts.rb` with the new version and SHA256

5. (Optional) Also publish to PyPI:
   ```bash
   python -m build
   twine upload dist/*
   ```

## License

MIT
