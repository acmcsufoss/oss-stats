import click
from rich.console import Console
from .stats import fetch_contributors, fetch_prs, fetch_commits, fetch_issues

console = Console()


@click.command()
@click.option(
    "--option", type=click.Choice(["commits", "prs", "issues", "contributors"])
)
def cli(option):
    """OSS Stats - Fetch GitHub stats from acmcsufoss and acmcsuf.com"""
    if option == "commits":
        commits = fetch_commits()
        console.print(f"{sum(commits.values())} total commits!")
    if option == "prs":
        prs = fetch_prs()
        console.print(f"{sum(prs.values())} total pull requests!")
    if option == "issues":
        issues = fetch_issues()
        console.print(f"{sum(issues)} total issues")
    if option == "contributors":
        contributors = fetch_contributors()
        console.print(contributors)


if __name__ == "__main__":
    cli()
