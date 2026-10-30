from oss_stats.stats import *

load_dotenv(find_dotenv(usecwd=True))
token = os.getenv("GITHUB_TOKEN")
gh = Github(token)
repo = gh.get_organization("acmcsufoss").get_repo("oss-stats")

def test_getCommits():
    # Test case 1: Valid repository with commits
    result = get_commits(repo)
    assert result >= 0, f"Expected commits >= 0, but got {result}"

    # Test case 2: Repository with no commits
    # repo_name = "empty_repo"
    # expected_commits = 0
    # result = get_commits(repo_name)
    # assert result == expected_commits, f"Expected {expected_commits}, but got {result}"

    # Test case 3: Invalid repository name
    invalidDidntFind = False
    try:
        inv_repo = gh.get_organization("acmcsufoss").get_repo("invalid_repo")
    except Exception as e:
        invalidDidntFind = type(e).__name__ == "UnknownObjectException"
    assert invalidDidntFind, "Expected an exception for invalid repository name, but no exception was raised"
    