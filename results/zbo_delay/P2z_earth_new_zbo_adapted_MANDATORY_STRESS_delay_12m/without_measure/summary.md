# P2z_earth_new_zbo_adapted — MANDATORY_STRESS (Обязательный стрессовый сценарий)

План исполним: **НЕТ** — жёстких нарушений: 4, отклонений от ориентиров: 0, предупреждений: 0

Единицы: топливо — т; деньги — млн у.е. в постоянных ценах 2035 г.; шаг расчёта — календарный месяц; ставка дисконтирования r = 8% (TEAM_ASSUMPTION, одинакова для всех альтернатив). Те же числа — в CSV/XLSX/JSON этого каталога; календарь заказов и поставок — `delivery_schedule.csv`; реестр допущений — `assumptions.csv`.

## Итоговые показатели

| Показатель | Ключ | Значение |
|---|---|---:|
| Полные затраты, млн | `total_cost_mln` | 12,782.152 |
| Приведённые затраты (PV), млн | `pv_cost_mln` | 10,074.755 |
| Затраты на обслуженную тонну, млн/т | `cost_per_served_t_mln` | 8.333 |
| PV затрат на обслуженную тонну, млн/т | `pv_cost_per_served_t_mln` | 6.568 |
| Обслужено, т | `served_total_t` | 1,534.000 |
| Спрос, т | `demand_total_t` | 1,534.000 |
| Дефицит, т | `shortage_total_t` | 0.000 |
| Дефицит критического спроса, т | `shortage_critical_t` | 0.000 |
| Мин. уровень сервиса (общий) | `min_service_level_total` | 1.000 |
| Мин. уровень сервиса (критический) | `min_service_level_critical` | 1.000 |
| Потери при хранении, т | `losses_total_t` | 39.519 |
| CAPEX, млн | `capex_total_mln` | 540.000 |
| Закупка, млн | `procurement_total_mln` | 11,482.316 |
| Резервирование мощности, млн | `reservation_total_mln` | 604.827 |
| Хранение, млн | `holding_total_mln` | 125.009 |
| Постоянный OPEX, млн | `fixed_opex_total_mln` | 30.000 |
| Оплачено по take-or-pay сверх заказа, т | `take_or_pay_idle_t` | 0.000 |
| Премия take-or-pay (оплата незаказанного объёма), млн | `take_or_pay_topup_mln` | 0.000 |

## Годовой баланс (т)

| Год | Спрос | в т.ч. критич. | Обслужено | УС общий | УС критич. | Дефицит | Поступление (факт) | Потери | Запас на начало | Запас на конец | R45 | Резерв на начало года | Хранилище |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | выполнен | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | выполнен | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 207.9 | 9.36 | 23.4 | 32.0 | 23.4 | выполнен | BASE |
| 2038 | 287.5 | 195.5 | 287.5 | 1.000 | 1.000 | 0.0 | 301.0 | 8.58 | 32.0 | 37.0 | 35.4 | НЕ ВЫПОЛНЕН | ZBO |
| 2039 | 368.0 | 241.5 | 368.0 | 1.000 | 1.000 | 0.0 | 382.5 | 4.59 | 37.0 | 46.9 | 45.4 | НЕ ВЫПОЛНЕН | ZBO |
| 2040 | 448.5 | 287.5 | 448.5 | 1.000 | 1.000 | 0.0 | 430.0 | 5.16 | 46.9 | 23.2 | 55.3 | НЕ ВЫПОЛНЕН | ZBO |

УС — уровень сервиса (обслужено / спрос); R45 — 45-дневный резерв `D_y × 45 / 365`, проверяется по физическому запасу на начало года.

## Финансы (млн у.е., постоянные цены 2035 г.)

| Год | Закупка | в т.ч. премия TOP | Резервирование | Хранение | Пост. OPEX | CAPEX | Итого | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 0.0 | 51.4 | 11.0 | 0.0 | 360.0 | 1218.5 | 1218.5 |
| 2036 | 948.9 | 0.0 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1305.4 | 0.0 | 90.9 | 20.0 | 0.0 | 180.0 | 1596.3 | 1368.5 |
| 2038 | 2260.9 | 0.0 | 118.8 | 23.9 | 6.0 | 0.0 | 2409.6 | 1912.8 |
| 2039 | 3091.0 | 0.0 | 133.9 | 30.2 | 12.0 | 0.0 | 3267.0 | 2401.4 |
| 2040 | 3080.0 | 0.0 | 141.0 | 25.2 | 12.0 | 0.0 | 3258.2 | 2217.5 |

«Премия TOP» — часть строки «Закупка», оплаченная за объём сверх заказанного по условию take-or-pay; это разложение платежа, а не дополнительный платёж.

## Инвестиции

| Инвестиция | Плата за опцион, млн | Дата опциона | Реализация / CAPEX, млн | Дата решения | Ввод в строй | Пост. OPEX, млн/год | Примечание |
|---|---:|---|---:|---|---|---:|---|
| Earth-New option (EARTH_NEW) | 90 | 2035-01 | 270 | 2035-01 | 2037-01 | 0 |  |
| ZBO modernization (ZBO) | 0 | — | 180 | 2037-07 | 2038-07 | 12 |  |

