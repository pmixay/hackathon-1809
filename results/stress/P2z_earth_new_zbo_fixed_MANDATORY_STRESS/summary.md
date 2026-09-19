# P2z_earth_new_zbo — MANDATORY_STRESS (Обязательный стрессовый сценарий)

План исполним: **НЕТ** — жёстких нарушений: 3, отклонений от ориентиров: 2, предупреждений: 0

Единицы: топливо — т; деньги — млн у.е. в постоянных ценах 2035 г.; шаг расчёта — календарный месяц; ставка дисконтирования r = 8% (TEAM_ASSUMPTION, одинакова для всех альтернатив). Те же числа — в CSV/XLSX/JSON этого каталога; календарь заказов и поставок — `delivery_schedule.csv`; реестр допущений — `assumptions.csv`.

## Итоговые показатели

| Показатель | Ключ | Значение |
|---|---|---:|
| Полные затраты, млн | `total_cost_mln` | 11,517.764 |
| Приведённые затраты (PV), млн | `pv_cost_mln` | 9,142.898 |
| Затраты на обслуженную тонну, млн/т | `cost_per_served_t_mln` | 8.009 |
| PV затрат на обслуженную тонну, млн/т | `pv_cost_per_served_t_mln` | 6.358 |
| Обслужено, т | `served_total_t` | 1,438.083 |
| Спрос, т | `demand_total_t` | 1,534.000 |
| Дефицит, т | `shortage_total_t` | 95.917 |
| Дефицит критического спроса, т | `shortage_critical_t` | 0.000 |
| Мин. уровень сервиса (общий) | `min_service_level_total` | 0.870 |
| Мин. уровень сервиса (критический) | `min_service_level_critical` | 1.000 |
| Потери при хранении, т | `losses_total_t` | 29.492 |
| CAPEX, млн | `capex_total_mln` | 540.000 |
| Закупка, млн | `procurement_total_mln` | 10,300.836 |
| Резервирование мощности, млн | `reservation_total_mln` | 578.846 |
| Хранение, млн | `holding_total_mln` | 56.082 |
| Постоянный OPEX, млн | `fixed_opex_total_mln` | 42.000 |
| Оплачено по take-or-pay сверх заказа, т | `take_or_pay_idle_t` | 0.000 |
| Премия take-or-pay (оплата незаказанного объёма), млн | `take_or_pay_topup_mln` | 0.000 |

## Годовой баланс (т)

| Год | Спрос | в т.ч. критич. | Обслужено | УС общий | УС критич. | Дефицит | Поступление (факт) | Потери | Запас на начало | Запас на конец | R45 | Резерв на начало года | Хранилище |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | выполнен | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | выполнен | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 23.4 | 30.8 | 23.4 | выполнен | ZBO |
| 2038 | 287.5 | 195.5 | 287.5 | 1.000 | 1.000 | 0.0 | 261.8 | 3.14 | 30.8 | 2.0 | 35.4 | НЕ ВЫПОЛНЕН | ZBO |
| 2039 | 368.0 | 241.5 | 330.6 | 0.898 | 1.000 | 37.4 | 332.6 | 3.99 | 2.0 | 0.0 | 45.4 | НЕ ВЫПОЛНЕН | ZBO |
| 2040 | 448.5 | 287.5 | 390.0 | 0.870 | 1.000 | 58.5 | 394.7 | 4.74 | 0.0 | 0.0 | 55.3 | НЕ ВЫПОЛНЕН | ZBO |

УС — уровень сервиса (обслужено / спрос); R45 — 45-дневный резерв `D_y × 45 / 365`, проверяется по физическому запасу на начало года.

## Финансы (млн у.е., постоянные цены 2035 г.)

| Год | Закупка | в т.ч. премия TOP | Резервирование | Хранение | Пост. OPEX | CAPEX | Итого | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 0.0 | 51.4 | 10.7 | 0.0 | 360.0 | 1218.2 | 1218.2 |
| 2036 | 948.9 | 0.0 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1271.6 | 0.0 | 89.5 | 18.9 | 6.0 | 180.0 | 1566.0 | 1342.6 |
| 2038 | 1982.1 | 0.0 | 107.0 | 11.8 | 12.0 | 0.0 | 2112.9 | 1677.3 |
| 2039 | 2535.9 | 0.0 | 126.4 | 0.1 | 12.0 | 0.0 | 2674.4 | 1965.7 |
| 2040 | 2766.2 | 0.0 | 135.7 | 0.0 | 12.0 | 0.0 | 2913.9 | 1983.1 |

«Премия TOP» — часть строки «Закупка», оплаченная за объём сверх заказанного по условию take-or-pay; это разложение платежа, а не дополнительный платёж.

## Инвестиции

