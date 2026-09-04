from oss_stats.cache import load_cache, save_cache, create_entry
import unittest

from oss_stats.const import (
    COMMITS_KEY,
    CONTRIBUTORS_KEY,
    ISSUES_KEY,
    LAST_UPDATED_KEY,
    PULL_REQUESTS_KEY,
    STARS_KEY,
)


class TestCache(unittest.TestCase):
    def test_createEntry(self):
        testStats = {}
        compare = {
            "dummyRepo": {
                COMMITS_KEY: -1,
                ISSUES_KEY: -1,
                PULL_REQUESTS_KEY: -1,
                STARS_KEY: -1,
                CONTRIBUTORS_KEY: None,
                LAST_UPDATED_KEY: "",
            }
        }
        create_entry(stats=testStats, repo_name="dummyRepo")
        self.assertEqual(testStats, compare)


if __name__ == "__main__":
    unittest.main()