## График по источникам (т)

| Год | Источник | Резерв, т/год | Заказано | Поставлено (факт) | Цена, млн/т | Оплачиваемый объём | Закупка, млн | в т.ч. премия TOP, млн | Резервирование, млн |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 0.0 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 0.0 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2037 | Earth-New | 17.9 | 17.9 | 17.9 | 7.10 | 17.9 | 127.4 | 0.0 | 5.4 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 0.0 | 85.5 |
| 2038 | Earth-New | 111.0 | 111.0 | 111.0 | 7.10 | 111.0 | 788.4 | 0.0 | 33.3 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 0.0 | 85.5 |
| 2039 | Earth-Flex | 62.5 | 62.5 | 62.5 | 11.12 | 62.5 | 695.5 | 0.0 | 9.4 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 0.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 0.0 | 16.5 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 0.0 | 39.0 |

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
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | ориентир |
| CAPEX_2037 | 2035 | cumulative_capex | 360.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2037 | 2036 | cumulative_capex | 360.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2037 | 2037 | cumulative_capex | 540.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2035 | cumulative_capex | 360.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2036 | cumulative_capex | 360.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2037 | cumulative_capex | 540.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2038 | cumulative_capex | 540.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2039 | cumulative_capex | 540.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2040 | cumulative_capex | 540.0000 | 2800.0000 | <= | выполнено | жёсткое |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 12.3289 | 12.3288 | >= | выполнено | жёсткое |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 17.2604 | 17.2603 | >= | выполнено | жёсткое |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 23.4249 | 23.4247 | >= | выполнено | жёсткое |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 32.0144 | 35.4452 | >= | НАРУШЕНО | жёсткое |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 36.9720 | 45.3699 | >= | НАРУШЕНО | жёсткое |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 46.8967 | 55.2945 | >= | НАРУШЕНО | жёсткое |
| EMERGENCY_BASE_STREAK | 2035 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2036 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2037 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2038 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2039 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2040 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| STRESS_LOSS_LIMIT | 2038 | losses_divided_by_throughput | 0.0285 | 0.0200 | <= | НАРУШЕНО | жёсткое |
| STRESS_LOSS_LIMIT | 2039 | losses_divided_by_throughput | 0.0120 | 0.0200 | <= | выполнено | жёсткое |
| STRESS_LOSS_LIMIT | 2040 | losses_divided_by_throughput | 0.0120 | 0.0200 | <= | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2035 | end_of_month_stock_t_in_worst_month | 17.2604 | 70.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2035 | intra_month_peak_stock_t_in_worst_month | 25.5938 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2035 | reserved_A_t_per_year | 109.8760 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2035 | ordered_A_t | 109.8760 | 109.8760 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2035 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2035 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2036 | end_of_month_stock_t_in_worst_month | 23.4249 | 70.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2036 | intra_month_peak_stock_t_in_worst_month | 35.0916 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2036 | reserved_A_t_per_year | 153.0520 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2036 | ordered_A_t | 153.0518 | 153.0520 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2036 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2036 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2037 | end_of_month_stock_t_in_worst_month | 32.0144 | 70.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2037 | intra_month_peak_stock_t_in_worst_month | 47.8477 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2037 | reserved_C_t_per_year | 17.9480 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_C_t | 17.9471 | 17.9480 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2038 | end_of_month_stock_t_in_worst_month | 32.0136 | 70.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2038 | intra_month_peak_stock_t_in_worst_month | 55.9719 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_C_t_per_year | 111.0380 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_C_t | 111.0372 | 111.0380 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2039 | end_of_month_stock_t_in_worst_month | 46.8967 | 120.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2039 | intra_month_peak_stock_t_in_worst_month | 77.5634 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_B_t_per_year | 62.5150 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_B_t | 62.5149 | 62.5150 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_C_t_per_year | 130.0000 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_C_t | 130.0000 | 130.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2040 | end_of_month_stock_t_in_worst_month | 44.9251 | 120.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2040 | intra_month_peak_stock_t_in_worst_month | 82.3001 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 110.0000 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 110.0000 | 110.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_C_t_per_year | 130.0000 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_C_t | 130.0000 | 130.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |

## Нарушения

| Правило | Строгость | Год | Месяц | Источник | Факт | Лимит | Превышение | Сообщение |
|---|---|---:|---:|---|---:|---:|---:|---|
| RESERVE_45D | жёсткое | 2038 | 1 |  | 32.014 | 35.445 | 3.431 | 2038-01: физический запас 32.014 т < 45-дневного резерва 35.445 т |
| RESERVE_45D | жёсткое | 2039 | 1 |  | 36.972 | 45.370 | 8.398 | 2039-01: физический запас 36.972 т < 45-дневного резерва 45.370 т |
| RESERVE_45D | жёсткое | 2040 | 1 |  | 46.897 | 55.295 | 8.398 | 2040-01: физический запас 46.897 т < 45-дневного резерва 55.295 т |
| STRESS_LOSS_LIMIT | жёсткое | 2038 |  |  | 0.029 | 0.020 | 0.009 | 2038: потери/поступление 0.0285 > 0.02 (8.580 т из 301.037 т) |
