import click
from rich.console import Console
import questionary
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
    retrieve_saved_commits,
    retrieve_saved_issues,
    retrieve_saved_prs,
    retrieve_saved_stars,
    retrieve_saved_contributors,
    retrieve_saved_latest_updates,
)

LOGO = r"""
                                     / _|
  __ _  ___ _ __ ___   ___ ___ _   _| |_ ___  ___ ___
 / _` |/ __| '_ ` _ \ / __/ __| | | |  _/ _ \/ __/ __|
| (_| | (__| | | | | | (__\__ \ |_| | || (_) \__ \__ \
 \__,_|\___|_| |_| |_|\___|___/\__,_|_| \___/|___/___/
"""

console = Console()

STAT_HANDLERS = {
    COMMITS_KEY: {
        "fetch": fetch_commits,
        "retrieve_saved": retrieve_saved_commits,
        "handle": lambda data: console.print(f"{sum(data.values())} total commits!"),
    },
    ISSUES_KEY: {
        "fetch": fetch_issues,
        "retrieve_saved": retrieve_saved_issues,
        "handle": lambda data: console.print(f"{sum(data.values())} total issues"),
    },
    PULL_REQUESTS_KEY: {
        "fetch": fetch_prs,
        "retrieve_saved": retrieve_saved_prs,
        "handle": lambda data: console.print(
            f"{sum(data.values())} total pull requests!"
        ),
    },
    STARS_KEY: {
        "fetch": fetch_stars,
        "retrieve_saved": retrieve_saved_stars,
        "handle": lambda data: console.print(f"{sum(data.values())} total stargazers!"),
    },
    CONTRIBUTORS_KEY: {
        "fetch": fetch_contributors,
        "retrieve_saved": retrieve_saved_contributors,
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
        "retrieve_saved": retrieve_saved_latest_updates,
        "handle": lambda _: None,
    },
}

OSS_GREEN = "#11D4B1"
ACTION_CHOICES = ["refetch", "aggregate"]
RESOURCE_CHOICES = list(STAT_HANDLERS.keys())


@click.command()
@click.option("--actions", "-a", type=click.Choice(ACTION_CHOICES), multiple=True)
@click.option(
    "--resources", "-r", type=click.Choice(RESOURCE_CHOICES + [ALL_KEY]), multiple=True
)
def cli(actions, resources):
    """OSS Stats - Fetch GitHub stats from acmcsufoss and acmcsuf.com"""
    console.print(LOGO, style=OSS_GREEN, highlight=False)

    if not actions:
        console.print(
            "What would you like to do today?\n",
            style=OSS_GREEN,
            highlight=False,
        )
        actions = questionary.checkbox(
            "Select one or more options:", choices=ACTION_CHOICES
        ).ask()

    if not resources:
        console.print(
            "What resources would you like to fetch?\n",
            style=OSS_GREEN,
            highlight=False,
        )
        resources = questionary.checkbox(
            "Select one or more options:", choices=RESOURCE_CHOICES + [ALL_KEY]
        ).ask()

    if ALL_KEY in resources:
        resources = RESOURCE_CHOICES

    console.print(
        f"\nYou selected: [{OSS_GREEN}]{resources}[/{OSS_GREEN}]\n",
        highlight=False,
    )

    for resource in resources:
        if "refetch" in actions:
            console.print(
                f"\nFetching resource: [{OSS_GREEN}]{resource}[/{OSS_GREEN}]\n",
                highlight=False,
            )
            try:
                data = STAT_HANDLERS[resource]["fetch"]()
            except Exception as e:
                console.print(f"Failed to fetch or handle '{resource}': {e}")
        if "aggregate" in actions:
            console.print(
                f"\nRetrieving saved resource: [{OSS_GREEN}]{resource}[/{OSS_GREEN}]\n",
                highlight=False,
            )
            try:
                data = STAT_HANDLERS[resource]["retrieve_saved"]()
                STAT_HANDLERS[resource]["handle"](data)
            except Exception as e:
                console.print(f"Failed to fetch or handle '{resource}': {e}")


if __name__ == "__main__":
    cli()
