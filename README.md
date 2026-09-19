# TerraPlan — планирование топливного снабжения орбитального узла 2035–2040

**CosmoHackathon 2026 · кейс 2 «Топливный космоконтур 2035»** · команда TerraPlan (4 участника, см. `docs/TEAM.md`)

TerraPlan — рабочий цифровой контур для оператора условного орбитального топливного узла: помесячный
материальный баланс, контракты (резервирование мощности, take-or-pay), инвестиционные опции (Earth-New,
Lunar-ISRU, ZBO), потери хранения, экономика (CAPEX/OPEX, закупка, резерв, хранение, приведённая стоимость),
проверка ограничений с указанием года, величины и причины, сравнение стандартного и обязательного стрессового
сценариев, сохранение/повторное открытие плана и выгрузка CSV/XLSX/JSON. Всё, что видит оператор и жюри
(вывод CLI, `summary.md`, тексты нарушений и ошибок, выгрузки), — на русском языке; идентификаторы правил,
имена файлов и колонок — как в форматах организатора.

*English:* TerraPlan is a Python calculation core + CLI + dict-in/dict-out API + local browser UI that turns operator
decisions (reservations, orders, stock policy, investments) into a monthly material balance, costs, service levels and
constraint checks for the 2035–2040 orbital-depot supply case. Everything is deterministic and reproducible.

## Быстрый старт

```bash
python -m pip install -e ".[dev]"                # Python ≥ 3.10; pyyaml, openpyxl, pytest
python -m terraplan ui                          # интерфейс оператора: http://127.0.0.1:8765, остановка Ctrl+C
python -m pytest -q                             # 167 тестов, включая контрольные примеры организатора V01–V10 и verify всех каталогов results/
python -m terraplan control-cases               # V01–V10: ПРОЙДЕН / НЕ ПРОЙДЕН
python -m terraplan run --plan configs/plans/P2z_earth_new_zbo.json --scenario BASE             --out results/demo_BASE
python -m terraplan run --plan configs/plans/P2z_earth_new_zbo.json --scenario MANDATORY_STRESS --out results/demo_STRESS
python -m terraplan compare results/demo_BASE results/demo_STRESS --out results/demo_compare
python -m terraplan verify results/demo_BASE           # доказательство воспроизводимости: пересчёт и сравнение с выгрузкой
python tests/independent_recalc.py results/demo_BASE    # независимый пересчёт только по CSV, без импорта движка
python experiments/run_all.py                   # EXP-01 … EXP-10, перегенерирует results/ (EXP-10 — с фиксированным seed)
python experiments/run_mcda.py                  # ранжирование стратегий R2 и четыре профиля стейкхолдеров
```

Код выхода `run`: 0 — план исполним; 2 — есть жёсткие нарушения (печатаются с идентификатором правила, годом,
фактической величиной, лимитом и причиной); 3 — ошибочный ввод (сообщение называет файл, поле и значение).

Интерфейс в браузере работает офлайн после установки: правка заказов, резервирований, инвестиций, начального запаса и параметров
контрактов на копии данных; расчёт, просмотр нарушений, закрепление расчёта A и сравнение с B; сохранение/открытие рабочего JSON и
выгрузка CSV/XLSX/JSON. Пошаговая демонстрация: [docs/operator_guide.md](docs/operator_guide.md). Презентация:
[12 слайдов PowerPoint](docs/presentation/TerraPlan.pptx). Передача и оставшийся шаг публикации: [docs/HANDOVER.md](docs/HANDOVER.md).

Программный вызов из интерфейса или ноутбука (тот же расчётный путь, что у CLI):

```python
from terraplan.api import run_plan, compare_runs, list_scenarios, list_plans, case_summary
r = run_plan("configs/plans/P2z_earth_new_zbo.json", "MANDATORY_STRESS")   # или словарь плана; out_dir=... для выгрузки
r["ok"], r["feasible"], r["kpi"]["pv_cost_mln"], r["violations"][0]["message"]
run_plan({"plan_id": "x", "decisions": {}}, "BASE")["error"]               # {"code": "PLAN_INVALID", "message": "... поле ... "}
```

## Порядок проверки (для жюри)

1. **Установка и запуск** — команды выше; `results/<каталог>/summary.md` показывает итоговые показатели, годовой баланс, финансы,
   инвестиции, график по источникам, полную матрицу проверок (каждое правило × год, выполненные и нарушенные) и нарушения;
   `results.xlsx` / `*.csv` / `export_envelope.json` содержат те же числа; `delivery_schedule.csv` — каждая поставка с датой
   размещения заказа, сроком поставки и пояснением.
