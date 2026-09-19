"""Реестр рисков: машиночитаемая форма, пересчёт последствий и соответствие тексту реестра."""
import csv
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from run_risk_assessment import main as assessment_main, metric_of, recompute

REGISTER = json.loads((ROOT / "configs" / "risks.json").read_text(encoding="utf-8"))
RISKS = REGISTER["risks"]
DOC = (ROOT / "docs" / "risk_register.md").read_text(encoding="utf-8")
REQUIRED = ("risk_id", "event", "cause", "parameters", "period", "basis", "dependencies",
            "owner", "protocol", "measures", "residual", "quantification")


def test_every_risk_has_the_full_set_of_fields():
    assert len(RISKS) >= 10
    for risk in RISKS:
        missing = [f for f in REQUIRED if not risk.get(f)]
        assert not missing, f"{risk.get('risk_id')}: нет полей {missing}"
        assert risk["measures"], f"{risk['risk_id']}: не указано ни одной меры"
        for m in risk["measures"]:
            assert m["label"] and "cost_mln_pv" in m and m["effect"]
        q = risk["quantification"]
        assert q["metric"] and q["unit"] and q["label"] and q["recompute"]["kind"]
        assert isinstance(q["expected"], (int, float))


def test_risk_ids_are_unique_and_dependencies_resolve():
    ids = [r["risk_id"] for r in RISKS]
    assert len(ids) == len(set(ids))
    for risk in RISKS:
        for dep in risk["dependencies"]:
            assert dep in ids, f"{risk['risk_id']} ссылается на несуществующий риск {dep}"
            assert dep != risk["risk_id"]


def test_owners_come_from_the_declared_vocabulary():
    known = set(REGISTER["owners"])
    for risk in RISKS:
        codes = {part.strip().split()[0] for part in risk["owner"].split("/") if part.strip()}
        assert codes <= known, f"{risk['risk_id']}: владелец {risk['owner']} вне словаря {sorted(known)}"


def test_the_markdown_register_describes_the_same_risks(case):
    for risk in RISKS:
        assert f"| {risk['risk_id']} |" in DOC or f"### {risk['risk_id']}." in DOC, \
            f"{risk['risk_id']} отсутствует в тексте реестра"
        for protocol in risk["protocol"]:
            assert protocol in DOC, f"{risk['risk_id']}: протокол {protocol} не упомянут в тексте реестра"


def test_published_consequences_are_recomputed_by_the_engine(case, assumptions, base, stress):
    """Каждое число последствия пересчитывается, а не переносится в реестр вручную."""
    for risk in RISKS:
        q = risk["quantification"]
        value, how = recompute(q["recompute"], case, assumptions, base, stress)
        assert abs(value - float(q["expected"])) <= float(q.get("tolerance", 0.0)) + 1e-9, \
            f"{risk['risk_id']}: пересчитано {value}, в реестре {q['expected']}"
        assert how


def test_assessment_regenerates_the_summary_and_reports_no_mismatch():
    assert assessment_main([]) == 0
    with (ROOT / "results" / "risk_assessment.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [r["risk_id"] for r in rows] == [r["risk_id"] for r in RISKS]
    assert all(r["matches"] == "True" for r in rows)
    summary = (ROOT / "results" / "risk_assessment.md").read_text(encoding="utf-8")
    for risk in RISKS:
        assert risk["risk_id"] in summary and risk["residual"] in summary


def test_a_stale_number_in_the_register_is_detected(case, assumptions, base, stress):
    risk = dict(RISKS[1])
    q = dict(risk["quantification"])
    value, _ = recompute(q["recompute"], case, assumptions, base, stress)
    assert abs(value - (float(q["expected"]) + 10.0)) > float(q.get("tolerance", 0.0)), \
        "сдвиг на 10 единиц обязан выходить за допуск — иначе сверка ничего не ловит"


def test_unknown_metric_or_recipe_is_refused(case, assumptions, base, stress):
    with pytest.raises(KeyError):
        recompute({"kind": "wishful_thinking"}, case, assumptions, base, stress)
    res_spec = {"kind": "plan_scenario", "plan": "P2z_earth_new_zbo", "scenario": "BASE", "metric": "profit"}
    with pytest.raises(KeyError):
        recompute(res_spec, case, assumptions, base, stress)
