# P3_isru_zbo_team_high_demand — TEAM_HIGH_DEMAND (Высокий спрос (проверка чувствительности, данные организатора))

План исполним: **ДА** — жёстких нарушений: 0, отклонений от ориентиров: 0, предупреждений: 0

Единицы: топливо — т; деньги — млн у.е. в постоянных ценах 2035 г.; шаг расчёта — календарный месяц; ставка дисконтирования r = 8% (TEAM_ASSUMPTION, одинакова для всех альтернатив). Те же числа — в CSV/XLSX/JSON этого каталога; календарь заказов и поставок — `delivery_schedule.csv`; реестр допущений — `assumptions.csv`.

## Итоговые показатели

| Показатель | Ключ | Значение |
|---|---|---:|
| Полные затраты, млн | `total_cost_mln` | 12,577.031 |
| Приведённые затраты (PV), млн | `pv_cost_mln` | 10,142.465 |
| Затраты на обслуженную тонну, млн/т | `cost_per_served_t_mln` | 7.574 |
| PV затрат на обслуженную тонну, млн/т | `pv_cost_per_served_t_mln` | 6.108 |
| Обслужено, т | `served_total_t` | 1,660.563 |
| Спрос, т | `demand_total_t` | 1,673.000 |
| Дефицит, т | `shortage_total_t` | 12.437 |
| Дефицит критического спроса, т | `shortage_critical_t` | 0.000 |
| Мин. уровень сервиса (общий) | `min_service_level_total` | 0.974 |
| Мин. уровень сервиса (критический) | `min_service_level_critical` | 1.000 |
| Потери при хранении, т | `losses_total_t` | 33.476 |
| CAPEX, млн | `capex_total_mln` | 1,430.000 |
| Закупка, млн | `procurement_total_mln` | 10,243.742 |
| Резервирование мощности, млн | `reservation_total_mln` | 517.968 |
| Хранение, млн | `holding_total_mln` | 133.320 |
| Постоянный OPEX, млн | `fixed_opex_total_mln` | 252.000 |
| Оплачено по take-or-pay сверх заказа, т | `take_or_pay_idle_t` | 0.000 |
| Премия take-or-pay (оплата незаказанного объёма), млн | `take_or_pay_topup_mln` | 0.000 |

## Годовой баланс (т)

| Год | Спрос | в т.ч. критич. | Обслужено | УС общий | УС критич. | Дефицит | Поступление (факт) | Потери | Запас на начало | Запас на конец | R45 | Резерв на начало года | Хранилище |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 110.0 | 88.0 | 110.0 | 1.000 | 1.000 | 0.0 | 120.9 | 5.44 | 13.6 | 19.0 | 13.6 | выполнен | BASE |
| 2036 | 154.0 | 115.5 | 154.0 | 1.000 | 1.000 | 0.0 | 168.4 | 7.58 | 19.0 | 25.8 | 19.0 | выполнен | BASE |
| 2037 | 209.0 | 148.5 | 209.0 | 1.000 | 1.000 | 0.0 | 228.3 | 6.51 | 25.8 | 38.5 | 25.8 | выполнен | ZBO |
| 2038 | 312.5 | 212.5 | 312.5 | 1.000 | 1.000 | 0.0 | 327.2 | 3.93 | 38.5 | 49.3 | 38.5 | выполнен | ZBO |
| 2039 | 400.0 | 262.5 | 400.0 | 1.000 | 1.000 | 0.0 | 415.8 | 4.99 | 49.3 | 60.1 | 49.3 | выполнен | ZBO |
| 2040 | 487.5 | 312.5 | 475.1 | 0.974 | 1.000 | 12.4 | 420.0 | 5.04 | 60.1 | 0.0 | 60.1 | выполнен | ZBO |

УС — уровень сервиса (обслужено / спрос); R45 — 45-дневный резерв `D_y × 45 / 365`, проверяется по физическому запасу на начало года.

## Финансы (млн у.е., постоянные цены 2035 г.)

| Год | Закупка | в т.ч. премия TOP | Резервирование | Хранение | Пост. OPEX | CAPEX | Итого | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 875.7 | 0.0 | 56.5 | 11.7 | 0.0 | 0.0 | 944.0 | 944.0 |
| 2036 | 1043.8 | 0.0 | 75.8 | 16.1 | 0.0 | 1250.0 | 2385.7 | 2209.0 |
| 2037 | 1518.6 | 0.0 | 91.2 | 22.5 | 6.0 | 180.0 | 1818.3 | 1558.9 |
| 2038 | 1809.2 | 0.0 | 91.1 | 25.7 | 82.0 | 0.0 | 2008.0 | 1594.0 |
| 2039 | 2479.4 | 0.0 | 101.4 | 39.4 | 82.0 | 0.0 | 2702.2 | 1986.2 |
| 2040 | 2517.0 | 0.0 | 102.0 | 17.9 | 82.0 | 0.0 | 2718.9 | 1850.5 |

