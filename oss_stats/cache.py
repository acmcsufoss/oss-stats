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
        "commits": -1,
        "issues": -1,
        "pull_requests": -1,
        "stars": -1,
        "contributors": None,
        "last_updated": "",
    }
