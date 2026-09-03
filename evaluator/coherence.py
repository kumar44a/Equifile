"""Coherence proxy: bullet-count and length sanity checks per the brief's
spec (exactly 2 highlights, 2-3 risks, non-trivial bullet length). Returns a
0-1 score plus a list of human-readable error strings for anything that fails.
"""
from __future__ import annotations

from models import Report

MIN_BULLET_LEN = 15  # characters; guards against empty/near-empty bullets


def coherence_score(report: Report) -> tuple[float, list[str]]:
    errors: list[str] = []
    checks_passed = 0
    total_checks = 4

    if len(report.highlights) == 2:
        checks_passed += 1
    else:
        errors.append(f"Expected 2 highlights, got {len(report.highlights)}")

    if 2 <= len(report.risks) <= 3:
        checks_passed += 1
    else:
        errors.append(f"Expected 2-3 risks, got {len(report.risks)}")

    if all(len(h) >= MIN_BULLET_LEN for h in report.highlights):
        checks_passed += 1
    else:
        errors.append("One or more highlight bullets are too short")

    if all(len(r.text) >= MIN_BULLET_LEN for r in report.risks):
        checks_passed += 1
    else:
        errors.append("One or more risk bullets are too short")

    return checks_passed / total_checks, errors
