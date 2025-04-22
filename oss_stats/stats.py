import os
from typing import List
from github import Github, GithubException
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from github.Repository import Repository

from .cache import create_entry, load_cache, save_cache

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise Exception("No token present!")

gh = Github(token)
org = "acmcsufoss"

repos = gh.get_organization(org).get_repos(sort="updated")
six_months_ago = datetime.now(timezone.utc) - timedelta(days=182)


def check_latest_update(repo):
    try:
        last_time = repo.updated_at
        return last_time < six_months_ago
    except ValueError:
        return False


def insert_latest_update(repo, cache):
    try:
        cache[repo.name]["last_updated"] = repo.updated_at.isoformat()
    except Exception as _:
        pass


def get_commits(repo: Repository) -> int:
    """Returns the total number of commits in the repository."""
    return repo.get_commits().totalCount


def get_issues(repo: Repository) -> int:
    """Returns the number of issues (excluding pull requests) in the repository."""
    return sum(1 for issue in repo.get_issues(state="all") if not issue.pull_request)


def get_prs(repo: Repository) -> int:
    """Returns the total number of pull requests in the repository."""
    return repo.get_pulls(state="all").totalCount


def get_stars(repo: Repository) -> int:
    """Returns the number of stargazers (stars) for the repository."""
    return repo.get_stargazers().totalCount


def get_contributors(repo: Repository) -> List[str]:
    """Returns a list of contributor names and usernames in the format 'Name (username)'."""
    return [
        f"{contributor.name} ({contributor.login})"
        for contributor in repo.get_contributors()
    ]


resource_config = {
    "commits": {"default": -1, "getter": get_commits},
    "issues": {"default": -1, "getter": get_issues},
    "pull_requests": {"default": -1, "getter": get_prs},
    "stars": {"default": -1, "getter": get_stars},
    "contributors": {"default": None, "getter": get_contributors},
}


def fetch_resource(option: str):
    config = resource_config.get(option)
    if not config:
        raise ValueError(f"Unknown resource option: {option}")

    default_value = config["default"]
    fetch_func = config["getter"]
    cache = load_cache()
    result = {}

    for repo in repos:
        # Create NEW stats entry with this repo
        if repo.name not in cache:
            create_entry(cache, repo.name)

        # Use cached results if already computed and results are from 6+ months
        if cache[repo.name][option] != default_value and check_latest_update(repo):
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name][option]
            continue

        try:
            resource_value = fetch_func(repo)
        except GithubException as e:
            print(e)
            resource_value = default_value

        if option != "updates":
            insert_latest_update(repo, cache)

        cache[repo.name][option] = resource_value
        result[repo.name] = resource_value
        print(f"{option} Count for {repo.name} = {cache[repo.name][option]}")
    save_cache(cache)
    return result


fetch_commits = lambda: fetch_resource("commits")
fetch_issues = lambda: fetch_resource("issues")
fetch_prs = lambda: fetch_resource("pull_requests")
fetch_stars = lambda: fetch_resource("stars")
fetch_contributors = lambda: fetch_resource("contributors")


def fetch_latest_updates():
    cache = load_cache()
    for repo in repos:
        # Create new stats entry with this repo
        if repo.name not in cache:
            create_entry(cache, repo.name)
        try:
            # gets date from github
            date = repo.updated_at.isoformat()
        except Exception as _:
            date = ""
        cache[repo.name]["last_updated"] = date
        print(repo.name + " Last Updated: " + str(cache[repo.name]["last_updated"]))
    save_cache(cache)
