import click
from rich.console import Console
from .const import (
    ALL_KEY,
    COMMITS_KEY,
    CONTRIBUTORS_KEY,
    ISSUES_KEY,
    LAST_UPDATED_KEY,
    PULL_REQUESTS_KEY,
    STARS_KEY,
)
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
    COMMITS_KEY: {
        "fetch": fetch_commits,
        "handle": lambda data: console.print(f"{sum(data.values())} total commits!"),
    },
    ISSUES_KEY: {
        "fetch": fetch_issues,
        "handle": lambda data: console.print(f"{sum(data.values())} total issues"),
    },
    PULL_REQUESTS_KEY: {
        "fetch": fetch_prs,
        "handle": lambda data: console.print(
            f"{sum(data.values())} total pull requests!"
        ),
    },
    STARS_KEY: {
        "fetch": fetch_stars,
        "handle": lambda data: console.print(f"{sum(data.values())} total stargazers!"),
    },
    CONTRIBUTORS_KEY: {
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
    LAST_UPDATED_KEY: {
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
            COMMITS_KEY,
            ISSUES_KEY,
            PULL_REQUESTS_KEY,
            STARS_KEY,
            CONTRIBUTORS_KEY,
            LAST_UPDATED_KEY,
            ALL_KEY,
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
