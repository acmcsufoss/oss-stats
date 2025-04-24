import json

from .const import (
    COMMITS_KEY,
    CONTRIBUTORS_KEY,
    ISSUES_KEY,
    LAST_UPDATED_KEY,
    PULL_REQUESTS_KEY,
    STARS_KEY,
)

CACHE_FILE = "stats/stats.json"


def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)


def create_entry(stats, repo_name: str):
    stats[repo_name] = {
        COMMITS_KEY: -1,
        ISSUES_KEY: -1,
        PULL_REQUESTS_KEY: -1,
        STARS_KEY: -1,
        CONTRIBUTORS_KEY: None,
        LAST_UPDATED_KEY: "",
    }
