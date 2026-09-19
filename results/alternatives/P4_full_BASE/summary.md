# P4_full — BASE (Стандартный сценарий)

План исполним: **ДА** — жёстких нарушений: 0, отклонений от ориентиров: 0, предупреждений: 0

Единицы: топливо — т; деньги — млн у.е. в постоянных ценах 2035 г.; шаг расчёта — календарный месяц; ставка дисконтирования r = 8% (TEAM_ASSUMPTION, одинакова для всех альтернатив). Те же числа — в CSV/XLSX/JSON этого каталога; календарь заказов и поставок — `delivery_schedule.csv`; реестр допущений — `assumptions.csv`.

## Итоговые показатели

| Показатель | Ключ | Значение |
|---|---|---:|
| Полные затраты, млн | `total_cost_mln` | 10,815.727 |
| Приведённые затраты (PV), млн | `pv_cost_mln` | 8,857.979 |
| Затраты на обслуженную тонну, млн/т | `cost_per_served_t_mln` | 7.781 |
| PV затрат на обслуженную тонну, млн/т | `pv_cost_per_served_t_mln` | 6.373 |
| Обслужено, т | `served_total_t` | 1,390.000 |
| Спрос, т | `demand_total_t` | 1,390.000 |
| Дефицит, т | `shortage_total_t` | 0.000 |
| Дефицит критического спроса, т | `shortage_critical_t` | 0.000 |
| Мин. уровень сервиса (общий) | `min_service_level_total` | 1.000 |
| Мин. уровень сервиса (критический) | `min_service_level_critical` | 1.000 |
| Потери при хранении, т | `losses_total_t` | 29.492 |
| CAPEX, млн | `capex_total_mln` | 1,790.000 |
| Закупка, млн | `procurement_total_mln` | 8,157.914 |
| Резервирование мощности, млн | `reservation_total_mln` | 485.716 |
| Хранение, млн | `holding_total_mln` | 130.097 |
| Постоянный OPEX, млн | `fixed_opex_total_mln` | 252.000 |
| Оплачено по take-or-pay сверх заказа, т | `take_or_pay_idle_t` | 0.000 |
| Премия take-or-pay (оплата незаказанного объёма), млн | `take_or_pay_topup_mln` | 0.000 |

## Годовой баланс (т)

| Год | Спрос | в т.ч. критич. | Обслужено | УС общий | УС критич. | Дефицит | Поступление (факт) | Потери | Запас на начало | Запас на конец | R45 | Резерв на начало года | Хранилище |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | выполнен | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | выполнен | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 23.4 | 30.8 | 23.4 | выполнен | ZBO |
| 2038 | 250.0 | 170.0 | 250.0 | 1.000 | 1.000 | 0.0 | 261.8 | 3.14 | 30.8 | 39.5 | 30.8 | выполнен | ZBO |
| 2039 | 320.0 | 210.0 | 320.0 | 1.000 | 1.000 | 0.0 | 332.6 | 3.99 | 39.5 | 48.1 | 39.5 | выполнен | ZBO |
| 2040 | 390.0 | 250.0 | 390.0 | 1.000 | 1.000 | 0.0 | 394.7 | 4.74 | 48.1 | 48.1 | 48.1 | выполнен | ZBO |

УС — уровень сервиса (обслужено / спрос); R45 — 45-дневный резерв `D_y × 45 / 365`, проверяется по физическому запасу на начало года.

## Финансы (млн у.е., постоянные цены 2035 г.)

| Год | Закупка | в т.ч. премия TOP | Резервирование | Хранение | Пост. OPEX | CAPEX | Итого | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 0.0 | 51.4 | 11.0 | 0.0 | 360.0 | 1218.5 | 1218.5 |
| 2036 | 948.9 | 0.0 | 68.9 | 14.6 | 0.0 | 1250.0 | 2282.4 | 2113.4 |
| 2037 | 1271.6 | 0.0 | 89.5 | 18.9 | 6.0 | 180.0 | 1566.0 | 1342.6 |
| 2038 | 1303.0 | 0.0 | 72.8 | 19.4 | 82.0 | 0.0 | 1477.2 | 1172.6 |
| 2039 | 1698.6 | 0.0 | 92.3 | 31.5 | 82.0 | 0.0 | 1904.4 | 1399.8 |
| 2040 | 2139.6 | 0.0 | 110.9 | 34.6 | 82.0 | 0.0 | 2367.2 | 1611.1 |

«Премия TOP» — часть строки «Закупка», оплаченная за объём сверх заказанного по условию take-or-pay; это разложение платежа, а не дополнительный платёж.

## Инвестиции

