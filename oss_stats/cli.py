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

STAT_HANDLERS = {
    "commits": {
        "fetch": fetch_commits,
        "handle": lambda data: console.print(f"{sum(data.values())} total commits!"),
    },
    "issues": {
        "fetch": fetch_issues,
        "handle": lambda data: console.print(f"{sum(data.values())} total issues"),
    },
    "pull_requests": {
        "fetch": fetch_prs,
        "handle": lambda data: console.print(
            f"{sum(data.values())} total pull requests!"
        ),
    },
    "stars": {
        "fetch": fetch_stars,
        "handle": lambda data: console.print(f"{sum(data.values())} total stargazers!"),
    },
    "contributors": {
        "fetch": fetch_contributors,
        "handle": lambda data: (
            console.print(
                f"All contributors: {list(set(c for v in data.values() for c in v))}"
            ),
            console.print(
                f"{len(set(c for v in data.values() for c in v))} total contributors!"
            ),
        ),
    },
    "updates": {
        "fetch": fetch_latest_updates,
        "handle": lambda _: None,
    },
}


@click.command()
@click.option(
    "--resources",
    "-r",
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
    multiple=True,
)
def cli(resources):
    """OSS Stats - Fetch GitHub stats from acmcsufoss and acmcsuf.com"""

    console.print(LOGO, style="#11D4B1", highlight=False)

    resources = list(STAT_HANDLERS.keys()) if "all" in resources else resources
    for resource in resources:
        try:
            data = STAT_HANDLERS[resource]["fetch"]()
            STAT_HANDLERS[resource]["handle"](data)
        except Exception as e:
            console.print(
                f"[bold red]Failed to fetch or handle '{resource}':[/bold red] {e}"
            )


if __name__ == "__main__":
    cli()
