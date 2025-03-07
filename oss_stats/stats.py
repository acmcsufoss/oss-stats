import os
from github import Github
from dotenv import load_dotenv

from .cache import create_entry, load_cache, save_cache

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise Exception("No token present!")

gh = Github(token)

rate_limit = gh.get_rate_limit()
print(rate_limit.core.remaining, rate_limit.core.limit)
print(rate_limit.search.remaining, rate_limit.search.limit)

org = "acmcsufoss"


def fetch_commits():
    cache = load_cache()
    repos = gh.get_organization(org).get_repos(sort="updated")
    result = {}
    for repo in repos:
        if (
            repo.name in cache
            and "commits" in cache[repo.name]
            and cache[repo.name]["commits"] != 0
        ):
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name]["commits"]
            continue  # Skip API call

        create_entry(cache, repo.name)  # Create NEW stats entry with this repo
        try:
            commits = repo.get_commits().totalCount
        except Exception as _:
            commits = 0
        cache[repo.name]["commits"] = commits
        result[repo.name] = commits
        print(repo.name + " Number of commits: " + str(cache[repo.name]["commits"]))
    save_cache(cache)
    return result


def fetch_prs():
    repos = gh.get_organization(org).get_repos()
    num_PRs = 0
    # Loops through each repo and counts PRs
    for repo in repos:
        num_PRs += repo.get_pulls(state="all").totalCount
    return num_PRs


def fetch_issues():
    repos = gh.get_organization(org).get_repos()
    return [repo.get_issues(state="all").totalCount for repo in repos]


def fetch_stars():
    pass


def fetch_contributors():
    cache = load_cache()
    repos = gh.get_organization(org).get_repos(sort="updated")
    result = {}
    for repo in repos:
        if (repo.name in cache and "contributors" in cache[repo.name]
            and len(cache[repo.name]["contributors"]) > 0):
            print(f"Using cached list for {repo.name}")
            result[repo.name] = cache[repo.name]["contributors"]
            continue  # Skip API call
        create_entry(cache, repo.name)  # Create NEW stats entry with this repo
        try:
            contributors = repo.get_contributors()
        except Exception as _:
            contributors = []
        cache[repo.name]["contributors"] = contributors
        result[repo.name] = contributors
        print(repo.name + " List of Contributors: " + str(cache[repo.name]["contributors"]))
    save_cache(cache)
    return result
