"""Published artifacts, checkout EOL conversion and strict tamper detection."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from provenance import HASH_FORMAT, normalized_bytes, sha256, verify_saved


@pytest.mark.parametrize("folder", ["reverse_stress", "protection_measures", "earth_new_delay", "monte_carlo", "earth_new_delay_measures"])
def test_published_inputs_and_snapshots_are_current(root, assumptions, folder):
    # Unlike tests of fresh reports, this catches stale hashes in the delivered repo.
    report = verify_saved(root / "results" / folder)
    assert report["hash_format"] == HASH_FORMAT
    snapshots = [r["assumptions"] for r in report["runs"]] if folder in ("earth_new_delay", "earth_new_delay_measures") else [report["assumptions"]]
    for snapshot in snapshots:
        for key, value in assumptions.entries.items():
            assert snapshot[key] == value


@pytest.mark.parametrize("eol", [b"\n", b"\r\n"])
def test_published_monte_carlo_survives_clean_checkout_eol(root, tmp_path, eol):
    original = root / "results/monte_carlo"
    manifest = json.loads((original / "run_manifest.json").read_text(encoding="utf-8"))
    # Emulate Git checkout, including code and inputs, without needing git in pytest.
    paths = list(manifest["input_sha256"])
    paths += [f"results/monte_carlo/{name}" for name in manifest["output_sha256"]]
    paths.append("results/monte_carlo/run_manifest.json")
    for name in paths:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(normalized_bytes((root / name).read_bytes()).replace(b"\n", eol))
    verify_saved(tmp_path / "results/monte_carlo", root=tmp_path)
    # A real input change must not be concealed by newline normalization.
    target = tmp_path / "configs/assumptions.yaml"
    target.write_bytes(target.read_bytes().replace(b"value: 0.02", b"value: 0.03", 1))
    with pytest.raises(ValueError, match="input_sha256 mismatch: configs/assumptions.yaml"):
        verify_saved(tmp_path / "results/monte_carlo", root=tmp_path)


def test_hash_preserves_whitespace_numbers_and_unicode(tmp_path):
    path = tmp_path / "sample.txt"
    original = "Запас 8.6\nPV 83.667825\n".encode("utf-8")
    path.write_bytes(original)
    digest = sha256(path)
    for ending in (b"\r\n", b"\r"):
        path.write_bytes(original.replace(b"\n", ending))
        assert sha256(path) == digest
    for changed in (original.replace(b"8.6", b"8.5"), original + b" ", original[:-1], original.replace(b"PV", b"pv")):
        path.write_bytes(changed)
        assert sha256(path) != digest


# 2026-09-19 (ответ на аудит): refreshed after the audit fixes A3 (intra-month capacity becomes a hard
# rule) and A4 (the initial stock is stored from its actual delivery month). Every changed numeric field
# was classified before refreshing — 0 unexplained, 0 removed:
#   163  monetary value  +0.369866 mln = the preparatory-period holding of the 12.329 t opening stock
#         (0.72 x 12.329 / 2 / 12), charged to 2035, so PV and total move by the same amount;
#   103  difference of two equally shifted values: change at machine-precision level only;
#    44  checks_total / checks_passed  +6 = one INTRA_MONTH_PEAK matrix row per year of the horizon;
#    44  cost_per_served_t / pv_cost_per_served_t: derived from the holding shift;
#    44  new KPI fields prep_holding_mln / prep_holding_months.
# No previously published conclusion changes sign or ordering; see docs/audit_response.md.
@pytest.mark.parametrize("folder,expected", [
    ("reverse_stress", "1b2b83279e2f2625e278cb702342edae57fd2858ec2f95c96c0555962d71c494"),
    ("protection_measures", "f2ba86b05bc778fd90fe5ab20482db4503e0bd05f4839bed61e10512ab8f7f6b"),
    ("earth_new_delay", "98001e5ec99da4d388963d5e8db2193220f956d5a0f392ee83c39cde4c5ede7e"),
    ("monte_carlo", "9f5d0967c0b758b9f9c52b93039d756076ee3455682168e83a9baf4a424823d6"),
])
def test_audit_refresh_preserves_published_numbers(root, folder, expected):
    # Golden numeric payloads from pre-audit commit e39c679. Keep every numeric
    # field (including booleans, dates, sample counts, costs, stocks, boundaries),
    # excluding only schema metadata and the expanded assumption registries.
    def numeric(value, path=""):
        if isinstance(value, dict):
            return {p: v for k, x in value.items() if k not in {"assumptions", "schema_version"}
                    for p, v in numeric(x, path + "/" + k).items()}
        if isinstance(value, list):
            return {p: v for i, x in enumerate(value) for p, v in numeric(x, path + "/" + str(i)).items()}
        return {path: value} if isinstance(value, (int, float)) else {}
    report = json.loads((root / "results" / folder / "report.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256(json.dumps(numeric(report), sort_keys=True, allow_nan=False).encode("utf-8")).hexdigest()
    assert digest == expected
