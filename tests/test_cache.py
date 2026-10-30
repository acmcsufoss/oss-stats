from oss_stats.cache import create_entry


from oss_stats.const import (
    COMMITS_KEY,
    CONTRIBUTORS_KEY,
    ISSUES_KEY,
    LAST_UPDATED_KEY,
    PULL_REQUESTS_KEY,
    STARS_KEY,
)


def test_createEntry(): #specific test cases
    testStats = {} 
    compare = { #we create an expected output to compare the testStats to (I just went through the codebase and looked at the function)
        "dummyRepo": {
            COMMITS_KEY: -1,
            ISSUES_KEY: -1,
            PULL_REQUESTS_KEY: -1,
            STARS_KEY: -1,
            CONTRIBUTORS_KEY: None,
            LAST_UPDATED_KEY: "",
        }
    }
    create_entry(stats=testStats, repo_name="dummyRepo") #we now test the function with input of dummy_repo
    assert testStats == compare #we assert that the output of the function is equal to the expected output
