# TerraPlan — планирование топливного снабжения орбитального узла 2035–2040

**CosmoHackathon 2026 · кейс 2 «Топливный космоконтур 2035»** · команда TerraPlan (4 участника, см. `docs/TEAM.md`)

TerraPlan — рабочий цифровой контур для оператора условного орбитального топливного узла: помесячный
материальный баланс, контракты (резервирование мощности, take-or-pay), инвестиционные опции (Earth-New,
Lunar-ISRU, ZBO), потери хранения, экономика (CAPEX/OPEX, закупка, резерв, хранение, приведённая стоимость),
проверка ограничений с указанием года, величины и причины, сравнение стандартного и обязательного стрессового
сценариев, сохранение/повторное открытие плана и выгрузка CSV/XLSX/JSON. Всё, что видит оператор и жюри
(вывод CLI, `summary.md`, тексты нарушений и ошибок, выгрузки), — на русском языке; идентификаторы правил,
имена файлов и колонок — как в форматах организатора.

*English:* TerraPlan is a Python calculation core + CLI + dict-in/dict-out API (web UI in progress) that turns operator
decisions (reservations, orders, stock policy, investments) into a monthly material balance, costs, service levels and
constraint checks for the 2035–2040 orbital-depot supply case. Everything is deterministic and reproducible.

## Быстрый старт

```bash
python -m pip install -e .                      # Python ≥ 3.10; зависимости: pyyaml, openpyxl (pytest — для тестов)
python -m pytest -q                             # 84 теста, включая контрольные примеры организатора V01–V10 и verify всех каталогов results/
python -m terraplan control-cases               # V01–V10: ПРОЙДЕН / НЕ ПРОЙДЕН
python -m terraplan run --plan configs/plans/P3_isru_zbo.json --scenario BASE             --out results/demo_BASE
python -m terraplan run --plan configs/plans/P3_isru_zbo.json --scenario MANDATORY_STRESS --out results/demo_STRESS
python -m terraplan compare results/demo_BASE results/demo_STRESS --out results/demo_compare
python -m terraplan verify results/demo_BASE           # доказательство воспроизводимости: пересчёт и сравнение с выгрузкой
python tests/independent_recalc.py results/demo_BASE    # независимый пересчёт только по CSV, без импорта движка
python experiments/run_all.py                   # EXP-01 … EXP-06, перегенерирует results/
```

Код выхода `run`: 0 — план исполним; 2 — есть жёсткие нарушения (печатаются с идентификатором правила, годом,
фактической величиной, лимитом и причиной); 3 — ошибочный ввод (сообщение называет файл, поле и значение).

Программный вызов из интерфейса или ноутбука (тот же расчётный путь, что у CLI):

```python
from terraplan.api import run_plan, compare_runs, list_scenarios, list_plans, case_summary
r = run_plan("configs/plans/P3_isru_zbo.json", "MANDATORY_STRESS")          # или словарь плана; out_dir=... для выгрузки
r["ok"], r["feasible"], r["kpi"]["pv_cost_mln"], r["violations"][0]["message"]
run_plan({"plan_id": "x", "decisions": {}}, "BASE")["error"]               # {"code": "PLAN_INVALID", "message": "... поле ... "}
```

## Порядок проверки (для жюри)

1. **Установка и запуск** — команды выше; `results/<каталог>/summary.md` показывает итоговые показатели, годовой баланс, финансы,
   инвестиции, график по источникам, полную матрицу проверок (каждое правило × год, выполненные и нарушенные) и нарушения;
   `results.xlsx` / `*.csv` / `export_envelope.json` содержат те же числа; `delivery_schedule.csv` — каждая поставка с датой
   размещения заказа, сроком поставки и пояснением.
2. **Стандартный сценарий** — `configs/plans/P3_isru_zbo.json` в `BASE` (исполним, все проверки выполнены): `results/alternatives/P3_isru_zbo_BASE/`.
3. **Обязательный стресс** — тот же план в `MANDATORY_STRESS` (`results/alternatives/P3_isru_zbo_MANDATORY_STRESS/`: RESERVE_45D нарушен в 2038–2040,
   дефицит 170 т) и адаптированный план `configs/plans/P3_isru_zbo_adapted.json` (`results/stress/P3_isru_zbo_adapted_MANDATORY_STRESS/`: исполним).
   Сравнение: `results/stress/compare_P3_isru_zbo.md`.
4. **Дополнительные тесты** — низкий/высокий спрос (`results/demand/`), свипы чувствительности и пороги (`results/sensitivity/summary.md`),
   реакция после наблюдения в стрессе (`results/reaction/`), расширяемость на копии данных с Source-X и 2041 годом (`results/extensibility/`),
   тесты ошибочного ввода и граничные тесты (`tests/`).
5. **Сравнение и выгрузка** — `results/*/summary.csv`, `results/stress/compare_*.csv`; в каждом каталоге результатов CSV + XLSX + JSON;
   планы открываются повторно: `python -m terraplan run --plan results/<каталог>/plan.json ...`; `python -m terraplan verify results/<каталог>`
   пересчитывает каталог и сравнивает с выгрузкой (в CI — для всех 34 каталогов).

Протоколы экспериментов: `experiments/README.md`. Методы и формулы: `docs/architecture.md`. Каталог правил: `docs/constraints_catalogue.md`.
Ручная проверка: `docs/manual_check.md`.

## Структура репозитория

