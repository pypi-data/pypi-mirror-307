import typer

app = typer.Typer()

@app.command()
def download(
    podcast_name: str = typer.Argument(..., help="Name of the podcast"),
    episode_title: str = typer.Argument(..., help="Title of the episode"),
    output_path: str = typer.Option(
        '.', '--output', '-o', help="Output directory for the downloaded file"
    )
):
    """
    Download a podcast episode by specifying the podcast name and episode title.
    """
    # Placeholder for the function implementation
    typer.echo(f"Podcast Name: {podcast_name}")
    typer.echo(f"Episode Title: {episode_title}")
    typer.echo(f"Output Path: {output_path}")

if __name__ == "__main__":
    app()
