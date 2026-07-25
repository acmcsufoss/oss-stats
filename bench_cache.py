#!/usr/bin/env python3
"""
Benchmark cache effectiveness for acmcsufoss/oss-stats.

Measures cold (no cache) vs warm (populated cache) runs across all resources,
reporting wall-clock time AND the number of HTTP requests issued to the GitHub
API. Request count is the more meaningful metric: wall-clock varies with
network conditions, but calls-saved is deterministic.

Usage:
    cp bench_cache.py <repo-root>/
    cd <repo-root>
    uv run python bench_cache.py

Requires GITHUB_TOKEN in .env, same as the CLI.
Writes results to bench_results.json.
"""

import datetime
import json
import shutil
import time
from pathlib import Path

import requests
from platformdirs import user_cache_path

# PyGithub 2.x issues every request through requests.Session.request, so wrapping
# that method counts real HTTP traffic. This replaces diffing
# get_rate_limit().core.remaining, which does not reliably move during a run and
# therefore reported garbage call counts.
_orig_request = requests.Session.request
_counter = {"n": 0}


def _counting_request(self, method, url, *args, **kwargs):
    """Wrapper around requests.Session.request that tallies every call."""
    _counter["n"] += 1
    return _orig_request(self, method, url, *args, **kwargs)


requests.Session.request = _counting_request

CACHE_FILE = Path(user_cache_path("oss-stats", appauthor=False)) / "stats.json"
BACKUP = CACHE_FILE.with_suffix(".json.benchbak")

RESOURCES = ["commits", "issues", "pull_requests", "stars", "contributors"]


def rate_remaining(gh):
    """Core rate-limit units left. PyGithub's own call here is not billed."""
    return gh.get_rate_limit().core.remaining


def clear_cache():
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()


def cache_stats(stale_after_days):
    """How many repos are in cache and how many are stale enough to be reused.

    Takes the threshold rather than hardcoding it so the reported
    cache-eligible count tracks whatever STALE_AFTER_DAYS the code under
    measurement actually uses.
    """
    if not CACHE_FILE.exists():
        return 0, 0
    data = json.loads(CACHE_FILE.read_text())
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        days=stale_after_days
    )
    stale = 0
    for entry in data.values():
        ts = entry.get("last_updated") or ""
        try:
            if datetime.datetime.fromisoformat(ts) < cutoff:
                stale += 1
        except ValueError:
            pass
    return len(data), stale


def run_pass(label, gh, fetchers):
    """Time one full pass over every resource, recording calls consumed."""
    print(f"\n--- {label} ---")
    per_resource = {}
    before_all = _counter["n"]
    t_all = time.perf_counter()

    for name in RESOURCES:
        before = _counter["n"]
        t0 = time.perf_counter()
        try:
            fetchers[name]()
        except Exception as exc:  # keep going; record the failure
            print(f"  {name:15s} FAILED: {exc}")
            per_resource[name] = {"error": str(exc)}
            continue
        elapsed = time.perf_counter() - t0
        used = _counter["n"] - before
        per_resource[name] = {"seconds": round(elapsed, 2), "api_calls": used}
        print(f"  {name:15s} {elapsed:7.2f}s   {used:4d} calls")

    total_time = time.perf_counter() - t_all
    total_calls = _counter["n"] - before_all
    print(f"  {'TOTAL':15s} {total_time:7.2f}s   {total_calls:4d} calls")
    return {
        "total_seconds": round(total_time, 2),
        "total_api_calls": total_calls,
        "per_resource": per_resource,
    }


def main():
    # Preserve whatever the user already had cached.
    had_backup = False
    if CACHE_FILE.exists():
        shutil.copy2(CACHE_FILE, BACKUP)
        had_backup = True
        print(f"Backed up existing cache -> {BACKUP}")

    try:
        # Import AFTER backup: stats.py does module-level API work on import.
        from oss_stats.stats import (
            gh,
            fetch_commits,
            fetch_issues,
            fetch_prs,
            fetch_stars,
            fetch_contributors,
        )

        fetchers = {
            "commits": fetch_commits,
            "issues": fetch_issues,
            "pull_requests": fetch_prs,
            "stars": fetch_stars,
            "contributors": fetch_contributors,
        }

        # Falls back to 182 so this script can also measure pre-change code,
        # which hardcoded the threshold and exposes no constant to read.
        try:
            from oss_stats.stats import STALE_AFTER_DAYS
        except ImportError:
            STALE_AFTER_DAYS = 182

        budget = rate_remaining(gh)
        print(f"Rate limit available: {budget}")
        if budget < 1200:
            print("WARNING: low budget. A cold+warm pass may exhaust it.")
            print("Wait for reset or the warm numbers will be garbage.")

        clear_cache()
        cold = run_pass("COLD (cache cleared)", gh, fetchers)

        n_repos, n_stale = cache_stats(STALE_AFTER_DAYS)
        print(
            f"\nCache populated: {n_repos} repos, "
            f"{n_stale} stale (>{STALE_AFTER_DAYS}d, reusable)"
        )

        warm = run_pass("WARM (cache populated)", gh, fetchers)

        call_delta = cold["total_api_calls"] - warm["total_api_calls"]
        time_delta = cold["total_seconds"] - warm["total_seconds"]
        call_pct = (
            call_delta / cold["total_api_calls"] * 100 if cold["total_api_calls"] else 0
        )
        time_pct = (
            time_delta / cold["total_seconds"] * 100 if cold["total_seconds"] else 0
        )

        print("\n=== RESULT ===")
        print(
            f"repos: {n_repos}   cache-eligible: {n_stale} ({n_stale / n_repos * 100:.0f}%)"
        )
        print(
            f"API calls : {cold['total_api_calls']} -> {warm['total_api_calls']}  ({call_pct:.1f}% fewer)"
        )
        print(
            f"Wall clock: {cold['total_seconds']:.1f}s -> {warm['total_seconds']:.1f}s  ({time_pct:.1f}% faster)"
        )
        print("\nUse the API-calls figure on your resume, not wall clock.")
        print(
            "Wall clock depends on your network; calls-saved is a property of the code."
        )

        results = {
            "measured_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "repos": n_repos,
            "stale_after_days": STALE_AFTER_DAYS,
            "cache_eligible_repos": n_stale,
            "cold": cold,
            "warm": warm,
            "api_call_reduction_pct": round(call_pct, 1),
            "wall_clock_reduction_pct": round(time_pct, 1),
        }

        # Key each run by the threshold that produced it and merge, so running
        # this at two thresholds leaves both measurements side by side rather
        # than overwriting the earlier one.
        out_path = Path("bench_results.json")
        try:
            existing = json.loads(out_path.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            existing = {}
        if "runs" not in existing:
            existing = {"runs": {}}
        existing["runs"][str(STALE_AFTER_DAYS)] = results
        out_path.write_text(json.dumps(existing, indent=2))
        print(f"\nWrote bench_results.json (runs: {sorted(existing['runs'])})")

    finally:
        if had_backup:
            shutil.copy2(BACKUP, CACHE_FILE)
            BACKUP.unlink()
            print("Restored original cache.")


if __name__ == "__main__":
    main()
