# results/ — генерируется командой `python experiments/run_all.py` (детерминированно; случайные числа только в EXP-10 с зерном 203510)

| Каталог | Эксперимент | Содержимое |
|---|---|---|
| `alternatives/` | EXP-01 | P1…P4 в BASE и MANDATORY_STRESS (план без изменений); `summary.csv/md` |
| `stress/` | EXP-02 | план без изменений и адаптированный план в MANDATORY_STRESS, адаптированные планы в BASE; `compare_<план>.csv/md` |
| `demand/` | EXP-03 | низкий / высокий спрос, план без изменений и перепланированный |
| `sensitivity/` | EXP-04 | `sweep_*.csv`, `thresholds.csv`, `tornado.csv`, `ranking_by_discount_rate.csv`, `summary.md` |
| `reaction/` | EXP-06 | реакция после наблюдения (Earth-Flex / Emergency после 2038-03) против плана без изменений и заблаговременной адаптации; `compare_*.md` |
| `extensibility/` | EXP-05 | `case_copy/` (Source-X, 2041) и `run/` |
| `reverse_stress/` | EXP-07 | обратный стресс адаптированного P3: граница совместного шока спроса и ISRU по 9 направлениям; `summary.md`, `report.json` |
| `protection_measures/` | EXP-08 | меры защиты P3 (запас, резерв, ранний ZBO): стоимость и радиус отказа; планы мер `*.plan.json` |
| `earth_new_delay/` | EXP-09 | задержка Earth-New 0/3/6/12 мес. для P2z: `delay_XXm/` с копией данных, `comparison.csv`, `yearly.csv` |
| `monte_carlo/` | EXP-10 | условный Монте-Карло защит P3, N = 10 000, seed 203510: `runs.csv`, `samples.csv`, `comparison.csv` |
| `geopolitical_price_shock/` | EXP-11 | ценовой шок +25 % Core/Flex 2038–2039 на копии данных: `<план>/before`, `<план>/after`, `price_overlay.csv`, `price_exposure.csv` |
| `p2z_resilience/` | EXP-12 | защита, чувствительность и обратный стресс P2z: `<мера>_delay_XXm/`, `cases/`, `comparison.csv`, `sizing.csv`, `sensitivity.csv`, `boundary.csv` |
| `earth_new_delay_measures/` | EXP-13 | меры P2z против задержки Earth-New: `delay_XXm/{none,reactive_flex,advance_buffer,advance_buffer_no_delay}/`, `comparison.csv` |
| `strategy/` | MCDA | метрики и баллы четырёх профилей; `summary.md` |

Каждый каталог расчёта: `summary.md` (на русском), `yearly_balance.csv`, `inventory_trace.csv` (помесячно), `source_schedule.csv`,
`financial_breakdown.csv`, `constraint_checks.csv` (нарушения), `constraint_matrix.csv` (каждое правило × год, включая выполненные),
`delivery_schedule.csv` (календарь заказов и поставок), `kpi.csv`, `investments.csv`, `assumptions.csv`,
`plan.json` (открывается повторно: `python -m terraplan run --plan <каталог>/plan.json ...`), `scenario.json`,
`export_envelope.json` (схема выгрузки организатора), `results.xlsx`, `run_manifest.json` (SHA-256 входов и показателей).

Проверка воспроизводимости любого каталога: `python -m terraplan verify <каталог>`; независимый пересчёт по CSV без движка:
`python tests/independent_recalc.py <каталог>`. Оба выполняются для всех каталогов в `tests/test_results_reproduce.py` и в CI.
Имена колонок CSV и идентификаторы правил — английские (форматы организатора); тексты сообщений — русские.
