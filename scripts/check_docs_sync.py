"""Reconciles README.md's stats block against the actual state of the repo.

Root-cause fix for the previous project's flagged issue: README claimed
numbers that didn't match pipeline_summary.json or the actual test count.
This script makes those numbers generated, not hand-typed.

Usage:
    python scripts/check_docs_sync.py            # check mode: exits 1 on mismatch
    python scripts/check_docs_sync.py --write     # regenerate the stats block in README.md

The stats block in README.md must be wrapped exactly like this:

<!-- STATS -->
- Synthetic filings: N
- Passing tests: N
- Sample summaries in evaluation/sample_summary.json: N
<!-- /STATS -->
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
SAMPLE_SUMMARY_PATH = REPO_ROOT / "evaluation" / "sample_summary.json"
STATS_BLOCK_RE = re.compile(
    r"<!-- STATS -->.*?<!-- /STATS -->", re.DOTALL
)


def count_synthetic_filings() -> int:
    data_dir = REPO_ROOT / "data" / "synthetic_filings"
    if not data_dir.exists():
        return 0
    return len(list(data_dir.glob("*.json")))


def count_passing_tests() -> int:
    """Counts collected tests via pytest --collect-only. Note: this counts
    *collected* tests, not necessarily passing ones — run `pytest` separately
    to confirm they pass. This script's job is consistency, not correctness.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    match = re.search(r"(\d+) tests? collected", result.stdout)
    return int(match.group(1)) if match else 0


def count_sample_summaries() -> int:
    if not SAMPLE_SUMMARY_PATH.exists():
        return 0
    with SAMPLE_SUMMARY_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    return len(data) if isinstance(data, list) else 1


def build_stats_block() -> str:
    filings = count_synthetic_filings()
    tests = count_passing_tests()
    summaries = count_sample_summaries()
    return (
        "<!-- STATS -->\n"
        f"- Synthetic filings: {filings}\n"
        f"- Collected tests: {tests}\n"
        f"- Sample summaries in evaluation/sample_summary.json: {summaries}\n"
        "<!-- /STATS -->"
    )


def read_current_block() -> str | None:
    if not README_PATH.exists():
        return None
    content = README_PATH.read_text(encoding="utf-8")
    match = STATS_BLOCK_RE.search(content)
    return match.group(0) if match else None


def write_stats_block() -> None:
    if not README_PATH.exists():
        raise FileNotFoundError(f"{README_PATH} does not exist yet — create it first.")
    content = README_PATH.read_text(encoding="utf-8")
    new_block = build_stats_block()
    if STATS_BLOCK_RE.search(content):
        content = STATS_BLOCK_RE.sub(new_block, content)
    else:
        content = content.rstrip() + "\n\n" + new_block + "\n"
    README_PATH.write_text(content, encoding="utf-8")
    print("README.md stats block updated:")
    print(new_block)


def check() -> bool:
    current = read_current_block()
    expected = build_stats_block()
    if current is None:
        print("No <!-- STATS --> block found in README.md. Run with --write to create one.")
        return False
    if current.strip() != expected.strip():
        print("MISMATCH between README.md stats and actual repo state.\n")
        print("README currently says:\n" + current + "\n")
        print("Actual state is:\n" + expected + "\n")
        print("Run: python scripts/check_docs_sync.py --write")
        return False
    print("README.md stats block matches actual repo state.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Regenerate the stats block in README.md")
    args = parser.parse_args()

    if args.write:
        write_stats_block()
        sys.exit(0)
    else:
        ok = check()
        sys.exit(0 if ok else 1)
