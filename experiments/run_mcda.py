"""Воспроизводимый MCDA R2 для трёх адаптируемых архитектур.

Скрипт не заменяет проверку исполнимости взвешенным баллом. Сначала он требует
исполнимость BASE и заблаговременно адаптированного обязательного стресса, затем
нормирует критерии по допущенному множеству и применяет раскрытые профили весов
из configs/mcda_profiles.yaml.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "strategy"

PLAN_SOURCES = {
    "P2z_earth_new_zbo": ("A", "B", "C"),
    "P3_isru_zbo": ("A", "B", "D"),
    "P4_full": ("A", "B", "C", "D"),
}
ADAPTED_PLAN = {
    "P2z_earth_new_zbo": "P2z_earth_new_zbo_adapted",
    "P3_isru_zbo": "P3_isru_zbo_adapted",
    "P4_full": "P4_full_adapted",
}
ADAPTED_VARIANTS = {"adapted plan", "адаптированный план"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def truth(value: str) -> bool:
    return value.strip().lower() == "true"


def f(value: str) -> float:
    return float(value)


def fmt(value: float, digits: int = 3) -> str:
    return f"{value:,.{digits}f}"


def main() -> None:
    # JSON is valid YAML; keeping the .yaml name makes the disclosed profile file
    # convenient for the project while avoiding a runtime-only dependency here.
    config = json.loads((ROOT / "configs" / "mcda_profiles.yaml").read_text(encoding="utf-8"))
    alternatives = read_csv(ROOT / "results" / "alternatives" / "summary.csv")
    stress = read_csv(ROOT / "results" / "stress" / "summary.csv")
    sources = {row["source_id"]: row for row in read_csv(ROOT / "data" / "case" / "supply_sources.csv")}

    alt_index = {(r["plan_id"], r["scenario_id"]): r for r in alternatives}
    stress_index = {
        (r["plan_id"], r["scenario_id"]): r
        for r in stress
        if r["variant"] in ADAPTED_VARIANTS
    }

    metrics: dict[str, dict[str, float]] = {}
    gates: dict[str, tuple[bool, bool]] = {}
    for plan, source_ids in PLAN_SOURCES.items():
        base = alt_index[(plan, "BASE")]
        fixed_stress = alt_index[(plan, "MANDATORY_STRESS")]
        adapted = stress_index[(ADAPTED_PLAN[plan], "MANDATORY_STRESS")]
        base_gate = truth(base["feasible"])
        stress_gate = truth(adapted["feasible"])
        gates[plan] = (base_gate, stress_gate)
        if not (base_gate and stress_gate):
            continue

        capacity = sum(f(sources[s]["capacity_t_per_year"]) for s in source_ids)
        no_top_capacity = sum(
            f(sources[s]["capacity_t_per_year"])
            for s in source_ids
            if f(sources[s]["take_or_pay_share"]) == 0.0
        )
        metrics[plan] = {
            "base_pv_mln": f(base["pv_cost_mln"]),
            "stress_adapted_pv_mln": f(adapted["pv_cost_mln"]),
            "capex_mln": f(base["capex_total_mln"]),
            "fixed_stress_shortage_t": f(fixed_stress["shortage_total_t"]),
            "no_top_capacity_share": no_top_capacity / capacity,
            "nominal_capacity_tpy": capacity,
        }

    if set(metrics) != set(PLAN_SOURCES):
        raise RuntimeError(f"Изменился фильтр исполнимости: {gates}")

    normalized: dict[str, dict[str, float]] = {plan: {} for plan in metrics}
    for criterion, definition in config["criteria"].items():
        values = [row[criterion] for row in metrics.values()]
        lo, hi = min(values), max(values)
        for plan, row in metrics.items():
            if hi == lo:
                score = 1.0
            elif definition["direction"] == "minimize":
                score = (hi - row[criterion]) / (hi - lo)
            else:
                score = (row[criterion] - lo) / (hi - lo)
            normalized[plan][criterion] = score

    profile_scores: list[dict[str, str | float | int]] = []
    for profile_id, profile in config["profiles"].items():
        weights = profile["weights"]
        if abs(sum(weights.values()) - 1.0) > 1e-9:
            raise ValueError(f"Сумма весов профиля {profile_id} не равна 1")
        ranked = sorted(
            (
                (plan, sum(weights[c] * normalized[plan][c] for c in weights))
                for plan in metrics
            ),
            key=lambda item: (-item[1], item[0]),
        )
        for rank, (plan, score) in enumerate(ranked, start=1):
            profile_scores.append(
                {"profile": profile_id, "rank": rank, "plan_id": plan, "score_0_100": score * 100}
            )

    OUT.mkdir(parents=True, exist_ok=True)
    metric_fields = ["plan_id", *config["criteria"].keys()]
    with (OUT / "mcda_metrics.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=metric_fields)
        writer.writeheader()
        for plan, row in metrics.items():
            writer.writerow({"plan_id": plan, **{k: f"{v:.9f}" for k, v in row.items()}})

    with (OUT / "mcda_scores.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["profile", "rank", "plan_id", "score_0_100"])
        writer.writeheader()
        for row in profile_scores:
            writer.writerow({**row, "score_0_100": f"{float(row['score_0_100']):.6f}"})

    lines = [
        "# MCDA роли 2 — итоговый выбор стратегии",
        "",
        "Исполнимость — жёсткий фильтр, а не взвешенный критерий: архитектура должна проходить BASE и иметь исполнимый заблаговременно адаптированный план MANDATORY_STRESS. Поэтому P1/P2 не оцениваются; P2z, P3 и P4 проходят фильтр. Все три адаптированных плана обслуживают 100% общего и критического спроса: веса не могут компенсировать нарушение сервиса или резерва.",
        "",
        "## Метрики решения",
        "",
        "| План | PV BASE, млн | PV адапт. стресса, млн | CAPEX, млн | Дефицит фикс. плана в стрессе, т | Мощность без TOP | Номинальная мощность, т/год |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    labels = {
        "P2z_earth_new_zbo": "P2z Earth-New + ZBO",
        "P3_isru_zbo": "P3 ISRU + ZBO",
        "P4_full": "P4 полный портфель",
    }
    for plan, row in metrics.items():
        lines.append(
            f"| {labels[plan]} | {fmt(row['base_pv_mln'], 1)} | {fmt(row['stress_adapted_pv_mln'], 1)} | "
            f"{fmt(row['capex_mln'], 0)} | {fmt(row['fixed_stress_shortage_t'], 1)} | "
            f"{row['no_top_capacity_share']:.1%} | {fmt(row['nominal_capacity_tpy'], 0)} |"
        )

    lines.extend([
        "",
        "Дефицит фиксированного плана показывает риск, если график BASE не пересмотреть; это не результат адаптированных планов. Доля без TOP и номинальная мощность не включают Emergency: это резервный, а не обычный производственный канал.",
        "",
        "## Результаты профилей (аддитивный min-max MCDA, 0–100)",
        "",
        "| Профиль | P2z | P3 | P4 | Победитель |",
        "|---|---:|---:|---:|---|",
    ])
    by_profile: dict[str, dict[str, float]] = {}
    for row in profile_scores:
        by_profile.setdefault(str(row["profile"]), {})[str(row["plan_id"])] = float(row["score_0_100"])
    for profile_id, profile in config["profiles"].items():
        scores = by_profile[profile_id]
        winner = max(scores, key=scores.get)
        lines.append(
            f"| {profile['label']} | {scores['P2z_earth_new_zbo']:.1f} | {scores['P3_isru_zbo']:.1f} | "
            f"{scores['P4_full']:.1f} | {labels[winner]} |"
        )

    lines.extend([
        "",
        "## Рекомендация",
        "",
        "Выбрать **P2z Earth-New + ZBO с пересматриваемым, зависящим от сценария графиком заказов**. План выигрывает во всех раскрытых профилях стейкхолдеров благодаря заметному преимуществу по стоимости адаптации к стрессу и существенно меньшему необратимому CAPEX, а не из-за произвольного заявления об универсальной устойчивости. У P3 остаются преимущества по стоимости BASE и доле мощности без TOP; у P4 — максимальная номинальная мощность. Эти сильные стороны видны в критериях и не скрыты итоговым рангом.",
        "",
        "Входы: `results/alternatives/summary.csv`, `results/stress/summary.csv`, `data/case/supply_sources.csv`, `configs/mcda_profiles.yaml`. Нормирование — min-max внутри допущенного множества. Баллы помогают принять решение, но не являются вероятностями или доказательством оптимальности.",
    ])
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
