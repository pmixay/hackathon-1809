import csv
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from terraplan.assumptions import load_assumptions  # noqa: E402
from terraplan.case import load_case  # noqa: E402
from terraplan.scenario import resolve_scenario  # noqa: E402


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def case():
    return load_case(ROOT / "data" / "case")


@pytest.fixture(scope="session")
def assumptions():
    return load_assumptions(ROOT / "configs" / "assumptions.yaml")


@pytest.fixture(scope="session")
def base():
    return resolve_scenario("BASE", ROOT / "configs" / "scenarios")


@pytest.fixture(scope="session")
def stress():
    return resolve_scenario("MANDATORY_STRESS", ROOT / "configs" / "scenarios")


def copy_case(tmp_path: Path, extra_source: dict | None = None, extra_demand: dict | None = None,
              extra_investment: dict | None = None, extra_constraint: dict | None = None) -> Path:
    """Copy data/case into tmp and append rows (the organizer's extensibility check works on a copy)."""
    dst = tmp_path / "case_copy"
    shutil.copytree(ROOT / "data" / "case", dst)
    for name, row in (("supply_sources.csv", extra_source), ("demand.csv", extra_demand),
                      ("investment_options.csv", extra_investment), ("constraints.csv", extra_constraint)):
        if row:
            p = dst / name
            with p.open(encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                fields = reader.fieldnames
                rows = list(reader)
            rows.append({k: str(row.get(k, "")) for k in fields})
            with p.open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                w.writerows(rows)
    return dst


SOURCE_X = dict(source_id="X", name="Source-X", capacity_t_per_year=10, variable_cost_mln_per_t=5.0,
                reservation_rate_mln_per_t_year_capacity=0.1, take_or_pay_share=0.0, lead_time_min_value=1, lead_time_max_value=1,
                lead_time_unit="month", reliability_profile="constant:0.9", available_from_year=2035, status="TEAM_ASSUMPTION",
                notes="synthetic source for extensibility check")
