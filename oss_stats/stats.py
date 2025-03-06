from github import Github
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise Exception("No token present!")

gh = Github(token)

rate_limit = gh.get_rate_limit()
print(rate_limit.core.remaining, rate_limit.core.limit)
print(rate_limit.search.remaining, rate_limit.search.limit)


org = "acmcsufoss"

def fetch_repositories():
    repos = gh.get_organization(org).get_repos()
    return [repo.name for repo in repos]


def fetch_commits():
    repos = gh.get_organization(org).get_repos()
    result = []
    for repo in repos:
        try:
            commits = repo.get_commits().totalCount
        except Exception as _:
            commits = 0
        result.append(commits)
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
