"""Organizer control vectors V01–V10 (tests/fixtures/expected_checks.json)."""
from terraplan.control_cases import run_control_cases


def test_all_control_cases_pass(root):
    rows = run_control_cases(root / "tests" / "fixtures" / "expected_checks.json")
    assert len(rows) == 10
    failed = [r for r in rows if not r["passed"]]
    assert not failed, failed
