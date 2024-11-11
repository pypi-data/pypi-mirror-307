# PodGrab

A command-line tool for downloading podcast episodes and generating transcriptions using OpenAI's Whisper model.

## Features

- 🔍 Search podcasts using the iTunes Search API
- ⬇️ Download individual podcast episodes
- 🎯 Interactive episode selection for ambiguous matches
- 📝 Transcribe audio files using OpenAI's Whisper model
- 📊 Progress bar for downloads
- 📋 Support for different Whisper model sizes (tiny to large)
- 🔄 Non-interactive mode for automation

## Installation

### From PyPI (Recommended)
```bash
pip install podgrab
```

### From Source (For Development)
1. Make sure you have Python 3.11 or later installed
2. Install Poetry if you haven't already:
   ```bash
   pip install poetry
   ```
3. Clone this repository and install dependencies:
   ```bash
   git clone https://github.com/username/podgrab.git
   cd podgrab
   poetry install
   ```

## Usage

### Downloading Podcasts

Basic usage to download a podcast episode:
```bash
podgrab download "Podcast Name" "Episode Title"
```

Options:
- `--output`/`-o`: Specify output directory (default: current directory)
- `--non-interactive`: Run without interactive prompts
- `--verbose`/`-v`: Enable verbose output
- `--quiet`/`-q`: Suppress non-error messages

Example:
```bash
podgrab download "The Daily" "Today's Episode" -o ~/Downloads
```

### Transcribing Audio

Transcribe a downloaded podcast episode:
```bash
podgrab transcribe path/to/audio/file.mp3
```

Options:
- `--model`/`-m`: Specify Whisper model size (tiny, base, small, medium, large)
- `--output`/`-o`: Save transcription to file (default: print to console)

Example:
```bash
podgrab transcribe podcast.mp3 -m medium -o transcript.txt
```

## Requirements

- Python 3.11+
- Required Python packages (automatically installed):
  - typer
  - requests
  - feedparser
  - rich
  - tqdm
  - openai-whisper
  - torch
  - torchvision
  - torchaudio

## Development

1. Set up the development environment:
   ```bash
   poetry install
   ```

2. Run tests:
   ```bash
   poetry run pytest
   ```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Add or update tests as needed
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Uses the [OpenAI Whisper](https://github.com/openai/whisper) model for transcription
- Built with [Typer](https://typer.tiangolo.com/) for the CLI interface
- Uses the iTunes Search API for podcast discovery