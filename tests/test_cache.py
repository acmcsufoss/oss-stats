from oss_stats.cache import create_entry
import unittest


from oss_stats.const import (
    COMMITS_KEY,
    CONTRIBUTORS_KEY,
    ISSUES_KEY,
    LAST_UPDATED_KEY,
    PULL_REQUESTS_KEY,
    STARS_KEY,
)


class TestCache(unittest.TestCase): #We create a class that inherits from unittest.TestCase
    #the purpose of the test should be to generate a dummyRepo in testStats
    def test_createEntry(self): #specific test cases
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
        self.assertEqual(testStats, compare) #set them equal to each other and assert if the test passes



if __name__ == "__main__":
    unittest.main()
