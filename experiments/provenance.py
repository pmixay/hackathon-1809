"""Portable provenance for EXP-07..10; independent of the core export format.

Only line endings are normalized. Whitespace, numbers, UTF-8 characters and the
final newline remain significant. This is NOT a semantic/rounded KPI hash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HASH_FORMAT = "sha256-utf8-lf-v1"
SCHEMA_VERSION = 2


def normalized_bytes(raw):
    return raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256(path):
    return hashlib.sha256(normalized_bytes(Path(path).read_bytes())).hexdigest()


def input_hashes(paths):
    paths = [*paths, Path(__file__)]
    return {p.relative_to(ROOT).as_posix(): sha256(p) for p in paths}


def write_text(path, text):
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def write_json(path, value):
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def verify_saved(folder, root=ROOT):
    """Validate published inputs and EXP-10 outputs, not just newly generated files."""
    folder, root = Path(folder), Path(root)
    manifest_path = folder / "run_manifest.json"
    if not manifest_path.exists():
        manifest_path = folder / "report.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("hash_format") != HASH_FORMAT or manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported provenance format: {manifest_path}")
    for field, base in (("input_sha256", root), ("output_sha256", folder)):
        for name, digest in manifest.get(field, {}).items():
            if sha256(base / name) != digest:
                raise ValueError(f"{field} mismatch: {name}")
    if manifest["experiment_id"] in ("EXP-09", "EXP-12"):
        for run in manifest["runs"]:
            for name, digest in run["case_sha256"].items():
                if sha256(folder / run["result_dir"] / "case" / name) != digest:
                    raise ValueError(f"case_sha256 mismatch: {run['result_dir']}/{name}")
            core = json.loads((folder / run["result_dir"] / "run_manifest.json").read_text(encoding="utf-8"))
            if core.get("case_file_hash_format") != HASH_FORMAT or core["case_file_sha256"] != run["case_sha256"]:
                raise ValueError(f"case-file manifest mismatch: {run['result_dir']}")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folders", nargs="*", type=Path)
    args = parser.parse_args()
    folders = args.folders or [ROOT / "results" / name for name in
                              ("reverse_stress", "protection_measures", "earth_new_delay", "monte_carlo", "earth_new_delay_measures")]
    for folder in folders:
        manifest = verify_saved(folder)
        print(f"{manifest['experiment_id']}: published inputs/artifacts PASS ({HASH_FORMAT})")


if __name__ == "__main__":
    main()