«Премия TOP» — часть строки «Закупка», оплаченная за объём сверх заказанного по условию take-or-pay; это разложение платежа, а не дополнительный платёж.

## Инвестиции

| Инвестиция | Плата за опцион, млн | Дата опциона | Реализация / CAPEX, млн | Дата решения | Ввод в строй | Пост. OPEX, млн/год | Примечание |
|---|---:|---|---:|---|---|---:|---|
| Lunar-ISRU pilot (LUNAR_ISRU) | 0 | — | 1250 | 2036-01 | 2038-01 | 70 |  |
| ZBO modernization (ZBO) | 0 | — | 180 | 2037-07 | 2037-07 | 12 |  |

## График по источникам (т)

| Год | Источник | Резерв, т/год | Заказано | Поставлено (факт) | Цена, млн/т | Оплачиваемый объём | Закупка, млн | в т.ч. премия TOP, млн | Резервирование, млн |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 120.9 | 120.9 | 120.9 | 6.20 | 120.9 | 749.4 | 0.0 | 54.4 |
| 2036 | Earth-Core | 168.4 | 168.4 | 168.4 | 6.20 | 168.4 | 1043.8 | 0.0 | 75.8 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2037 | Earth-Flex | 38.3 | 38.3 | 38.3 | 8.90 | 38.3 | 340.6 | 0.0 | 5.7 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2038 | Earth-Flex | 37.2 | 37.2 | 37.2 | 8.90 | 37.2 | 331.2 | 0.0 | 5.6 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2039 | Earth-Flex | 105.8 | 105.8 | 105.8 | 8.90 | 105.8 | 941.4 | 0.0 | 15.9 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 0.0 | 16.5 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 | 0.0 |

Оплачиваемый объём = max(заказ, take-or-pay × резерв × доля года); начальный запас подготовительного периода учтён в закупке первого года.

## Матрица проверок (каждое правило × год, включая выполненные)

| Правило | Год | Метрика | Факт | Лимит | Оп. | Результат | Строгость |
|---|---:|---|---:|---:|---|:---:|---|
| BASE_CRITICAL_SERVICE | 2035 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | ориентир |
| BASE_CRITICAL_SERVICE | 2036 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | ориентир |
| BASE_CRITICAL_SERVICE | 2037 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | ориентир |
| BASE_CRITICAL_SERVICE | 2038 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | ориентир |
| BASE_CRITICAL_SERVICE | 2039 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | ориентир |
| BASE_CRITICAL_SERVICE | 2040 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | ориентир |
| BASE_TOTAL_SERVICE | 2035 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | ориентир |
| BASE_TOTAL_SERVICE | 2036 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | ориентир |
| BASE_TOTAL_SERVICE | 2037 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | ориентир |
| BASE_TOTAL_SERVICE | 2038 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | ориентир |
| BASE_TOTAL_SERVICE | 2039 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | ориентир |
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 0.9745 | 0.9700 | >= | выполнено | ориентир |
| CAPEX_2037 | 2035 | cumulative_capex | 0.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2037 | 2036 | cumulative_capex | 1250.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2037 | 2037 | cumulative_capex | 1430.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2035 | cumulative_capex | 0.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2036 | cumulative_capex | 1250.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2037 | cumulative_capex | 1430.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2038 | cumulative_capex | 1430.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2039 | cumulative_capex | 1430.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2040 | cumulative_capex | 1430.0000 | 2800.0000 | <= | выполнено | жёсткое |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 13.5617 | 13.5616 | >= | выполнено | жёсткое |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 18.9864 | 18.9863 | >= | выполнено | жёсткое |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 25.7672 | 25.7671 | >= | выполнено | жёсткое |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 38.5276 | 38.5274 | >= | выполнено | жёсткое |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 49.3153 | 49.3151 | >= | выполнено | жёсткое |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 60.1030 | 60.1027 | >= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2035 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2036 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2037 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2038 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2039 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2040 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2035 | end_of_month_stock_t_in_worst_month | 18.9864 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2035 | reserved_A_t_per_year | 120.8640 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2035 | ordered_A_t | 120.8636 | 120.8640 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2035 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2035 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2036 | end_of_month_stock_t_in_worst_month | 25.7672 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2036 | reserved_A_t_per_year | 168.3570 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2036 | ordered_A_t | 168.3569 | 168.3570 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2036 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2036 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2037 | end_of_month_stock_t_in_worst_month | 30.2642 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2037 | reserved_B_t_per_year | 38.2660 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_B_t | 38.2659 | 38.2660 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2038 | end_of_month_stock_t_in_worst_month | 49.3153 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_B_t_per_year | 37.2150 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_B_t | 37.2143 | 37.2150 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_D_t | 100.0000 | 100.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2039 | end_of_month_stock_t_in_worst_month | 60.1030 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_B_t_per_year | 105.7770 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_B_t | 105.7770 | 105.7770 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_D_t | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2040 | end_of_month_stock_t_in_worst_month | 54.0580 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 110.0000 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 110.0000 | 110.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_D_t | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |

## Нарушения

Нарушений нет.
