"""Analyze the gpt52_xhigh eval run and identify the hardest cases.

This is a small helper script for quickly summarizing which prompts are hardest
across tool variants.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from evals.dataset import EXPENSE_CASES


def main() -> None:
    results_path = Path("evals/runs/gpt52_xhigh/results.json")
    data = json.loads(results_path.read_text())

    by_case: dict[str, list[dict]] = defaultdict(list)
    for row in data["results"]:
        by_case[row["case_name"]].append(row)

    prompt_by_case = {c.name: c.prompt for c in EXPENSE_CASES}

    stats: list[tuple[float, int, float, str, int]] = []
    for case_name, rows in by_case.items():
        avg_score = sum(r["overall_score"] for r in rows) / len(rows)
        min_score = min(r["overall_score"] for r in rows)
        fail_count = sum(1 for r in rows if r["overall_score"] < 0.8)
        stats.append((avg_score, fail_count, min_score, case_name, len(rows)))

    stats.sort(key=lambda t: (t[0], t[1], t[2]))

    print("Worst cases by avg score (lower is worse):")
    for avg_score, fail_count, min_score, case_name, n in stats[:10]:
        print(
            f"- {case_name}: avg={avg_score:.3f} min={min_score:.3f} "
            f"fails={fail_count}/{n}"
        )

    worst_case_name = stats[0][3]
    prompt = prompt_by_case.get(worst_case_name)

    print("\nMost difficult user query:")
    print(prompt)
    print(f"case_name: {worst_case_name}")


if __name__ == "__main__":
    main()
