import click
from rich.console import Console
from .github import fetch_repositories, fetch_commits

console = Console()


import click
from rich.console import Console
from .github import fetch_commits, fetch_repositories

console = Console()


@click.command()
@click.option(
    "--option", type=click.Choice(["issues", "prs", "commits", "repositories"])
)
def cli(option):
    """OSS Stats - Fetch GitHub stats from acmcsufoss and acmcsuf.com"""
    if option == "repositories":
        repositories = fetch_repositories()
        console.print(f"{len(repositories)} total repositories!")
    if option == "commits":
        commits = fetch_commits()
        console.print(f"{sum(commits)} total commits!")
    # TODO: Implement functionality for remaining options (issues and prs)


if __name__ == "__main__":
    cli()