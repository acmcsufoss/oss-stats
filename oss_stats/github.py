from github import Github
import os

token = os.getenv("GITHUB_TOKEN")
github = Github(token)

org = "acmcsufoss"


def fetch_repositories():
    repos = github.get_organization(org).get_repos()
    return [repo.name for repo in repos]


# TODO: Create functions that fetch issues, PRs, commits, number of contributors,
# and more from acmcsufoss org and EthanThatOneKid/acmcsuf.com using the PyGithub library.

# fetch commits
def fetch_commits():
    repos = github.get_organization(org).get_repos()
    return [repo.get_commits() for repo in repos]
