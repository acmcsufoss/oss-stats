import argparse
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
    STALE_AFTER_DAYS,
    set_stale_after,
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
                                    ______      ______   ______  __    __ ________ 
                                  _/      \_   /      \ /      \|  \  |  \        \
  ______   _______ ______ ____   /   ▓▓▓▓▓▓ \ |  ▓▓▓▓▓▓\  ▓▓▓▓▓▓\ ▓▓  | ▓▓ ▓▓▓▓▓▓▓▓
 |      \ /       \      \    \ /  ▓▓▓____▓▓▓\| ▓▓   \▓▓ ▓▓___\▓▓ ▓▓  | ▓▓ ▓▓__    
  \▓▓▓▓▓▓\  ▓▓▓▓▓▓▓ ▓▓▓▓▓▓\▓▓▓▓\  ▓▓/     \ ▓▓\ ▓▓      \▓▓    \| ▓▓  | ▓▓ ▓▓  \   
 /      ▓▓ ▓▓     | ▓▓ | ▓▓ | ▓▓ ▓▓|  ▓▓▓▓▓| ▓▓ ▓▓   __ _\▓▓▓▓▓▓\ ▓▓  | ▓▓ ▓▓▓▓▓   
|  ▓▓▓▓▓▓▓ ▓▓_____| ▓▓ | ▓▓ | ▓▓ ▓▓| ▓▓| ▓▓| ▓▓ ▓▓__/  \  \__| ▓▓ ▓▓__/ ▓▓ ▓▓      
 \▓▓    ▓▓\▓▓     \ ▓▓ | ▓▓ | ▓▓ ▓▓ \▓▓  ▓▓| ▓▓\▓▓    ▓▓\▓▓    ▓▓\▓▓    ▓▓ ▓▓      
  \▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓\▓▓  \▓▓  \▓▓\▓▓\ \▓▓▓▓▓▓▓▓  \▓▓▓▓▓▓  \▓▓▓▓▓▓  \▓▓▓▓▓▓ \▓▓      
                                 \▓▓\ __/   \                                      
                                  \▓▓▓    ▓▓▓                                      
                                    \▓▓▓▓▓▓                                        
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


def cli():
    # -- cli arguments --
    parser = argparse.ArgumentParser(
        description="OSS Stats - Fetch GitHub stats from acmcsufoss and acmcsuf.com"
    )
    parser.add_argument(
        "-a",
        "--actions",
        metavar="[refetch | aggregate]",
        help="refetch fetches data from github | aggregate displays the data in the terminal",
        #        nargs='+',
        choices=ACTION_CHOICES,
    )
    parser.add_argument(
        "-r",
        "--resources",
        metavar="[commits | issues | pull_requests | stars | contributors | last_updated | all]",
        help="resource to fetch/display",
        #        nargs='+',
        choices=(RESOURCE_CHOICES + [ALL_KEY]),
    )
    parser.add_argument(
        "--stale-after",
        metavar="DAYS",
        type=int,
        default=STALE_AFTER_DAYS,
        help=(
            "reuse cached stats for repos untouched for at least DAYS days "
            f"(default: {STALE_AFTER_DAYS}); 0 forces a full refresh"
        ),
    )

    args = parser.parse_args()

    try:
        set_stale_after(args.stale_after)
    except ValueError as e:
        parser.error(str(e))

    actions = args.actions
    resources = args.resources
    # -- cli arguments end --

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
