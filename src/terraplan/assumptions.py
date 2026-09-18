"""TEAM_ASSUMPTION registry: every parameter not given by the organizer, with meaning, unit, range, status.

Values are loaded from configs/assumptions.yaml; each entry may be a bare value or a mapping with
value/unit/status/range/justification. Defaults below are used when the file does not mention a key.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULTS: dict[str, dict[str, Any]] = {
    "discount_rate_real": dict(value=0.08, unit="доля в год", status="TEAM_ASSUMPTION", range=[0.0, 0.15],
        justification="Реальная ставка для инфраструктуры с технологическим риском; одна ставка для всех альтернатив. Чувствительность 0–12 %."),
    "discount_t0_year": dict(value=2035, unit="год", status="TEAM_ASSUMPTION", range=[2035, 2035],
        justification="Денежные потоки — годовые суммы, датированные началом года; показатель степени PV = год − 2035."),
    "discount_timing": dict(value="start", unit="enum start|mid|end", status="TEAM_ASSUMPTION", range=["start", "mid", "end"],
        justification="Момент внутри года, к которому отнесён годовой поток: начало (степень год−2035), середина (+0,5) или конец (+1). Одинаково для всех альтернатив."),
    "prep_period_start": dict(value="2034-01", unit="YYYY-MM", status="TEAM_ASSUMPTION", range=["2033-01", "2034-12"],
        justification="Самый ранний месяц размещения заказа в подготовительном периоде; Earth-Core требует 12 месяцев до 2035-01."),
    "lead_time_policy": dict(value="max", unit="enum min|max|mean", status="TEAM_ASSUMPTION", range=["min", "max", "mean"],
        justification="Для проверок сроков используется консервативный край диапазона сроков поставки организатора."),
    "weeks_per_month": dict(value=4.345, unit="недель", status="TEAM_ASSUMPTION", range=[4.0, 4.5],
        justification="365/12/7; сроки в неделях переводятся как ceil(недели/4,345): 6 недель -> 2 месяца."),
    "days_per_month": dict(value=30.4167, unit="дней", status="TEAM_ASSUMPTION", range=[28, 31],
        justification="365/12; сроки в днях переводятся с округлением вверх."),
    "zbo_commissioning_lag_months": dict(value=0, unit="месяцев", status="TEAM_ASSUMPTION", range=[0, 12],
        justification="Кейс не задаёт срок модернизации ZBO; она считается действующей с месяца оплаты CAPEX. Варьируется в анализе чувствительности."),
    "earth_new_post_commissioning_lead_months": dict(value=0, unit="месяцев", status="TEAM_ASSUMPTION", range=[0, 12],
        justification="Срок Earth-New 18–24 месяца трактуется как время от решения до первой поставки; заказы размещаются в период подготовки."),
    "isru_commissioning_month": dict(value="2038-01", unit="YYYY-MM", status="CASE_INPUT", range=["2038-01", "2038-01"],
        justification="Кейс: Lunar-ISRU доступен с 2038 года при финансировании CAPEX до 2038 года."),
    "isru_financing_deadline": dict(value="2037-12", unit="YYYY-MM", status="CASE_INPUT", range=["2037-12", "2037-12"],
        justification="Кейс: CAPEX 1 250 млн должен быть профинансирован до 2038 года."),
    "source_investment_link": dict(value={"C": "EARTH_NEW", "D": "LUNAR_ISRU"}, unit="map source_id -> investment_id", status="CASE_INPUT",
        range=None, justification="Мощность Earth-New требует реализованного опциона; Lunar-ISRU — CAPEX пилотного производства."),
    "storage_investment_link": dict(value={"ZBO": "ZBO"}, unit="map investment_id -> storage_id", status="CASE_INPUT", range=None,
        justification="Модернизация ZBO переключает активный режим хранилища."),
    "emergency_base_share_threshold": dict(value=0.20, unit="доля годового общего спроса", status="TEAM_ASSUMPTION", range=[0.1, 0.5],
        justification="Emergency считается базовым каналом в году, когда заказанный у него объём превышает эту долю спроса года."),
    "holding_cost_averaging": dict(value="trapezoid_monthly", unit="enum", status="TEAM_ASSUMPTION", range=["trapezoid_monthly"],
        justification="Средний физический запас за месяц = (I_start + I_end)/2; хранение = 0,72 × средний × 1/12."),
    "storage_capacity_check": dict(value="end_of_month_hard_peak_warning", unit="enum", status="TEAM_ASSUMPTION", range=None,
        justification="Жёсткое нарушение, если запас на конец месяца > ёмкости; предупреждение, если запас после поступления и до выдачи превышает ёмкость."),
    "emergency_reserve_equivalence": dict(value="stock_covers_lead_time_and_reserved_capacity_covers_45d", unit="правило", status="TEAM_ASSUMPTION", range=None,
        justification="Контрактный резерв засчитывается, только если физический запас покрывает спрос за 6 недель срока поставки Emergency и зарезервированная мощность Emergency >= R_y."),
    "opening_stock_reservation_years": dict(value=1.0, unit="лет", status="TEAM_ASSUMPTION", range=[0.0, 1.0],
        justification="Закупка подготовительного периода оплачивает ставку резервирования источника на купленный тоннаж за один год; учитывается в 2035 году."),
    "prep_period_holding_charged": dict(value=False, unit="логическое", status="TEAM_ASSUMPTION", range=[True, False],
        justification="Хранение начисляется с 2035-01; время хранения в подготовительном периоде не оплачивается (несущественно, < 1 месяца)."),
    "intra_year_demand_profile": dict(value="uniform", unit="enum", status="CASE_INPUT", range=["uniform"],
        justification="Конвенция организатора: равномерный спрос внутри года, 365 дней."),
}


@dataclass
class Assumptions:
    entries: dict[str, dict[str, Any]] = field(default_factory=dict)
    source_file: str = ""

    def __getattr__(self, key: str) -> Any:
        entries = self.__dict__.get("entries", {})
        if key in entries:
            return entries[key]["value"]
        raise AttributeError(key)

    def get(self, key: str, default: Any = None) -> Any:
        return self.entries[key]["value"] if key in self.entries else default

    def with_overrides(self, **overrides: Any) -> "Assumptions":
        new = {k: dict(v) for k, v in self.entries.items()}
        for k, v in overrides.items():
            if k not in new:
                new[k] = dict(value=v, unit="", status="TEAM_ASSUMPTION", range=None, justification="переопределение (override)")
            else:
                new[k] = dict(new[k], value=v)
        return Assumptions(new, self.source_file)

    def table(self) -> list[dict[str, Any]]:
        return [dict(key=k, **v) for k, v in self.entries.items()]

    def to_dict(self) -> dict[str, Any]:
        return {k: dict(v) for k, v in self.entries.items()}


def load_assumptions(path: str | Path | None = None) -> Assumptions:
    entries = {k: dict(v) for k, v in DEFAULTS.items()}
    src = ""
    if path is not None and Path(path).exists():
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        src = str(path)
        for k, v in data.items():
            if isinstance(v, dict) and "value" in v:
                base = dict(entries.get(k, dict(unit="", status="TEAM_ASSUMPTION", range=None, justification="")))
                base.update(v)
                entries[k] = base
            else:
                base = dict(entries.get(k, dict(unit="", status="TEAM_ASSUMPTION", range=None, justification="")))
                base["value"] = v
                entries[k] = base
    return Assumptions(entries, src)