2. **Выбранная стратегия в BASE** — `configs/plans/P2z_earth_new_zbo.json` (исполнима, все проверки выполнены): `results/alternatives/P2z_earth_new_zbo_BASE/`.
3. **Обязательный стресс** — тот же P2z без изменения заказов (`results/alternatives/P2z_earth_new_zbo_MANDATORY_STRESS/`: RESERVE_45D нарушен в 2038–2040,
   дефицит 95,917 т) и заблаговременно адаптированный `configs/plans/P2z_earth_new_zbo_adapted.json`
   (`results/stress/P2z_earth_new_zbo_adapted_MANDATORY_STRESS/`: исполним, дефицит 0). Сравнение: `results/stress/compare_P2z_earth_new_zbo.md`.
4. **Дополнительные тесты** — низкий/высокий спрос (`results/demand/`), свипы чувствительности и пороги (`results/sensitivity/summary.md`),
   реакция после наблюдения в стрессе (`results/reaction/`), обратный стресс, защитные меры, задержка Earth-New и Монте-Карло с seed
   (EXP-07–10: `results/reverse_stress/`, `results/protection_measures/`, `results/earth_new_delay/`, `results/monte_carlo/`),
   расширяемость на копии данных с Source-X и 2041 годом (`results/extensibility/`), тесты ошибочного ввода и граничные тесты (`tests/`).
5. **Сравнение и выгрузка** — `results/*/summary.csv`, `results/stress/compare_*.csv`; в каждом каталоге результатов CSV + XLSX + JSON;
   планы открываются повторно: `python -m terraplan run --plan results/<каталог>/plan.json ...`; `python -m terraplan verify results/<каталог>`
   пересчитывает каталог и сравнивает с выгрузкой (в тестах и CI — для всех 38 каталогов результатов, включая EXP-09).

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
| `experiments/` | скрипты и протоколы EXP-01…10 (`README.md`), переносимая провенанс-проверка `provenance.py` |
| `results/` | выгрузки всех экспериментов (CSV, XLSX, JSON, `summary.md`, `run_manifest.json` с хешами) |
| `tests/` | pytest (167): V01–V10, интеграция движка, ошибочный ввод, граничные планы, расширяемость, паритет выгрузок, эталонные значения, ручная проверка, согласованность матрицы проверок и списка нарушений, календарь Earth-New, реактивные заказы и месяц наблюдения, контрактный резерв, API, `verify` + независимый пересчёт каждого каталога `results/` |
| `schemas/` | JSON-схемы организатора (план, выгрузка, сценарий, данные) |
| `docs/` | `CASE_SUMMARY.md`, `TEAM.md`, `architecture.md`, `management_note.md`, `one_pager_scenarios.md`, `stress_test_protocol.md`, `risk_register.md`, `stakeholders.md`, `roadmap_budget.md`, `sources.md`, `operator_guide.md`, `HANDOVER.md`, `ui_mockups/` (исторический макет), `organizer/` (PDF кейса + снимок справочного репозитория), `literature/` (8 статей + конспекты), `presentation/` (`TerraPlan.pptx`, 12 слайдов) |

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

ZBO нужна для соблюдения годового стрессового потолка потерь при продолжении поставок (базовое хранилище теряет 4,5 % > 2 %);
ввод до 2038 — консервативная цель, движок проверяет годовое отношение потерь к поступлению. Для плана P3 без изменений спрос +5 %
и недопоставка ISRU 5 % — первые неуспешные точки сетки, а не точные границы (`results/sensitivity/`). Планы, адаптированные к стрессу,
в BASE переполняют хранилище (17/25/25 жёстких нарушений у P2z/P3/P4); универсальная робастная политика не продемонстрирована.
**Итоговый выбор для защиты — P2z с пересматриваемым, зависящим от сценария графиком заказов.**
Он дороже P3 в BASE на 90,547 млн PV, но дешевле адаптированного P3 в обязательном стрессе на
539,183 млн PV и требует на 890 млн меньше CAPEX. Воспроизводимый MCDA: `results/strategy/`;
распределение договорных рисков: `docs/contract_strategy.md`; критерии стейкхолдеров 17–18:
`docs/stakeholders.md`. Выбор ограничен горизонтом 2035–2040 и не означает, что один фиксированный
заказной план проходит оба сценария (см. `docs/management_note.md`).

## Ограничения прототипа

Веб-интерфейс запускается командой `python -m terraplan ui` (`docs/ui_mockups/` — исторический макет); он обслуживает одного локального
оператора, хранит последние 12 расчётов до остановки сервера и сохраняет работу через скачиваемые файлы. Публикация на GitVerse ожидает
адрес репозитория команды; настроенный origin — GitHub. Оптимизатора нет (только жадный построитель по порядку цен). Обратный стресс,
защитные меры, задержка Earth-New и Монте-Карло с seed реализованы в EXP-07–10; их распределения остаются TEAM_ASSUMPTION.
Геополитический бонус-модуль запланирован. Секретов и внешних сервисов нет; работает офлайн.
