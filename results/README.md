# results/ — генерируется командой `python experiments/run_all.py` (детерминированно, без случайных чисел)

| Каталог | Эксперимент | Содержимое |
|---|---|---|
| `alternatives/` | EXP-01 | P1…P4 в BASE и MANDATORY_STRESS (план без изменений); `summary.csv/md` |
| `stress/` | EXP-02 | план без изменений и адаптированный план в MANDATORY_STRESS, адаптированные планы в BASE; `compare_<план>.csv/md` |
| `demand/` | EXP-03 | низкий / высокий спрос, план без изменений и перепланированный |
| `sensitivity/` | EXP-04 | `sweep_*.csv`, `thresholds.csv`, `tornado.csv`, `ranking_by_discount_rate.csv`, `summary.md` |
| `reaction/` | EXP-06 | реакция после наблюдения (Earth-Flex / Emergency после 2038-03) против плана без изменений и заблаговременной адаптации; `compare_*.md` |
| `extensibility/` | EXP-05 | `case_copy/` (Source-X, 2041) и `run/` |

Каждый каталог расчёта: `summary.md` (на русском), `yearly_balance.csv`, `inventory_trace.csv` (помесячно), `source_schedule.csv`,
`financial_breakdown.csv`, `constraint_checks.csv` (нарушения), `constraint_matrix.csv` (каждое правило × год, включая выполненные),
`delivery_schedule.csv` (календарь заказов и поставок), `kpi.csv`, `investments.csv`, `assumptions.csv`,
`plan.json` (открывается повторно: `python -m terraplan run --plan <каталог>/plan.json ...`), `scenario.json`,
`export_envelope.json` (схема выгрузки организатора), `results.xlsx`, `run_manifest.json` (SHA-256 входов и показателей).

Проверка воспроизводимости любого каталога: `python -m terraplan verify <каталог>`; независимый пересчёт по CSV без движка:
`python tests/independent_recalc.py <каталог>`. Оба выполняются для всех каталогов в `tests/test_results_reproduce.py` и в CI.
Имена колонок CSV и идентификаторы правил — английские (форматы организатора); тексты сообщений — русские.
