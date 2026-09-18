"""Scenario loader: BASE, MANDATORY_STRESS (CASE_INPUT) and TEAM_* research scenarios.

A scenario changes the environment (demand multipliers, price multipliers, actual delivery shares,
loss ceiling, demand variant), never the plan. YAML layout follows the organizer's scenarios/*.yaml.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

from .case import Source


class ScenarioError(ValueError):
    """Raised for malformed scenario files (missing id, bad multipliers)."""


def _year_lookup(table: Any, year: int, default: float = 1.0) -> float:
    """table may be a number, {'default': x}, or {year: x, ...}."""
    if table is None:
        return default
    if isinstance(table, (int, float)):
        return float(table)
    if isinstance(table, dict):
        if year in table:
            return float(table[year])
        if str(year) in table:
            return float(table[str(year)])
        if "default" in table:
            return float(table["default"])
        return default
    raise ScenarioError(f"unsupported multiplier table: {table!r}")


@dataclass
class Scenario:
    scenario_id: str
    label: str = ""
    status: str = "TEAM_ASSUMPTION"
    demand_multiplier: Any = None
    critical_demand_multiplier: Any = None
    variable_price_multiplier: Any = None      # {source name/id: {year: mult}} or {'default': 1.0}
    actual_delivery_share: Any = None          # {source name/id: {year: share}} or {'default': 1.0}
    loss_ceiling: dict = field(default_factory=dict)
    demand_variant: str = "base"               # base | low | high (team sensitivity checks)
    enforce_service_thresholds: Optional[bool] = None  # None -> hard only for BASE
    notes: list = field(default_factory=list)
    changes: list = field(default_factory=list)  # human-readable list of changes vs BASE
    source_file: str = ""

    # ---- lookups -------------------------------------------------------
    def demand_mult(self, year: int) -> float:
        return _year_lookup(self.demand_multiplier, year)

    def critical_mult(self, year: int) -> float:
        tbl = self.critical_demand_multiplier if self.critical_demand_multiplier is not None else self.demand_multiplier
        return _year_lookup(tbl, year)

    def _per_source(self, table: Any, source: Source, year: int, default: float) -> float:
        if table is None:
            return default
        if isinstance(table, (int, float)):
            return float(table)
        if not isinstance(table, dict):
            raise ScenarioError(f"unsupported per-source table: {table!r}")
        for key in (source.source_id, source.name):
            if key in table:
                return _year_lookup(table[key], year, default)
        if "default" in table:
            return _year_lookup(table["default"], year, default)
        return default

    def price_mult(self, source: Source, year: int) -> float:
        return self._per_source(self.variable_price_multiplier, source, year, 1.0)

    def delivery_share(self, source: Source, year: int) -> float:
        return self._per_source(self.actual_delivery_share, source, year, 1.0)

    @property
    def loss_ceiling_enabled(self) -> bool:
        return bool(self.loss_ceiling and self.loss_ceiling.get("enabled"))

    @property
    def service_thresholds_hard(self) -> bool:
        if self.enforce_service_thresholds is not None:
            return bool(self.enforce_service_thresholds)
        return self.scenario_id == "BASE"

    def to_dict(self) -> dict:
        return {
            "scenario_id": self.scenario_id, "label": self.label, "status": self.status,
            "demand_multiplier": self.demand_multiplier, "critical_demand_multiplier": self.critical_demand_multiplier,
            "variable_price_multiplier": self.variable_price_multiplier, "actual_delivery_share": self.actual_delivery_share,
            "loss_ceiling": self.loss_ceiling, "demand_variant": self.demand_variant,
            "enforce_service_thresholds": self.enforce_service_thresholds, "notes": self.notes, "changes": self.changes,
        }


def scenario_from_dict(data: dict, source_file: str = "") -> Scenario:
    if not isinstance(data, dict):
        raise ScenarioError(f"scenario file {source_file or '<dict>'}: top level must be a mapping")
    sid = data.get("scenario_id")
    if not sid or not isinstance(sid, str):
        raise ScenarioError(f"scenario file {source_file or '<dict>'} has no 'scenario_id' (required, e.g. BASE / MANDATORY_STRESS / TEAM_xxx)")
    variant = str(data.get("demand_variant", "base")).lower()
    if variant not in ("base", "low", "high"):
        raise ScenarioError(f"scenario {sid}: demand_variant must be base|low|high, got {variant!r}")
    for key in ("demand_multiplier", "critical_demand_multiplier"):
        tbl = data.get(key)
        if isinstance(tbl, dict):
            for k, v in tbl.items():
                if not isinstance(v, (int, float)) or v < 0:
                    raise ScenarioError(f"scenario {sid}: {key}[{k}] must be a non-negative number, got {v!r}")
    lc = data.get("loss_ceiling") or {}
    if lc and lc.get("enabled") and "max_losses_divided_by_throughput" not in lc:
        raise ScenarioError(f"scenario {sid}: loss_ceiling.enabled requires max_losses_divided_by_throughput")
    return Scenario(
        scenario_id=sid, label=str(data.get("label_ru") or data.get("label") or sid),
        status=str(data.get("status", "TEAM_ASSUMPTION")),
        demand_multiplier=data.get("demand_multiplier"),
        critical_demand_multiplier=data.get("critical_demand_multiplier"),
        variable_price_multiplier=data.get("variable_price_multiplier"),
        actual_delivery_share=data.get("actual_delivery_share"),
        loss_ceiling=dict(lc), demand_variant=variant,
        enforce_service_thresholds=data.get("enforce_service_thresholds"),
        notes=list(data.get("notes") or []), changes=list(data.get("changes") or []), source_file=source_file,
    )


def load_scenario(path: str | Path) -> Scenario:
    p = Path(path)
    if not p.exists():
        raise ScenarioError(f"scenario file not found: {p}")
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ScenarioError(f"scenario file {p} is not valid YAML: {exc}") from exc
    return scenario_from_dict(data, str(p))


def resolve_scenario(spec: str, scenarios_dir: str | Path = "configs/scenarios") -> Scenario:
    """Accept a scenario id (BASE, MANDATORY_STRESS, TEAM_xxx -> <dir>/<lower>.yaml) or a file path."""
    p = Path(spec)
    if p.exists():
        return load_scenario(p)
    cand = Path(scenarios_dir) / f"{spec.lower()}.yaml"
    if cand.exists():
        return load_scenario(cand)
    raise ScenarioError(f"unknown scenario {spec!r}: not a file and {cand} does not exist")
