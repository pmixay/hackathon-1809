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


@pytest.mark.parametrize("folder,expected", [
    ("reverse_stress", "edb213fe314176dcc98f04d2dc3fb6f1a6ca73d996468d938f3ad681242811dc"),
    ("protection_measures", "e30f24595b7467e0936ec6f205901c1a9a96a3bab92c25c72ccd2d4fe6509707"),
    # 2026-09-19: refreshed after the Earth-New order-calendar fix; the only numeric change is kpi/checks_passed
    # (73 -> 75 reference, 67 -> 70 delayed runs) because LEAD_TIME_VIOLATED matrix rows of Earth-New deliveries now pass.
    ("earth_new_delay", "142fc5febb66e1a82fd03a30941ae26cb9ebe64c16c04827bb3b1c39838d67f8"),
    ("monte_carlo", "d8cf43b762a4895852025124f8e64e1bda0b02e9019e1f2a9bd73f567c1981e7"),
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
