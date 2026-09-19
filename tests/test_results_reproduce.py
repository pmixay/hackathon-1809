"""Каждый закоммиченный каталог results/ пересчитывается в те же числа (`verify`) и проходит независимый пересчёт по CSV.

Организатор: повторный запуск с теми же данными даёт согласованный результат; сохранённые планы открываются повторно.
"""
import json

import pytest

from conftest import ROOT
from independent_recalc import recalc
from terraplan.cli import main

RESULT_DIRS = sorted(p.parent for p in (ROOT / "results").rglob("run_manifest.json")
                     if (p.parent / "result.json").exists() and (p.parent / "plan.json").exists())   # core export layout; EXP-07..10 use experiments/provenance.py


def _case_dir(d):
    manifest = json.loads((d / "run_manifest.json").read_text(encoding="utf-8"))
    rel = manifest.get("case_dir", "data/case")
    for cand in (d / rel, ROOT / rel):            # EXP-09 keeps its case copy inside the result directory
        if (cand / "demand.csv").exists():
            return cand
    return ROOT / "data/case"


def test_there_are_committed_results():
    assert len(RESULT_DIRS) >= 30, [str(p) for p in RESULT_DIRS]


@pytest.mark.parametrize("d", RESULT_DIRS, ids=[str(p.relative_to(ROOT)) for p in RESULT_DIRS])
def test_committed_result_dir_verifies_and_recalculates(d):
    case_dir = _case_dir(d)
    assert main(["verify", str(d), "--case", str(case_dir)]) == 0, f"verify не пройден для {d}"
    assert recalc(d, case_dir) == []
    # the saved plan reopens as a plan (organizer: save / reopen)
    assert main(["validate", "--plan", str(d / "plan.json"), "--case", str(case_dir)]) == 0
