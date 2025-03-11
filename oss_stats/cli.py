import click
from rich.console import Console
from .stats import (
    fetch_commits,
    fetch_issues,
    fetch_prs,
    fetch_stars,
    fetch_contributors,
)

console = Console()


@click.command()
@click.option(
    "--option",
    type=click.Choice(["commits", "issues", "pull_requests", "stars", "contributors"]),
)
def cli(option):
    """OSS Stats - Fetch GitHub stats from acmcsufoss and acmcsuf.com"""
    if option == "commits":
        commits = fetch_commits()
        console.print(f"{sum(commits.values())} total commits!")
    if option == "issues":
        issues = fetch_issues()
        console.print(f"{sum(issues.values())} total issues")
    if option == "pull_requests":
        prs = fetch_prs()
        console.print(f"{sum(prs.values())} total pull requests!")
    if option == "stars":
        stars = fetch_stars()
        console.print(f"{sum(stars.values())} total stargazers!")
    if option == "contributors":
        contributors = fetch_contributors()
        contributors_set = set()
        for repo_contributors in contributors.values():
            for contributor in repo_contributors:
                contributors_set.add(contributor)
        console.print(f"All contributors: {list(contributors_set)}")
        console.print(f"{len(contributors_set)} total contributors!")


if __name__ == "__main__":
    cli()
