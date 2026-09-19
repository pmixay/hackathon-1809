"""TEAM_ASSUMPTION registry: every parameter not given by the organizer, with meaning, unit, range, status.

Values are loaded from configs/assumptions.yaml; each entry may be a bare value or a mapping with
value/unit/status/range/scope/justification. `scope` names the calculation block that reads the
value, so a reader can go from an assumption to the place it changes the result. Defaults below are
used when the file does not mention a key.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .case import InputError


class AssumptionError(InputError):
    """Значение допущения вне объявленного в реестре диапазона."""

DEFAULTS: dict[str, dict[str, Any]] = {
    "discount_rate_real": dict(scope="блок 4 «Контракты и финансы»: приведение годовых потоков", value=0.08, unit="доля в год", status="TEAM_ASSUMPTION", range=[0.0, 0.20],
        justification="Реальная ставка для инфраструктуры с технологическим риском; одна ставка для всех альтернатив. Чувствительность 0–12 %."),
    "discount_t0_year": dict(scope="блок 4 «Контракты и финансы»: база приведения", value=2035, unit="год", status="TEAM_ASSUMPTION", range=[2035, 2035],
        justification="Денежные потоки — годовые суммы, датированные началом года; показатель степени PV = год − 2035."),
    "discount_timing": dict(scope="блок 4 «Контракты и финансы»: момент потока внутри года", value="start", unit="enum start|mid|end", status="TEAM_ASSUMPTION", range=["start", "mid", "end"],
        justification="Момент внутри года, к которому отнесён годовой поток: начало (степень год−2035), середина (+0,5) или конец (+1). Одинаково для всех альтернатив."),
    "prep_period_start": dict(scope="блок 2 «Календарь поставок»: самая ранняя допустимая дата заказа", value="2034-01", unit="YYYY-MM", status="TEAM_ASSUMPTION", range=["2033-01", "2034-12"],
        justification="Самый ранний месяц размещения заказа в подготовительном периоде; Earth-Core требует 12 месяцев до 2035-01."),
    "lead_time_policy": dict(scope="блок 2 «Календарь поставок»: выбор края диапазона сроков", value="max", unit="enum min|max|mean", status="TEAM_ASSUMPTION", range=["min", "max", "mean"],
        justification="Для проверок сроков используется консервативный край диапазона сроков поставки организатора."),
    "weeks_per_month": dict(scope="блок 2 «Календарь поставок»: перевод недель в месяцы", value=4.345, unit="недель", status="TEAM_ASSUMPTION", range=[4.0, 4.5],
        justification="365/12/7; сроки в неделях переводятся как ceil(недели/4,345): 6 недель -> 2 месяца."),
    "days_per_month": dict(scope="блок 2 «Календарь поставок» и проверка покрытия резерва: перевод в дни", value=30.4167, unit="дней", status="TEAM_ASSUMPTION", range=[28, 31],
        justification="365/12; сроки в днях переводятся с округлением вверх."),
    "zbo_commissioning_lag_months": dict(scope="блок 1 «Инвестиции и доступность»: месяц ввода хранилища", value=0, unit="месяцев", status="TEAM_ASSUMPTION", range=[0, 12],
        justification="Кейс не задаёт срок модернизации ZBO; она считается действующей с месяца оплаты CAPEX. Варьируется в анализе чувствительности."),
    "earth_new_post_commissioning_lead_months": dict(scope="блок 2 «Календарь поставок»: срок заказа после ввода Earth-New", value=0, unit="месяцев", status="TEAM_ASSUMPTION", range=[0, 12],
        justification="Срок Earth-New 18–24 месяца трактуется как время от решения до первой поставки; заказы размещаются в период подготовки."),
    "isru_commissioning_month": dict(scope="блок 1 «Инвестиции и доступность»: месяц ввода Lunar-ISRU", value="2038-01", unit="YYYY-MM", status="CASE_INPUT", range=["2038-01", "2038-01"],
        justification="Кейс: Lunar-ISRU доступен с 2038 года при финансировании CAPEX до 2038 года."),
    "isru_financing_deadline": dict(scope="блок 1 «Инвестиции и доступность»: предельный срок финансирования", value="2037-12", unit="YYYY-MM", status="CASE_INPUT", range=["2037-12", "2037-12"],
        justification="Кейс: CAPEX 1 250 млн должен быть профинансирован до 2038 года."),
    "source_investment_link": dict(scope="блок 1 «Инвестиции и доступность»: связь канала с инвестицией", value={"C": "EARTH_NEW", "D": "LUNAR_ISRU"}, unit="map source_id -> investment_id", status="CASE_INPUT",
        range=None, justification="Мощность Earth-New требует реализованного опциона; Lunar-ISRU — CAPEX пилотного производства."),
    "storage_investment_link": dict(scope="блок 1 «Инвестиции и доступность»: связь режима хранилища с инвестицией", value={"ZBO": "ZBO"}, unit="map investment_id -> storage_id", status="CASE_INPUT", range=None,
        justification="Модернизация ZBO переключает активный режим хранилища."),
    "emergency_base_share_threshold": dict(scope="блок 5 «Проверки»: признание Emergency базовым каналом года", value=0.20, unit="доля годового общего спроса", status="TEAM_ASSUMPTION", range=[0.1, 0.5],
        justification="Emergency считается базовым каналом в году, когда заказанный у него объём превышает эту долю спроса года."),
    "holding_cost_averaging": dict(scope="блок 3 «Помесячный баланс» и блок 4: стоимость хранения", value="trapezoid_monthly", unit="enum", status="TEAM_ASSUMPTION", range=["trapezoid_monthly"],
        justification="Средний физический запас за месяц = (I_start + I_end)/2; хранение = 0,72 × средний × 1/12."),
    "storage_capacity_check": dict(scope="блок 5 «Проверки»: ёмкость хранилища", value="end_of_month_and_intra_month_peak_hard", unit="enum", status="TEAM_ASSUMPTION", range=None,
        justification="Оба превышения ёмкости — жёсткие нарушения: запас на конец месяца и расчётный пик внутри месяца при заявленном дроблении поставок (intra_month_delivery_batches)."),
    "intra_month_delivery_batches": dict(scope="блок 3 «Помесячный баланс» и блок 5 «Проверки»: дробление месячной поставки", value=1, unit="партий в месяц", status="TEAM_ASSUMPTION", range=[1, 12],
        justification="Месячный объём канала приходит N равными партиями, равномерно распределёнными по месяцу, при равномерной выдаче. N=1 (консервативно) — одна партия в начале месяца, без допущения о внутримесячной синхронизации. Пик запаса при партии j: I_нач + (j·нетто − (j−1)·выдача)/N; проверяется как жёсткое ограничение ёмкости."),
    "emergency_reserve_equivalence": dict(scope="блок 5 «Проверки»: эквивалентность контрактного резерва физическому", value="contracted_batch_schedule_and_waiting_cover", unit="правило", status="TEAM_ASSUMPTION", range=None,
        justification="Пять условий: доступность канала, договорный срок не быстрее срока поставки, нетто-партия >= R_y, свободная зарезервированная мощность >= партия × активаций, запас покрывает спрос за время активации и исполнения."),
    "opening_stock_reservation_years": dict(scope="блок 4 «Контракты и финансы»: плата за резерв подготовительного периода", value=1.0, unit="лет", status="TEAM_ASSUMPTION", range=[0.0, 1.0],
        justification="Закупка подготовительного периода оплачивает ставку резервирования источника на купленный тоннаж за один год; учитывается в 2035 году."),
    "prep_period_holding_charged": dict(scope="блок 3 «Помесячный баланс» и блок 4: хранение начального запаса", value=True, unit="логическое", status="TEAM_ASSUMPTION", range=[True, False],
        justification="Хранение начального запаса начисляется с фактического месяца поставки до 2035-01 по тому же трапецеидальному правилу и относится на первый финансовый год."),
    "intra_year_demand_profile": dict(scope="блок 3 «Помесячный баланс»: распределение спроса внутри года", value="uniform", unit="enum", status="CASE_INPUT", range=["uniform"],
        justification="Конвенция организатора: равномерный спрос внутри года, 365 дней."),
    "undelivered_volume_paid": dict(scope="блок 4 «Контракты и финансы»: что оплачивается при недопоставке", value=True, unit="логическое", status="CASE_INPUT", range=[True, False],
        justification="Контрольное правило организатора: оплачивается заказанный объём, недопоставка в стрессе платёж не возвращает; false — только для исследовательских контрактных сценариев."),
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

    def check_ranges(self) -> None:
        """Проверить каждое значение против объявленного в реестре диапазона.

        Диапазон объявлен у большинства допущений, но раньше не проверялся: значение вне диапазона
        молча использовалось или молча приводилось к краю. Это тот же класс дефекта, что и приём
        некорректных данных CASE_INPUT, поэтому проверка сделана обязательной. Числовой диапазон
        задаётся парой [min, max], перечисление — списком допустимых значений.
        """
        problems: list[dict] = []
        for key, entry in self.entries.items():
            allowed, value = entry.get("range"), entry.get("value")
            if not allowed or not isinstance(allowed, list):
                continue
            path = f"{self.source_file or 'configs/assumptions.yaml'}: {key}"
            # Пара значений — это границы [min, max] (числа или даты ГГГГ-ММ, сравнимые лексикографически).
            # Перечисление объявляется либо в поле unit («enum ...»), либо списком другой длины,
            # либо булевыми значениями: [true, false] — это выбор, а не отрезок.
            unit = str(entry.get("unit", ""))
            is_enum = (unit.startswith("enum") or len(allowed) != 2
                       or any(isinstance(x, bool) for x in allowed)
                       or type(allowed[0]) is not type(allowed[1]))
            if is_enum:
                if value not in allowed:
                    problems.append({"path": path, "message": f"{path}: значение {value!r} вне объявленного списка допустимых {allowed}"})
                continue
            lo, hi = allowed
            if isinstance(lo, (int, float)) and not isinstance(value, (int, float)) or isinstance(value, bool):
                problems.append({"path": path, "message": f"{path}: значение {value!r} должно быть числом в диапазоне [{lo}, {hi}]"})
            elif isinstance(value, (int, float)) and not math.isfinite(float(value)):
                problems.append({"path": path, "message": f"{path}: значение должно быть конечным числом, получено {value!r}"})
            elif not (lo <= value <= hi):
                problems.append({"path": path, "message": f"{path}: значение {value!r} вне объявленного диапазона [{lo}, {hi}]"})
        if problems:
            raise AssumptionError.from_problems(problems)

    def with_overrides(self, **overrides: Any) -> "Assumptions":
        new = {k: dict(v) for k, v in self.entries.items()}
        for k, v in overrides.items():
            if k not in new:
                new[k] = dict(value=v, unit="", status="TEAM_ASSUMPTION", range=None, scope="переопределение расчёта",
                              justification="переопределение (override)")
            else:
                new[k] = dict(new[k], value=v)
        result = Assumptions(new, self.source_file)
        result.check_ranges()
        return result

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
                base = dict(entries.get(k, dict(unit="", status="TEAM_ASSUMPTION", range=None, scope="", justification="")))
                base.update(v)
                entries[k] = base
            else:
                base = dict(entries.get(k, dict(unit="", status="TEAM_ASSUMPTION", range=None, scope="", justification="")))
                base["value"] = v
                entries[k] = base
    result = Assumptions(entries, src)
    result.check_ranges()          # значение вне объявленного диапазона не должно применяться молча
    return result
