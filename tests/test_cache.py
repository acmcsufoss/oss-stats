from pathlib import Path

from oss_stats.cache import create_entry, load_cache, save_cache
import pytest

from oss_stats.const import (
    COMMITS_KEY,
    CONTRIBUTORS_KEY,
    ISSUES_KEY,
    LAST_UPDATED_KEY,
    PULL_REQUESTS_KEY,
    STARS_KEY,
)

TEST_DATA = (
    Path(__file__).parent / "test_data"
)  # folder with the test json files, works no matter where pytest is run from


def test_createEntry():  # specific test cases
    testStats = {}
    compare = {  # we create an expected output to compare the testStats to (I just went through the codebase and looked at the function)
        "dummyRepo": {
            COMMITS_KEY: -1,
            ISSUES_KEY: -1,
            PULL_REQUESTS_KEY: -1,
            STARS_KEY: -1,
            CONTRIBUTORS_KEY: None,
            LAST_UPDATED_KEY: "",
        }
    }
    create_entry(
        stats=testStats, repo_name="dummyRepo"
    )  # we now test the function with input of dummy_repo
    assert testStats == compare, (
        f"Dictionary output does not match.\n"
        f"\nExpected:\n{compare!r}\n\n"
        f"Got:\n{testStats!r}"
    )  # we assert that the output of the function is equal to the expected output


def test_loadEntry():
    compareEmptyRepo = {}  # we need an empty repo to test what happens when there is no file or if there is an error
    compareValidRepo = {  # a valid repo
        "acmcsuf.com": {
            "commits": 2227,
            "issues": -1,
            "pull_requests": -1,
            "stars": -1,
            "contributors": None,
            "last_updated": "2026-08-13T04:19:31+00:00",
        }
    }

    # Test Case 1: Cache file doesn't exist.
    # ----------------------------------------------------------

    # we want to use try and except so we can fail if FileNotFoundError is incorrectly handled.
    try:
        load_cache("nonExistent.json")
    except Exception:
        pytest.fail(
            "Unhandled or incorrect exception. The exception to be handled should be 'FileNotFoundError.'"
        )

    # test the return output
    testOutput = load_cache("nonExistent.json")  # have some test dictionary
    assert compareEmptyRepo == testOutput, (
        f"Expected empty dictionary '{compareEmptyRepo}', but got '{testOutput}'"
    )

    # Test Case 2: Bad JSON file.
    # ----------------------------------------------------------

    # we want to use try and except so we can fail if JSONDecodeError is incorrectly handled.
    try:
        testOutput = load_cache(
            TEST_DATA / "dummyBad.json"
        )  # load the real bad file; if the function lets JSONDecodeError escape, that raises error.
    except Exception:
        pytest.fail(
            "Unhandled or incorrect exception. The exception to be handled should be 'JSONDecodeError'"
        )

    # test the return output
    assert compareEmptyRepo == testOutput, (
        f"Expected empty dictionary '{compareEmptyRepo}', but got '{testOutput}'"
    )

    # Test Case 3: Valid Cache File Exists
    # ----------------------------------------------------------

    testOutput = load_cache(TEST_DATA / "dummyValid.json")
    assert compareValidRepo == testOutput, (
        f"Dictionary output does not match.\n"
        f"\nExpected:\n{compareValidRepo!r}\n\n"
        f"Got:\n{testOutput!r}"
    )


def test_saveEntry(tmp_path):
    testRepo = {  # a valid repo
        "acmcsuf.com": {
            "commits": 2227,
            "issues": -1,
            "pull_requests": -1,
            "stars": -1,
            "contributors": None,
            "last_updated": "2026-08-13T04:19:31+00:00",
        }
    }
    filePath = tmp_path / "cache.json"
    save_cache(testRepo, filePath)

    # Test Case 1: Has the file been created yet?
    assert filePath.exists(), "Cache file has not been created."

    # Test Case 2: Read Cache File
    # ----------------------------------------------------------

    loadedRepo = load_cache(filePath)
    assert loadedRepo == testRepo, (
        f"Loaded repository after save_cache does not match expected.\n"
        f"\nExpected:\n{testRepo!r}\n\n"
        f"Got:\n{loadedRepo!r}"
    )  # we assert that the output of the function is equal to the expected output

    # Test Case 3: Overwrite Cache File
    # ----------------------------------------------------------
    newTestRepo = {  # a valid repo
        "api.acmcsuf.com": {
            "commits": 537,
            "issues": 68,
            "pull_requests": -1,
            "stars": -1,
            "contributors": None,
            "last_updated": "2026-08-21T03:06:45+00:00",
        }
    }
    save_cache(newTestRepo, filePath)
    loadedRepo = load_cache(filePath)
    assert loadedRepo == newTestRepo, (
        f"Loaded repository after overwrite does not match expected.\n"
        f"\nExpected:\n{newTestRepo!r}\n\n"
        f"Got:\n{loadedRepo!r}"
    )  # we assert that the output of the function is equal to the expected output
