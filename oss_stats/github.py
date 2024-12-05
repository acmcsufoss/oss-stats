from github import Github
import os

token = os.getenv("GITHUB_TOKEN")
github = Github(token)

org = "acmcsufoss"

def fetch_repositories():
    repos = github.get_organization(org).get_repos()
    return [repo.name for repo in repos]


def fetch_commits():
    repos = github.get_organization(org).get_repos()
    result = []
    for repo in repos:
        try:
            commits = repo.get_commits().totalCount
        except Exception as e:
            commits = 0
        result.append(commits)
    return result


def fetch_prs():
    repos = github.get_organization(org).get_repos()
    num_PRs = 0
    # Loops through each repo and counts PRs
    for repo in repos:
        num_PRs += repo.get_pulls(state="all").totalCount
    return num_PRs


def fetch_issues():
    repos = github.get_organization(org).get_repos()
    return [repo.get_issues(state="all").totalCount for repo in repos]
