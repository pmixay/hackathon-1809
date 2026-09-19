"""Таблица «тонны и деньги по сторонам» должна совпадать с расчётом выбранного плана (критерий 17)."""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from common import PLANS
from terraplan.engine import simulate
from terraplan.plan import load_plan

FULL_DOC = (ROOT / "docs" / "stakeholders.md").read_text(encoding="utf-8")
# раздел со сводкой по сторонам; имена строк встречаются и в других таблицах документа
DOC = FULL_DOC.split("## Тонны и деньги по сторонам")[1].split("\n## ")[0]


NUMBER = r"\d[\d\s\u00a0]*(?:,\d+)?"


def num(text: str) -> float:
    return float(re.sub(r"[\s\u00a0]", "", text).replace(",", "."))


def numbers(text: str) -> list[float]:
    return [num(m) for m in re.findall(NUMBER, text)]


def doc_row(name: str) -> list[str]:
    match = re.search(rf"^\| {re.escape(name)} \|(.+)$", DOC, re.M)
    assert match, f"строка «{name}» отсутствует в таблице по сторонам"
    return [c.strip() for c in match.group(1).split("|")]


@pytest.fixture(scope="module")
def result(case, base, assumptions):
    return simulate(case, load_plan(PLANS / "P2z_earth_new_zbo.json"), base, assumptions)


@pytest.mark.parametrize("name, source_id", [("Поставщик Earth-Core", "A"), ("Поставщик Earth-Flex", "B"),
                                             ("Поставщик Earth-New", "C"), ("Поставщик Emergency", "E")])
def test_supplier_rows_match_the_run(result, name, source_id):
    rows = [s for s in result.source_years if s.source_id == source_id]
    delivered = sum(s.planned_delivery_t for s in rows)      # валовая отгрузка поставщика; потери возникают уже на узле
    money = sum(s.procurement_mln + s.reservation_payment_mln for s in rows)
    reservation = sum(s.reservation_payment_mln for s in rows)
    topup = sum(s.take_or_pay_topup_mln for s in rows)
    cells = doc_row(name)
    assert numbers(cells[0])[0] == pytest.approx(delivered, abs=0.001)
    assert numbers(cells[1])[0] == pytest.approx(money, abs=0.001)
    assert numbers(cells[2])[0] == pytest.approx(reservation, abs=0.001)
    assert numbers(cells[3])[0] == pytest.approx(topup, abs=0.001)


def test_consumer_rows_match_the_run(result):
    critical = doc_row("Критические потребители")[0]
    served, demand = numbers(critical)[:2]
    assert served == pytest.approx(result.kpi["served_critical_t"], abs=0.001)
    assert demand == pytest.approx(sum(y.demand_critical_t for y in result.years), abs=0.001)
    commercial = doc_row("Коммерческие потребители")[0]
    served_c, demand_c = numbers(commercial)[:2]
    assert served_c == pytest.approx(result.kpi["served_total_t"] - result.kpi["served_critical_t"], abs=0.001)
    assert demand_c == pytest.approx(sum(y.demand_total_t - y.demand_critical_t for y in result.years), abs=0.001)


def test_operator_and_financier_rows_match_the_run(result):
    operator = doc_row("Оператор узла")
    served, losses = numbers(operator[0])[:2]
    assert served == pytest.approx(result.kpi["served_total_t"], abs=0.001)
    assert losses == pytest.approx(result.kpi["losses_total_t"], abs=0.001)
    total, holding = numbers(operator[1])[:2]
    assert total == pytest.approx(result.kpi["total_cost_mln"], abs=0.001)
    assert holding == pytest.approx(sum(f.holding_mln for f in result.finance), abs=0.001)
    assert numbers(operator[2])[0] == pytest.approx(sum(s.reservation_payment_mln for s in result.source_years), abs=0.001)
    capex = numbers(doc_row("Финансирующая сторона")[1])[0]
    assert capex == pytest.approx(result.kpi["capex_total_mln"], abs=0.001)


def test_portfolio_present_value_quoted_in_the_section_matches(result):
    quoted = re.search(rf"({NUMBER}) млн PV при реальной ставке", FULL_DOC)
    assert quoted, "в разделе не указано приведённое значение затрат портфеля"
    assert num(quoted.group(1)) == pytest.approx(result.kpi["pv_cost_mln"], abs=0.001)