| Путь | Содержимое |
|---|---|
| `src/terraplan/` | расчётное ядро: `case.py` (загрузка CASE_INPUT), `scenario.py`, `plan.py` (TEAM_DECISION), `assumptions.py` (реестр TEAM_ASSUMPTION), `rules.py` (формулы организатора), `engine.py` (помесячная симуляция + проверки), `planner.py` (жадный построитель плана по порядку цен), `export.py`, `compare.py`, `api.py` (словарь → словарь для интерфейса), `cli.py` |
| `data/case/` | CASE_INPUT организатора (CSV, копия `data/` справочного репозитория, только чтение) |
| `configs/scenarios/` | `base.yaml`, `mandatory_stress.yaml` (CASE_INPUT), `team_low_demand.yaml`, `team_high_demand.yaml` (чувствительность) |
| `configs/plans/` | сохранённые планы (JSON по схеме организатора) — P1…P4 и варианты, адаптированные к стрессу |
| `configs/assumptions.yaml` | каждое допущение команды: смысл, единица, статус, диапазон, обоснование |
| `experiments/` | скрипты и протоколы EXP-01…06 (`README.md`) |
| `results/` | выгрузки всех экспериментов (CSV, XLSX, JSON, `summary.md`, `run_manifest.json` с хешами) |
| `tests/` | pytest (84): V01–V10, интеграция движка, ошибочный ввод, граничные планы, расширяемость, паритет выгрузок, эталонные значения, ручная проверка, согласованность матрицы проверок и списка нарушений, календарь Earth-New, реактивные заказы и месяц наблюдения, контрактный резерв, API, `verify` + независимый пересчёт каждого каталога `results/` |
| `schemas/` | JSON-схемы организатора (план, выгрузка, сценарий, данные) |
| `docs/` | `CASE_SUMMARY.md`, `TEAM.md`, `architecture.md`, `management_note.md`, `one_pager_scenarios.md`, `stress_test_protocol.md`, `risk_register.md`, `stakeholders.md`, `roadmap_budget.md`, `sources.md`, `ui_mockups/`, `organizer/` (PDF кейса + снимок справочного репозитория), `literature/` (8 статей + конспекты), `presentation/` |

## Модель в двух словах

- Шаг — календарный месяц, 2035-01 … 2040-12 (+ подготовительный период с 2034-01 для заказов до старта). Спрос равномерен внутри года.
- `I_end = I_start + поступление − потери − выдача`; `потери = поступление × доля потерь` (один раз); дефицит показывается отдельно, запас никогда не отрицателен.
- Контракты: `Q_pay = max(заказ, TOP × резерв × доля периода)`, `плата за резерв = ставка × резерв × доля периода`; недопоставка ISRU в стрессе не возвращается.
- Инвестиции: CAPEX в дату решения; Earth-New вводится через 24 месяца после реализации опциона (консервативный край 18–24), первые поставки заказываются самим решением о реализации; ISRU с 2038-01 при оплате до 2037-12, срок заказа 2 месяца; ZBO действует с месяца оплаты CAPEX (допущение, чувствительность 0–12 месяцев).
- Затраты: закупка + резервирование + хранение (0,72 × средний запас) + постоянный OPEX + CAPEX; PV по реальной ставке 8 % (допущение, одинаково для всех альтернатив, чувствительность 0–12 %).
- Проверки по каждому году: сервис ≥ 97 % / 99 % (жёстко в BASE, ориентир в стрессе), CAPEX ≤ 1 800 до 2037 / ≤ 2 800 до 2040, 45-дневный резерв на начало года, ёмкость хранилища помесячно, мощность/резерв/доступность/срок поставки по источникам, Emergency ≤ 2 лет подряд как базовый канал, потери/поступление ≤ 2 % с 2038 в стрессе.

## Ключевые результаты (см. `results/`)

| План | PV затрат BASE, млн | Исполним в BASE | STRESS (план без изменений) | PV адаптированного к стрессу, млн |
|---|---:|:---:|---|---:|
| P1 только Earth-Core + Earth-Flex | 7 857 | нет (мощность 300 т/год < спроса 2040) | неисполним | — |
| P2z Earth-New + ZBO | 8 729 | да | 3 жёстких нарушения, дефицит 96 т | **10 097** |
| P3 ISRU + ZBO | **8 639** | да | 3 жёстких нарушения, дефицит 170 т | 10 637 |
| P4 Earth-New + ISRU + ZBO | 8 858 | да | 3 жёстких нарушения, дефицит 170 т | 10 578 |

ZBO нужна каждому плану, проходящему стресс (базовое хранилище теряет 4,5 % > потолка 2 % с 2038). План, построенный под BASE,
не имеет запаса прочности: он ломается при спросе +5 % или недопоставке ISRU 5 % (`results/sensitivity/`).
Выбор между P2z и P3 — вопрос робастности, а не цены (см. `docs/management_note.md`).

## Ограничения прототипа

Веб-интерфейс — на стадии макета (`docs/ui_mockups/index.html`, 7 экранов на русском, предпросмотр https://claude.ai/artifact/94xJiuJBULiYuiZf3BGrjp);
операции выполняются через CLI, JSON-файлы планов и `terraplan.api`. Оптимизатора нет (только жадный построитель по порядку цен).
Монте-Карло / обратный стресс и геополитический бонус-модуль запланированы (см. `docs/TEAM.md`). Секретов и внешних сервисов нет; работает офлайн.
