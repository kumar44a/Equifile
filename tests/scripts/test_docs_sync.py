from scripts.check_docs_sync import check


def test_readme_stats_match_actual_repo_state():
    assert check(), (
        "README.md stats are out of sync with the actual repo state. "
        "Run: python scripts/check_docs_sync.py --write"
    )
