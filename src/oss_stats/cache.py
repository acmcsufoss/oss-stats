from pathlib import Path
from platformdirs import user_cache_path
import json

from .const import (
    COMMITS_KEY,
    CONTRIBUTORS_KEY,
    ISSUES_KEY,
    LAST_UPDATED_KEY,
    PULL_REQUESTS_KEY,
    STARS_KEY,
)

cache_dir = user_cache_path("oss-stats", appauthor=False)
Path.mkdir(cache_dir, parents=True, exist_ok=True)
CACHE_FILE = f"{cache_dir}/stats.json"


def load_cache(cachePath=CACHE_FILE):
    try:
        with open(cachePath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cache(cache, cachePath=CACHE_FILE):
    with open(cachePath, "w") as f:
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
