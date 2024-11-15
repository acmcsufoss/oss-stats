import click
from rich.console import Console
from .github import fetch_repositories, fetch_prs

console = Console()


@click.command()
@click.option(
    "--option", type=click.Choice(["issues", "prs", "commits", "repositories"])
)
def cli(option):
    """OSS Stats - Fetch GitHub stats from acmcsufoss and acmcsuf.com"""
    if option == "repositories":
        repositories = fetch_repositories()
        print(repositories)
        console.print(f"{len(repositories)} total repositories!")
    if option == "prs":
        prs = fetch_prs()
        console.print(f"{prs} total pull requests")
    # TODO: Implement functionality for other options (issues, prs, commits)


if __name__ == "__main__":
    cli()
