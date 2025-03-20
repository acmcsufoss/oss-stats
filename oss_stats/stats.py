import os
from github import Github
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

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
repos = gh.get_organization(org).get_repos(sort="updated")

six_months_ago = datetime.now(timezone.utc) - timedelta(days=182)


def check_latest_update(repo):
    try:
        last_time = repo.updated_at
        return last_time < six_months_ago
    except ValueError:
        return False  # Force Update if parsing fails


def insert_latest_update(repo, cache):
    try:
        cache[repo.name]["last_updated"] = repo.updated_at.isoformat()
    except Exception as _:
        pass


def fetch_commits():
    cache = load_cache()
    result = {}

    for repo in repos:
        # Create NEW stats entry with this repo
        if repo.name not in cache:
            create_entry(cache, repo.name)

        # Use cached results if already computed and results are from 6+ months
        if cache[repo.name]["commits"] != -1 and check_latest_update(repo):
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name]["commits"]
            continue

        try:
            commit_count = repo.get_commits().totalCount
        except Exception as _:
            commit_count = -1
        cache[repo.name]["commits"] = commit_count
        result[repo.name] = commit_count
        print(repo.name + " Number of commits: " + str(cache[repo.name]["commits"]))
    save_cache(cache)
    return result


def fetch_issues():
    cache = load_cache()
    result = {}
    for repo in repos:
        if repo.name not in cache:
            create_entry(cache, repo.name)

        if cache[repo.name]["issues"] != -1 and check_latest_update(repo):
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name]["issues"]
            continue

        try:
            issues = repo.get_issues(state="all")
            # Pull Requests are also considered Issues, but we don't count them
            issue_count = sum(1 for issue in issues if not issue.pull_request)
        except Exception as _:
            issue_count = -1

        insert_latest_update(repo, cache)
        cache[repo.name]["issues"] = issue_count
        result[repo.name] = issue_count
        print(repo.name + " Number of Issues: " + str(cache[repo.name]["issues"]))

    save_cache(cache)
    return result


def fetch_prs():
    cache = load_cache()
    result = {}
    for repo in repos:
        if repo.name not in cache:
            create_entry(cache, repo.name)

        if cache[repo.name]["pull_requests"] != -1 and check_latest_update(repo):
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name]["pull_requests"]
            continue

        try:
            pull_request_count = repo.get_pulls(state="all").totalCount
        except Exception as _:
            pull_request_count = -1

        insert_latest_update(repo, cache)
        cache[repo.name]["pull_requests"] = pull_request_count
        result[repo.name] = pull_request_count
        print(
            repo.name
            + " Number of Pull Requests: "
            + str(cache[repo.name]["pull_requests"])
        )
    save_cache(cache)
    return result


def fetch_stars():
    cache = load_cache()
    result = {}
    for repo in repos:
        if repo.name not in cache:
            create_entry(cache, repo.name)

        if cache[repo.name]["star_count"] != -1 and check_latest_update(repo):
            print(f"Using cached count for {repo.name}")
            result[repo.name] = cache[repo.name]["star_count"]
            continue

        try:
            star_count = repo.get_stargazers().totalCount
        except Exception as _:
            star_count = -1

        insert_latest_update(repo, cache)
        cache[repo.name]["star_count"] = star_count
        result[repo.name] = star_count
        print(repo.name + " Number of Stars: " + str(cache[repo.name]["star_count"]))
    save_cache(cache)
    return result


def fetch_contributors():
    cache = load_cache()
    result = {}

    for repo in repos:
        if repo.name not in cache:
            create_entry(cache, repo.name)

        if cache[repo.name]["contributors"] is not None and check_latest_update(repo):
            print(f"Using cached list for {repo.name}")
            result[repo.name] = cache[repo.name]["contributors"]
            continue

        try:
            contributors = repo.get_contributors()
            contributors_res = []
            for contributor in contributors:
                contributors_res.append(f"{contributor.name} ({contributor.login})")
        except Exception as _:
            contributors_res = None

        insert_latest_update(repo, cache)
        cache[repo.name]["contributors"] = contributors_res
        result[repo.name] = contributors_res
        print(f"{repo.name} List of Contributors: {cache[repo.name]['contributors']}")
    save_cache(cache)
    return result


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
