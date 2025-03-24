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


def get_commits(repo):
    return repo.get_commits().totalCount


def get_issues(repo):
    issues = repo.get_issues(state="all")
    issue_count = sum(1 for issue in issues if not issue.pull_request)
    return issue_count


def get_prs(repo):
    return repo.get_pulls(state="all").totalCount


def get_stars(repo):
    return repo.get_stargazers().totalCount


def get_contributors(repo):
    contributors = repo.get_contributors()
    contributors_res = []
    for contributor in contributors:
        contributors_res.append(f"{contributor.name} ({contributor.login})")
    return contributors_res


get_funcs = {
    "commits": get_commits,
    "issues": get_issues,
    "pull_requests": get_prs,
    "stars": get_stars,
    "contributors": get_contributors,
}


def fetch_resource(option: str, default_value):
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
            resource_value = get_funcs[option](repo)
        except Exception as _:
            resource_value = default_value

        if option != "updates":
            insert_latest_update(repo, cache)

        cache[repo.name][option] = resource_value
        result[repo.name] = resource_value
        print(f"{option} Count for {repo.name} = {cache[repo.name][option]}")
    save_cache(cache)
    return result


def fetch_commits():
    return fetch_resource(option="commits", default_value=-1)


def fetch_issues():
    return fetch_resource(option="issues", default_value=-1)


def fetch_prs():
    return fetch_resource(option="pull_requests", default_value=-1)


def fetch_stars():
    return fetch_resource(option="stars", default_value=-1)


def fetch_contributors():
    return fetch_resource(option="contributors", default_value=None)


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