| Инвестиция | Плата за опцион, млн | Дата опциона | Реализация / CAPEX, млн | Дата решения | Ввод в строй | Пост. OPEX, млн/год | Примечание |
|---|---:|---|---:|---|---|---:|---|
| Earth-New option (EARTH_NEW) | 90 | 2035-01 | 270 | 2035-01 | 2037-01 | 0 |  |
| ZBO modernization (ZBO) | 0 | — | 180 | 2037-07 | 2037-07 | 12 |  |

## График по источникам (т)

| Год | Источник | Резерв, т/год | Заказано | Поставлено (факт) | Цена, млн/т | Оплачиваемый объём | Закупка, млн | в т.ч. премия TOP, млн | Резервирование, млн |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 0.0 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 0.0 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2037 | Earth-New | 13.2 | 13.2 | 13.2 | 7.10 | 13.2 | 93.6 | 0.0 | 4.0 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 0.0 | 85.5 |
| 2038 | Earth-New | 71.8 | 71.8 | 71.8 | 7.10 | 71.8 | 509.6 | 0.0 | 21.5 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 0.0 | 85.5 |
| 2039 | Earth-Flex | 12.6 | 12.6 | 12.6 | 11.12 | 12.6 | 140.4 | 0.0 | 1.9 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 0.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2040 | Earth-Flex | 74.7 | 74.7 | 74.7 | 8.90 | 74.7 | 665.2 | 0.0 | 11.2 |
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
| BASE_TOTAL_SERVICE | 2039 | total_service_level | 0.8983 | 0.9700 | >= | НАРУШЕНО | ориентир |
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 0.8696 | 0.9700 | >= | НАРУШЕНО | ориентир |
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
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 30.8222 | 35.4452 | >= | НАРУШЕНО | жёсткое |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 1.9524 | 45.3699 | >= | НАРУШЕНО | жёсткое |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 0.0000 | 55.2945 | >= | НАРУШЕНО | жёсткое |
| EMERGENCY_BASE_STREAK | 2035 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2036 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2037 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2038 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2039 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2040 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| STRESS_LOSS_LIMIT | 2038 | losses_divided_by_throughput | 0.0120 | 0.0200 | <= | выполнено | жёсткое |
| STRESS_LOSS_LIMIT | 2039 | losses_divided_by_throughput | 0.0120 | 0.0200 | <= | выполнено | жёсткое |
| STRESS_LOSS_LIMIT | 2040 | losses_divided_by_throughput | 0.0120 | 0.0200 | <= | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2035 | end_of_month_stock_t_in_worst_month | 17.2604 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2035 | reserved_A_t_per_year | 109.8760 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2035 | ordered_A_t | 109.8760 | 109.8760 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2035 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2035 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2036 | end_of_month_stock_t_in_worst_month | 23.4249 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2036 | reserved_A_t_per_year | 153.0520 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2036 | ordered_A_t | 153.0518 | 153.0520 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2036 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2036 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2037 | end_of_month_stock_t_in_worst_month | 25.4473 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2037 | reserved_C_t_per_year | 13.1890 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_C_t | 13.1882 | 13.1890 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2038 | end_of_month_stock_t_in_worst_month | 28.4164 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_C_t_per_year | 71.7720 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_C_t | 71.7714 | 71.7720 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2039 | end_of_month_stock_t_in_worst_month | 0.0000 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_B_t_per_year | 12.6220 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_B_t | 12.6216 | 12.6220 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_C_t_per_year | 130.0000 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_C_t | 130.0000 | 130.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2040 | end_of_month_stock_t_in_worst_month | 0.0000 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 74.7370 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 74.7369 | 74.7370 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_C_t_per_year | 130.0000 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_C_t | 130.0000 | 130.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |

## Нарушения

| Правило | Строгость | Год | Месяц | Источник | Факт | Лимит | Превышение | Сообщение |
|---|---|---:|---:|---|---:|---:|---:|---|
| BASE_TOTAL_SERVICE | ориентир | 2039 |  |  | 0.898 | 0.970 | 0.072 | 2039: общий уровень сервиса 0.8983 < 0.97 (дефицит 37.417 т) [в этом сценарии — ориентир, не жёсткое ограничение] |
| BASE_TOTAL_SERVICE | ориентир | 2040 |  |  | 0.870 | 0.970 | 0.100 | 2040: общий уровень сервиса 0.8696 < 0.97 (дефицит 58.500 т) [в этом сценарии — ориентир, не жёсткое ограничение] |
| RESERVE_45D | жёсткое | 2038 | 1 |  | 30.822 | 35.445 | 4.623 | 2038-01: физический запас 30.822 т < 45-дневного резерва 35.445 т |
| RESERVE_45D | жёсткое | 2039 | 1 |  | 1.952 | 45.370 | 43.417 | 2039-01: физический запас 1.952 т < 45-дневного резерва 45.370 т |
| RESERVE_45D | жёсткое | 2040 | 1 |  | 0.000 | 55.295 | 55.295 | 2040-01: физический запас 0.000 т < 45-дневного резерва 55.295 т |
