import os
import sys
from typing import List
from github import Github, GithubException
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from alive_progress import alive_bar

from github.Repository import Repository

from .const import (
    COMMITS_KEY,
    CONTRIBUTORS_KEY,
    ISSUES_KEY,
    LAST_UPDATED_KEY,
    PULL_REQUESTS_KEY,
    STARS_KEY,
)
from .cache import create_entry, load_cache, save_cache

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
token = os.getenv("GITHUB_TOKEN")

if not token:
    print("Please set your github token!")
    sys.exit(1)

gh = Github(token)
org = "acmcsufoss"

try:
    repos = gh.get_organization(org).get_repos(sort="updated")
except GithubException as e:
    print(f"GitHub API Error: {e.data.get('message', str(e))}")
    sys.exit(1)
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
    """Returns the total number of commits in the repository"""
    return repo.get_commits().totalCount


def get_issues(repo: Repository) -> int:
    """Returns the number of issues (excluding pull requests) in the repository"""
    return sum(1 for issue in repo.get_issues(state="all") if not issue.pull_request)


def get_prs(repo: Repository) -> int:
    """Returns the total number of pull requests in the repository"""
    return repo.get_pulls(state="all").totalCount


def get_stars(repo: Repository) -> int:
    """Returns the number of stargazers (stars) for the repository"""
    return repo.get_stargazers().totalCount


def get_contributors(repo: Repository) -> List[str]:
    """Returns a list of contributor names and usernames in the format 'Name (username)'"""
    return [
        f"{contributor.name} ({contributor.login})"
        for contributor in repo.get_contributors()
    ]


def get_latest_update(repo: Repository) -> str:
    """Returns when the repository was last updated in ISO format"""
    return repo.updated_at.isoformat()


RESOURCE_CONFIG = {
    COMMITS_KEY: {"default": -1, "getter": get_commits},
    ISSUES_KEY: {"default": -1, "getter": get_issues},
    PULL_REQUESTS_KEY: {"default": -1, "getter": get_prs},
    STARS_KEY: {"default": -1, "getter": get_stars},
    CONTRIBUTORS_KEY: {"default": None, "getter": get_contributors},
    LAST_UPDATED_KEY: {"default": "", "getter": get_latest_update},
}


def fetch_res(res: str):
    config = RESOURCE_CONFIG.get(res)
    if not config:
        raise ValueError(f"Unknown res option: {res}")

    default_value = config["default"]
    fetch_func = config["getter"]
    cache = load_cache()
    result = {}

    with alive_bar(repos.totalCount) as bar:
        for repo in repos:
            if repo.name not in cache:
                create_entry(cache, repo.name)

            is_stale_check_required = res != LAST_UPDATED_KEY
            if is_stale_check_required:
                # Use cached results if already computed and results are from 6+ months
                if cache[repo.name][res] != default_value and check_latest_update(repo):
                    result[repo.name] = cache[repo.name][res]
                    continue

            try:
                res_value = fetch_func(repo)
            except GithubException as e:
                print(e)
                res_value = default_value

            if res != LAST_UPDATED_KEY:
                insert_latest_update(repo, cache)

            cache[repo.name][res] = res_value
            result[repo.name] = res_value
            bar()
    save_cache(cache)
    return result


def fetch_commits():
    return fetch_res(COMMITS_KEY)


def fetch_issues():
    return fetch_res(ISSUES_KEY)


def fetch_prs():
    return fetch_res(PULL_REQUESTS_KEY)


def fetch_stars():
    return fetch_res(STARS_KEY)


def fetch_contributors():
    return fetch_res(CONTRIBUTORS_KEY)


def fetch_latest_updates():
    return fetch_res(LAST_UPDATED_KEY)


def retrieve_saved(res: str):
    cache = load_cache()
    result = {}
    for repo_name, repo_stats in cache.items():
        res_value = repo_stats[res]
        result[repo_name] = res_value
    return result


def retrieve_saved_commits():
    return retrieve_saved(COMMITS_KEY)


def retrieve_saved_issues():
    return retrieve_saved(ISSUES_KEY)


def retrieve_saved_prs():
    return retrieve_saved(PULL_REQUESTS_KEY)


def retrieve_saved_stars():
    return retrieve_saved(STARS_KEY)


def retrieve_saved_contributors():
    return retrieve_saved(CONTRIBUTORS_KEY)


def retrieve_saved_latest_updates():
    return retrieve_saved(LAST_UPDATED_KEY)
