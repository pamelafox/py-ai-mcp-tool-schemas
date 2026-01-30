"""Analyze how often spanish_* eval cases fail across runs.

This is a small helper script for quickly answering:
- Which Spanish cases fail most often?
- Do any ever fail without add_expense_cat_a?

Pass/fail is defined as overall_score >= 0.8 (consistent with other quick analyses
used in this repo).
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


RUNS: list[tuple[str, Path]] = [
    ("gpt52_none", Path("evals/runs/gpt52_none/results.json")),
    ("gpt52_xhigh", Path("evals/runs/gpt52_xhigh/results.json")),
    ("gpt41mini", Path("evals/runs/gpt41mini/results.json")),
]

SPANISH_PREFIX = "spanish_"
PASS_THRESHOLD = 0.8


@dataclass(frozen=True)
class CaseStats:
    total: int
    failed: int
    variant_fail_counts: Counter[str]
    eval_fail_counts: Counter[str]

    @property
    def fail_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.failed / self.total


def load_rows(path: Path) -> list[dict]:
    return json.loads(path.read_text()).get("results", [])


def is_pass(row: dict) -> bool:
    return float(row.get("overall_score") or 0.0) >= PASS_THRESHOLD


def summarize(rows: list[dict], *, include_cat_a: bool) -> dict[str, CaseStats]:
    by_case: dict[str, list[dict]] = defaultdict(list)

    for row in rows:
        case = row.get("case_name")
        if not isinstance(case, str) or not case.startswith(SPANISH_PREFIX):
            continue
        if not include_cat_a and row.get("tool_variant") == "add_expense_cat_a":
            continue
        by_case[case].append(row)

    out: dict[str, CaseStats] = {}
    for case, case_rows in by_case.items():
        failed_rows = [r for r in case_rows if not is_pass(r)]

        variant_fail_counts = Counter(str(r.get("tool_variant")) for r in failed_rows)

        eval_fail_counts: Counter[str] = Counter()
        for row in failed_rows:
            eval_results = row.get("eval_results") or {}
            for eval_name, eval_result in eval_results.items():
                if eval_result and eval_result.get("passed") is False:
                    eval_fail_counts[str(eval_name)] += 1

        out[case] = CaseStats(
            total=len(case_rows),
            failed=len(failed_rows),
            variant_fail_counts=variant_fail_counts,
            eval_fail_counts=eval_fail_counts,
        )

    return out


def print_report(title: str, per_run: dict[str, dict[str, CaseStats]]) -> None:
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)

    cases = sorted({case for run_stats in per_run.values() for case in run_stats.keys()})
    if not cases:
        print("No spanish_* cases found.")
        return

    combined: dict[str, tuple[int, int, float]] = {}
    for case in cases:
        total = sum(per_run[run].get(case, CaseStats(0, 0, Counter(), Counter())).total for run in per_run)
        failed = sum(per_run[run].get(case, CaseStats(0, 0, Counter(), Counter())).failed for run in per_run)
        combined[case] = (failed, total, (failed / total) if total else 0.0)

    print("Overall (across runs):")
    for case, (failed, total, rate) in sorted(combined.items(), key=lambda x: (-x[1][2], -x[1][0], x[0])):
        print(f"- {case}: {failed}/{total} failed ({rate*100:.1f}%)")

    for run_name, stats in per_run.items():
        print("\n" + run_name)
        if not stats:
            print("- (no spanish_* rows)")
            continue

        for case, s in sorted(stats.items(), key=lambda x: (-x[1].fail_rate, -x[1].failed, x[0])):
            extra = ""
            if s.failed:
                top_variants = ", ".join(f"{v}({n})" for v, n in s.variant_fail_counts.most_common(3))
                top_evals = ", ".join(f"{e}({n})" for e, n in s.eval_fail_counts.most_common(3))
                if top_variants:
                    extra += " | variants: " + top_variants
                if top_evals:
                    extra += " | evals: " + top_evals
            print(f"- {case}: {s.failed}/{s.total} ({s.fail_rate*100:.1f}%)" + extra)


def main() -> None:
    rows_by_run = {name: load_rows(path) for name, path in RUNS}

    per_run_all = {run: summarize(rows, include_cat_a=True) for run, rows in rows_by_run.items()}
    print_report("Spanish cases — including add_expense_cat_a", per_run_all)

    per_run_no_a = {run: summarize(rows, include_cat_a=False) for run, rows in rows_by_run.items()}
    print_report("Spanish cases — excluding add_expense_cat_a", per_run_no_a)


if __name__ == "__main__":
    main()
