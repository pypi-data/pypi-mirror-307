
import os
import sys
import logging
import requests
import json
import feedparser
import typer
from typing import List, Optional
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from tqdm import tqdm
import whisper
import torch
import time

app = typer.Typer()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("podgrab.log"),
        logging.StreamHandler()
    ]
)

@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress non-error messages")
):
    """
    Entry point for the CLI application.

    Sets the logging level based on the provided command-line options.

    Args:
        verbose (bool): Enable verbose output (DEBUG level logging).
        quiet (bool): Suppress non-error messages (set logging level to ERROR).
    """
    if quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

@app.command()
def download(
    podcast_name: str = typer.Argument(..., help="Name of the podcast"),
    episode_title: str = typer.Argument(..., help="Title of the episode"),
    output_path: Path = typer.Option(
        '.', '--output', '-o', help="Output directory for the downloaded file"
    ),
    non_interactive: bool = typer.Option(
        False, '--non-interactive', help="Run in non-interactive mode"
    )
):
    """
    Download a podcast episode by specifying the podcast name and episode title.

    This command searches for the podcast using the iTunes Search API, retrieves the RSS feed,
    finds the specified episode, and downloads the audio file to the output directory.

    Args:
        podcast_name (str): Name of the podcast to search for.
        episode_title (str): Title of the episode to download.
        output_path (Path): Directory where the downloaded file will be saved.
        non_interactive (bool): Run without interactive prompts (automatic selections).

    Raises:
        SystemExit: Exits the program if an error occurs.
    """
    try:
        # Input validation
        podcast_name = podcast_name.strip()
        episode_title = episode_title.strip()

        if not podcast_name:
            logging.error("Podcast name cannot be empty.")
            typer.echo("Error: Podcast name cannot be empty.")
            sys.exit(1)

        if not episode_title:
            logging.error("Episode title cannot be empty.")
            typer.echo("Error: Episode title cannot be empty.")
            sys.exit(1)

        if not output_path.is_dir():
            logging.error(f"The output path '{output_path}' is not a valid directory.")
            typer.echo(f"Error: The output path '{output_path}' is not a valid directory.")
            sys.exit(1)

        if not os.access(output_path, os.W_OK):
            logging.error(f"The output path '{output_path}' is not writable.")
            typer.echo(f"Error: The output path '{output_path}' is not writable.")
            sys.exit(1)

        # Search for the podcast using the iTunes Search API
        logging.info(f"Searching for podcast '{podcast_name}'")
        podcasts = search_podcast(podcast_name)

        if not podcasts:
            typer.echo(f"No podcasts found for '{podcast_name}'.")
            sys.exit(1)

        # Handle multiple podcast matches
        if len(podcasts) > 1 and not non_interactive:
            typer.echo(f"Multiple podcasts found for '{podcast_name}':")
            for idx, podcast in enumerate(podcasts, start=1):
                typer.echo(f"{idx}. {podcast['collectionName']} by {podcast.get('artistName', 'Unknown Artist')}")
            selection = typer.prompt("Enter the number of the podcast you want to download", type=int)
            if selection < 1 or selection > len(podcasts):
                typer.echo("Invalid selection.")
                sys.exit(1)
            podcast = podcasts[selection - 1]
        else:
            podcast = podcasts[0]
            if len(podcasts) > 1:
                typer.echo(f"Multiple podcasts found. Automatically selecting the first one due to non-interactive mode.")
                logging.warning("Multiple podcasts found. Automatically selected the first one.")

        feed_url = podcast.get('feedUrl')
        if not feed_url:
            typer.echo("RSS feed URL not found for the selected podcast.")
            sys.exit(1)

        # Retrieve and parse the RSS feed
        logging.info(f"Retrieving RSS feed from '{feed_url}'")
        feed = fetch_and_parse_feed(feed_url)

        # Search for the episode
        matching_episodes = find_episode(feed, episode_title)

        if not matching_episodes:
            typer.echo(f"No episodes found with title matching '{episode_title}'.")
            sys.exit(1)

        # Handle multiple episode matches
        if len(matching_episodes) > 1 and not non_interactive:
            typer.echo(f"Multiple episodes found matching '{episode_title}':")
            for idx, episode in enumerate(matching_episodes, start=1):
                pub_date = episode.get('published', 'Unknown Date')
                typer.echo(f"{idx}. {episode['title']} ({pub_date})")
            selection = typer.prompt("Enter the number of the episode you want to download", type=int)
            if selection < 1 or selection > len(matching_episodes):
                typer.echo("Invalid selection.")
                sys.exit(1)
            episode = matching_episodes[selection - 1]
        else:
            episode = matching_episodes[0]
            if len(matching_episodes) > 1:
                typer.echo(f"Multiple episodes found. Automatically selecting the first one due to non-interactive mode.")
                logging.warning("Multiple episodes found. Automatically selected the first one.")

        # Extract audio URL
        audio_url = get_audio_url(episode)
        if not audio_url:
            typer.echo("Audio URL not found for the selected episode.")
            sys.exit(1)

        # Prepare output file path
        file_extension = get_file_extension(audio_url)
        sanitized_title = sanitize_filename(episode['title'])
        file_name = f"{sanitized_title}{file_extension}"
        full_file_path = output_path / file_name

        if full_file_path.exists():
            if non_interactive:
                logging.info(f"The file '{full_file_path}' already exists. Overwriting in non-interactive mode.")
            else:
                typer.echo(f"The file '{full_file_path}' already exists.")
                overwrite = typer.confirm("Do you want to overwrite it?", default=False)
                if not overwrite:
                    typer.echo("Download canceled.")
                    sys.exit(0)

        # Download the audio file
        download_audio(audio_url, full_file_path)

        typer.echo("Download completed successfully.")

    except Exception as e:
        logging.exception("An unexpected error occurred.")
        typer.echo("An unexpected error occurred. Please check the log file for details.")
        sys.exit(1)

