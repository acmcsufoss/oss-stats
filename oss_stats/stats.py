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

    for repo in repos:
        if repo.name not in cache:
            create_entry(cache, repo.name)

        if cache[repo.name]["pull_requests"] != -1:
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name]["pull_requests"]
            continue

        try:
            pull_requests = repo.get_pulls(state="all").totalCount
        except Exception as _:
            pull_requests = 0

        cache[repo.name]["pull_requests"] = pull_requests
        result[repo.name] = pull_requests
        print(
            repo.name
            + " Number of Pull Requests: "
            + str(cache[repo.name]["pull_requests"])
        )
    save_cache(cache)
    return result


def fetch_issues():
    repos = gh.get_organization(org).get_repos()
    return [repo.get_issues(state="all").totalCount for repo in repos]


def fetch_stars():
    cache = load_cache()
    repos = gh.get_organization(org).get_repos(sort="updated")
    result = {}
    for repo in repos:
        if repo.name not in cache:
          create_entry(cache, repo.name)

        if cache[repo.name]["stars"] != -1:
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name]["stars"]
            continue

        try:
            stars = repo.get_starred().totalCount
        except Exception as _:
            stars = 0

        cache[repo.name]["stars"] = stars
        result[repo.name] = stars
        print(repo.name + " Number of Stars: " + str(cache[repo.name]["stars"]))
    save_cache(cache)
    return result


def fetch_contributors():
    cache = load_cache()
    repos = gh.get_organization(org).get_repos(sort="updated")
    result = {}
    for repo in repos:
        if repo.name not in cache:
            create_entry(cache, repo.name)

        if len(cache[repo.name]["contributors"]) > 0:
            print(f"Using cached list for {repo.name}")
            result[repo.name] = cache[repo.name]["contributors"]
            continue  # Skip API call

        try:
            contributors = repo.get_contributors()
            contributors_res = []
            for contributor in contributors:
                contributors_res.append(f"{contributor.name} ({contributor.login})")
        except Exception as _:
            contributors_res = []

        cache[repo.name]["contributors"] = contributors_res
        result[repo.name] = contributors_res
        print(f"{repo.name} List of Contributors: {cache[repo.name]['contributors']}")
    save_cache(cache)
    return result
