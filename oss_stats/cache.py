import json

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
        "commits": 0,
        "issues": 0,
        "pull_requests": 0,
        "contributors": [],
        "star_count": 0,
        "last_updated": ""
    }