| Инвестиция | Плата за опцион, млн | Дата опциона | Реализация / CAPEX, млн | Дата решения | Ввод в строй | Пост. OPEX, млн/год | Примечание |
|---|---:|---|---:|---|---|---:|---|
| Earth-New option (EARTH_NEW) | 90 | 2035-01 | 270 | 2035-01 | 2037-01 | 0 |  |
| Lunar-ISRU pilot (LUNAR_ISRU) | 0 | — | 1250 | 2036-01 | 2038-01 | 70 |  |
| ZBO modernization (ZBO) | 0 | — | 180 | 2037-07 | 2037-07 | 12 |  |

## График по источникам (т)

| Год | Источник | Резерв, т/год | Заказано | Поставлено (факт) | Цена, млн/т | Оплачиваемый объём | Закупка, млн | в т.ч. премия TOP, млн | Резервирование, млн |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 0.0 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 0.0 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2037 | Earth-New | 13.2 | 13.2 | 13.2 | 7.10 | 13.2 | 93.6 | 0.0 | 4.0 |
| 2038 | Earth-Core | 161.8 | 161.8 | 161.8 | 6.20 | 161.8 | 1003.0 | 0.0 | 72.8 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2039 | Earth-New | 22.6 | 22.6 | 22.6 | 7.10 | 22.6 | 160.6 | 0.0 | 6.8 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2040 | Earth-New | 84.7 | 84.7 | 84.7 | 7.10 | 84.7 | 601.6 | 0.0 | 25.4 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 | 0.0 |

Оплачиваемый объём = max(заказ, take-or-pay × резерв × доля года); начальный запас подготовительного периода учтён в закупке первого года.

## Матрица проверок (каждое правило × год, включая выполненные)

| Правило | Год | Метрика | Факт | Лимит | Оп. | Результат | Строгость |
|---|---:|---|---:|---:|---|:---:|---|
| BASE_CRITICAL_SERVICE | 2035 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | жёсткое |
| BASE_CRITICAL_SERVICE | 2036 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | жёсткое |
| BASE_CRITICAL_SERVICE | 2037 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | жёсткое |
| BASE_CRITICAL_SERVICE | 2038 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | жёсткое |
| BASE_CRITICAL_SERVICE | 2039 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | жёсткое |
| BASE_CRITICAL_SERVICE | 2040 | critical_service_level | 1.0000 | 0.9900 | >= | выполнено | жёсткое |
| BASE_TOTAL_SERVICE | 2035 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | жёсткое |
| BASE_TOTAL_SERVICE | 2036 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | жёсткое |
| BASE_TOTAL_SERVICE | 2037 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | жёсткое |
| BASE_TOTAL_SERVICE | 2038 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | жёсткое |
| BASE_TOTAL_SERVICE | 2039 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | жёсткое |
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | жёсткое |
| CAPEX_2037 | 2035 | cumulative_capex | 360.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2037 | 2036 | cumulative_capex | 1610.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2037 | 2037 | cumulative_capex | 1790.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2035 | cumulative_capex | 360.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2036 | cumulative_capex | 1610.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2037 | cumulative_capex | 1790.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2038 | cumulative_capex | 1790.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2039 | cumulative_capex | 1790.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2040 | cumulative_capex | 1790.0000 | 2800.0000 | <= | выполнено | жёсткое |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 12.3289 | 12.3288 | >= | выполнено | жёсткое |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 17.2604 | 17.2603 | >= | выполнено | жёсткое |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 23.4249 | 23.4247 | >= | выполнено | жёсткое |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 30.8222 | 30.8219 | >= | выполнено | жёсткое |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 39.4524 | 39.4521 | >= | выполнено | жёсткое |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 48.0825 | 48.0822 | >= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2035 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2036 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2037 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2038 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2039 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
| EMERGENCY_BASE_STREAK | 2040 | consecutive_years_with_emergency_as_base_channel | 0 | 2.0000 | <= | выполнено | жёсткое |
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
| STORAGE_OVERFLOW | 2037 | end_of_month_stock_t_in_worst_month | 25.4473 | 70.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2037 | intra_month_peak_stock_t_in_worst_month | 41.2806 | 70.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2037 | reserved_C_t_per_year | 13.1890 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_C_t | 13.1882 | 13.1890 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2038 | end_of_month_stock_t_in_worst_month | 39.4524 | 120.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2038 | intra_month_peak_stock_t_in_worst_month | 60.2857 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 161.7720 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 161.7714 | 161.7720 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_D_t | 100.0000 | 100.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2039 | end_of_month_stock_t_in_worst_month | 48.0825 | 120.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2039 | intra_month_peak_stock_t_in_worst_month | 74.7492 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_C_t_per_year | 22.6220 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_C_t | 22.6216 | 22.6220 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_D_t | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2040 | end_of_month_stock_t_in_worst_month | 48.0826 | 120.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2040 | intra_month_peak_stock_t_in_worst_month | 80.5826 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_C_t_per_year | 84.7370 | 130.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_C_t | 84.7369 | 84.7370 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_D_t | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |

## Нарушения

Нарушений нет.