@app.command()
def transcribe(
    audio_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Path to the audio file to transcribe"
    ),
    model_name: str = typer.Option(
        "base",
        "--model",
        "-m",
        help="Name of the Whisper model to use (e.g., tiny, base, small, medium, large)"
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="File to save the transcription (defaults to printing to console)"
    )
):
    """
    Transcribe an audio file using OpenAI's Whisper model.
    """
    try:
        device = get_device()
        logging.info(f"Using device: {device}")

        logging.info(f"Loading Whisper model '{model_name}'")
        model = whisper.load_model(model_name, device=device)

        logging.info(f"Transcribing audio file '{audio_file}'")

        result = model.transcribe(str(audio_file), fp16=False)

        transcription = result['text']
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(transcription)
            typer.echo(f"Transcription saved to '{output_file}'")
        else:
            typer.echo(transcription)

    except Exception as e:
        logging.exception("An error occurred during transcription.")
        typer.echo("An error occurred during transcription. Please check the log file for details.")
        sys.exit(1)

def search_podcast(podcast_name: str) -> List[dict]:
    """
    Search for podcasts using the iTunes Search API.

    Args:
        podcast_name (str): The name of the podcast to search for.

    Returns:
        List[dict]: A list of podcasts matching the search term.

    Raises:
        SystemExit: Exits the program if a network error occurs.
    """
    try:
        params = {
            'term': podcast_name,
            'media': 'podcast',
            'limit': 10
        }
        response = requests.get('https://itunes.apple.com/search', params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        logging.exception("Error occurred while searching for the podcast.")
        typer.echo("Network error occurred while searching for the podcast.")
        sys.exit(1)

def fetch_and_parse_feed(feed_url: str) -> feedparser.FeedParserDict:
    """
    Fetch and parse the RSS feed from the given URL.

    Args:
        feed_url (str): The URL of the RSS feed to fetch.

    Returns:
        feedparser.FeedParserDict: The parsed RSS feed object.

    Raises:
        SystemExit: Exits the program if a network error occurs or parsing fails.
    """
    try:
        response = requests.get(feed_url, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        if feed.bozo:
            logging.error("Error parsing RSS feed.")
            typer.echo("Failed to parse the RSS feed.")
            sys.exit(1)
        return feed
    except requests.exceptions.RequestException as e:
        logging.exception("Error occurred while fetching the RSS feed.")
        typer.echo("Network error occurred while fetching the RSS feed.")
        sys.exit(1)

def find_episode(feed: feedparser.FeedParserDict, episode_title: str) -> List[dict]:
    """
    Find episodes in the feed that match the given episode title.

    Args:
        feed (feedparser.FeedParserDict): The parsed RSS feed.
        episode_title (str): The title (or partial title) of the episode to find.

    Returns:
        List[dict]: A list of episodes matching the title.

    """
    matching_episodes = []
    for entry in feed.entries:
        if episode_title.lower() in entry.title.lower():
            matching_episodes.append(entry)
    return matching_episodes

def get_audio_url(episode: dict) -> Optional[str]:
    """
    Extract the audio URL from the episode data.

    Args:
        episode (dict): The episode entry from the RSS feed.

    Returns:
        Optional[str]: The audio URL if found, otherwise None.
    """
    enclosures = episode.get('enclosures', [])
    if enclosures:
        return enclosures[0].get('href')
    return None

def get_file_extension(url: str) -> str:
    """
    Determine the file extension based on the URL.

    Args:
        url (str): The URL of the audio file.

    Returns:
        str: The file extension (e.g., '.mp3'). Defaults to '.mp3' if none found.
    """
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    if ext:
        return ext
    else:
        # Default to .mp3 if extension is not found
        return '.mp3'

def sanitize_filename(name: str) -> str:
    """
    Sanitize the file name by removing or replacing invalid characters.

    Args:
        name (str): The original file name.

    Returns:
        str: A sanitized file name safe for use in the file system.
    """
    return "".join(c for c in name if c.isalnum() or c in " ._-").rstrip()

def download_audio(url: str, output_path: Path):
    """
    Download the audio file from the given URL to the specified output path.

    Displays a progress bar during the download.

    Args:
        url (str): The URL of the audio file to download.
        output_path (Path): The file path where the audio will be saved.

    Raises:
        SystemExit: Exits the program if a network error occurs during download.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(output_path, 'wb') as f:
            for data in response.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        if total_size != 0 and t.n != total_size:
            typer.echo("ERROR: Download incomplete.")
            sys.exit(1)
        logging.info(f"Downloaded audio file to '{output_path}'")
    except requests.exceptions.RequestException as e:
        logging.exception("Error occurred while downloading the audio file.")
        typer.echo("Network error occurred while downloading the audio file.")
        sys.exit(1)


def get_device():
    """
    Returns the best available device: CUDA or CPU.
    Excludes MPS due to current limitations with sparse tensors.
    """
    if torch.cuda.is_available():
        return 'cuda'
    else:
        return 'cpu'

if __name__ == "__main__":
    app()
