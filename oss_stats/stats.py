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
        # Create NEW stats entry with this repo
        if repo.name not in cache:
            create_entry(cache, repo.name)

        # Use cached results if already computed
        if cache[repo.name]["commits"] != -1:
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name]["commits"]
            continue

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
    cache = load_cache()
    repos = gh.get_organization(org).get_repos(sort="updated")
    result = {}

    # Loops through each repo and counts PRs
    for repo in repos:
        if repo.name not in cache:
            create_entry(cache,repo.name)
        
        if "prs" not in cache[repo.name]:
            cache[repo.name]["prs"] = -1

        if cache[repo.name]["prs"] != -1:
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name]["prs"]
            continue
        num_PRs = 0
        try:
            num_PRs = repo.get_pulls(state="all").totalCount
        except Exception as _:
            num_PRs = 0
        cache[repo.name]["prs"] = num_PRs
        result[repo.name] = num_PRs
        print(repo.name + " Number of pull requests: " + str(cache[repo.name]["prs"]))
    save_cache(cache)
    return result


def fetch_issues():
    repos = gh.get_organization(org).get_repos()
    return [repo.get_issues(state="all").totalCount for repo in repos]


def fetch_stars():
    pass


def fetch_contributors():
    pass
