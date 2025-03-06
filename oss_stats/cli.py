import click
from rich.console import Console
from .stats import fetch_repositories, fetch_prs, fetch_commits, fetch_issues

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
    if option == "prs":
        prs = fetch_prs()
        console.print(f"{prs} total pull requests!")
    if option == "commits":
        commits = fetch_commits()
        console.print(f"{sum(commits.values())} total commits!")
    if option == "issues":
        issues = fetch_issues()
        console.print(f"{sum(issues)} total issues")


if __name__ == "__main__":
    cli()
