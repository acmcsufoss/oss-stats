import click
from rich.console import Console
from .stats import (
    fetch_commits,
    fetch_issues,
    fetch_prs,
    fetch_stars,
    fetch_contributors,
    fetch_latest_updates,
)

LOGO = """
                                      __              
                                     / _|             
  __ _  ___ _ __ ___   ___ ___ _   _| |_ ___  ___ ___ 
 / _` |/ __| '_ ` _ \\ / __/ __| | | |  _/ _ \\/ __/ __|
| (_| | (__| | | | | | (__\\__ \\ |_| | || (_) \\__ \\__ \\
 \\__,_|\\___|_| |_| |_|\\___|___/\\__,_|_| \\___/|___/___/

"""

console = Console()


@click.command()
@click.option(
    "--option",
    type=click.Choice(
        [
            "commits",
            "issues",
            "pull_requests",
            "stars",
            "contributors",
            "updates",
            "all",
        ]
    ),
)
def cli(option):
    """OSS Stats - Fetch GitHub stats from acmcsufoss and acmcsuf.com"""

    console.print(LOGO, style="#11D4B1", highlight=False)

    if option == "commits" or option == "all":
        commits = fetch_commits()
        console.print(f"{sum(commits.values())} total commits!")
    if option == "issues" or option == "all":
        issues = fetch_issues()
        console.print(f"{sum(issues.values())} total issues")
    if option == "pull_requests" or option == "all":
        prs = fetch_prs()
        console.print(f"{sum(prs.values())} total pull requests!")
    if option == "updates" or option == "all":
        fetch_latest_updates()
    if option == "stars" or option == "all":
        stars = fetch_stars()
        console.print(f"{sum(stars.values())} total stargazers!")
    if option == "contributors" or option == "all":
        contributors = fetch_contributors()
        contributors_set = set()
        for repo_contributors in contributors.values():
            for contributor in repo_contributors:
                contributors_set.add(contributor)
        console.print(f"All contributors: {list(contributors_set)}")
        console.print(f"{len(contributors_set)} total contributors!")


if __name__ == "__main__":
    cli()
