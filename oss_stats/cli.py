import click
from rich.console import Console
from .github import fetch_repositories

console = Console()


@click.command()
@click.option(
    "--option", type=click.Choice(["issues", "PRs", "commits", "repositories"])
)
def cli(option):
    """OSS Stats - Fetch GitHub stats from acmcsufoss and acmcsuf.com"""
    if option == "repositories":
        repositories = fetch_repositories()
        print(repositories)
        console.print(f"{len(repositories)} total repositories!")
    # TODO: Implement functionality for other options


if __name__ == "__main__":
    cli()
