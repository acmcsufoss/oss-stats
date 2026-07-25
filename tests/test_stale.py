#!/usr/bin/env python3
"""Behavioural checks for the configurable cache staleness threshold.

Run with:
    uv run python tests/test_stale.py

Importing oss_stats.stats performs module-level API work and exits if
GITHUB_TOKEN is unset, so these checks skip rather than fail when no token is
available. The assertions themselves make no network calls: they exercise
is_stale() and set_stale_after() against stub repos with fixed timestamps.
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

# stats.py resolves its dotenv path to src/.env rather than the repo root, so
# load the real one here to keep this runnable from a clean checkout.
load_dotenv(dotenv_path=REPO_ROOT / ".env")

if not os.getenv("GITHUB_TOKEN"):
    print("SKIP: GITHUB_TOKEN unset; oss_stats.stats cannot be imported without it.")
    sys.exit(0)

from oss_stats import stats  # noqa: E402


class StubRepo:
    """Stands in for a Repository with a fixed last-updated timestamp"""

    def __init__(self, days_ago: int) -> None:
        self.updated_at = datetime.now(timezone.utc) - timedelta(days=days_ago)


class NoTimestampRepo:
    """Repository whose updated_at raises AttributeError"""

    @property
    def updated_at(self) -> datetime:
        raise AttributeError("updated_at is unavailable")


class BadTimestampRepo:
    """Repository whose updated_at raises ValueError"""

    @property
    def updated_at(self) -> datetime:
        raise ValueError("unparseable timestamp")


failures: list[str] = []


def check(label: str, got: object, want: object) -> None:
    """Records a single assertion and prints its outcome"""
    if got == want:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}: got={got!r} want={want!r}")
        failures.append(label)


def main() -> int:
    """Runs every check and returns a process exit code"""
    original = stats.STALE_AFTER_DAYS
    try:
        check("default threshold is 90", stats.STALE_AFTER_DAYS, 90)

        print("\nat the 90-day default:")
        stats.set_stale_after(90)
        check("200d repo is reusable", stats.is_stale(StubRepo(200)), True)
        check("100d repo is reusable", stats.is_stale(StubRepo(100)), True)
        check("50d repo is not reusable", stats.is_stale(StubRepo(50)), False)
        check("5d repo is not reusable", stats.is_stale(StubRepo(5)), False)

        print("\nafter set_stale_after(30):")
        stats.set_stale_after(30)
        check("threshold updated", stats.STALE_AFTER_DAYS, 30)
        check("50d repo becomes reusable", stats.is_stale(StubRepo(50)), True)
        check("20d repo stays non-reusable", stats.is_stale(StubRepo(20)), False)

        print("\nset_stale_after(0) forces a full refresh:")
        stats.set_stale_after(0)
        check("10000d repo not reusable", stats.is_stale(StubRepo(10000)), False)
        check("1d repo not reusable", stats.is_stale(StubRepo(1)), False)

        print("\nerror handling:")
        stats.set_stale_after(90)
        check("AttributeError yields False", stats.is_stale(NoTimestampRepo()), False)
        check("ValueError yields False", stats.is_stale(BadTimestampRepo()), False)

        try:
            stats.set_stale_after(-1)
            check("negative threshold rejected", "no error", "ValueError")
        except ValueError:
            check("negative threshold rejected", True, True)
    finally:
        stats.set_stale_after(original)

    if failures:
        print(f"\n{len(failures)} FAILED: {failures}")
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
