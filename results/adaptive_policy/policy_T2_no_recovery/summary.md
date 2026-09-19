# P3_isru_zbo_policy_T2_no_recovery — TEAM_TRAJ_T2_NO_RECOVERY (T2 без восстановления ISRU)

План исполним: **НЕТ** — жёстких нарушений: 1, отклонений от ориентиров: 0, предупреждений: 0

Единицы: топливо — т; деньги — млн у.е. в постоянных ценах 2035 г.; шаг расчёта — календарный месяц; ставка дисконтирования r = 8% (TEAM_ASSUMPTION, одинакова для всех альтернатив). Те же числа — в CSV/XLSX/JSON этого каталога; календарь заказов и поставок — `delivery_schedule.csv`; реестр допущений — `assumptions.csv`.

## Итоговые показатели

| Показатель | Ключ | Значение |
|---|---|---:|
| Полные затраты, млн | `total_cost_mln` | 14,979.833 |
| Приведённые затраты (PV), млн | `pv_cost_mln` | 11,828.867 |
| Затраты на обслуженную тонну, млн/т | `cost_per_served_t_mln` | 9.771 |
| PV затрат на обслуженную тонну, млн/т | `pv_cost_per_served_t_mln` | 7.715 |
| Обслужено, т | `served_total_t` | 1,533.134 |
| Спрос, т | `demand_total_t` | 1,534.000 |
| Дефицит, т | `shortage_total_t` | 0.866 |
| Дефицит критического спроса, т | `shortage_critical_t` | 0.000 |
| Мин. уровень сервиса (общий) | `min_service_level_total` | 0.997 |
| Мин. уровень сервиса (критический) | `min_service_level_critical` | 1.000 |
| Потери при хранении, т | `losses_total_t` | 31.223 |
| CAPEX, млн | `capex_total_mln` | 1,430.000 |
| Закупка, млн | `procurement_total_mln` | 12,580.313 |
| Резервирование мощности, млн | `reservation_total_mln` | 585.030 |
| Хранение, млн | `holding_total_mln` | 132.490 |
| Постоянный OPEX, млн | `fixed_opex_total_mln` | 252.000 |
| Оплачено по take-or-pay сверх заказа, т | `take_or_pay_idle_t` | 0.000 |
| Премия take-or-pay (оплата незаказанного объёма), млн | `take_or_pay_topup_mln` | 0.000 |

## Годовой баланс (т)

| Год | Спрос | в т.ч. критич. | Обслужено | УС общий | УС критич. | Дефицит | Поступление (факт) | Потери | Запас на начало | Запас на конец | R45 | Резерв на начало года | Хранилище |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | выполнен | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | выполнен | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 23.4 | 30.8 | 23.4 | выполнен | ZBO |
| 2038 | 287.5 | 195.5 | 286.6 | 0.997 | 1.000 | 0.9 | 310.7 | 3.73 | 30.8 | 51.2 | 35.4 | НЕ ВЫПОЛНЕН | ZBO |
| 2039 | 368.0 | 241.5 | 368.0 | 1.000 | 1.000 | 0.0 | 376.6 | 4.52 | 51.2 | 55.3 | 45.4 | выполнен | ZBO |
| 2040 | 448.5 | 287.5 | 448.5 | 1.000 | 1.000 | 0.0 | 446.0 | 5.35 | 55.3 | 47.4 | 55.3 | выполнен | ZBO |

УС — уровень сервиса (обслужено / спрос); R45 — 45-дневный резерв `D_y × 45 / 365`, проверяется по физическому запасу на начало года.

## Финансы (млн у.е., постоянные цены 2035 г.)

| Год | Закупка | в т.ч. премия TOP | Резервирование | Хранение | Пост. OPEX | CAPEX | Итого | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 0.0 | 51.4 | 11.0 | 0.0 | 0.0 | 858.5 | 858.5 |
| 2036 | 948.9 | 0.0 | 68.9 | 14.6 | 0.0 | 1250.0 | 2282.4 | 2113.4 |
| 2037 | 1295.4 | 0.0 | 87.5 | 18.9 | 6.0 | 180.0 | 1587.8 | 1361.3 |
| 2038 | 2703.7 | 0.0 | 117.3 | 14.5 | 82.0 | 0.0 | 2917.5 | 2316.0 |
| 2039 | 3215.2 | 0.0 | 130.0 | 36.4 | 82.0 | 0.0 | 3463.6 | 2545.9 |
| 2040 | 3621.0 | 0.0 | 130.0 | 37.0 | 82.0 | 0.0 | 3870.0 | 2633.8 |

«Премия TOP» — часть строки «Закупка», оплаченная за объём сверх заказанного по условию take-or-pay; это разложение платежа, а не дополнительный платёж.

## Инвестиции

| Инвестиция | Плата за опцион, млн | Дата опциона | Реализация / CAPEX, млн | Дата решения | Ввод в строй | Пост. OPEX, млн/год | Примечание |
|---|---:|---|---:|---|---|---:|---|
| Lunar-ISRU pilot (LUNAR_ISRU) | 0 | — | 1250 | 2036-01 | 2038-01 | 70 |  |
| ZBO modernization (ZBO) | 0 | — | 180 | 2037-07 | 2037-07 | 12 |  |

## График по источникам (т)

| Год | Источник | Резерв, т/год | Заказано | Поставлено (факт) | Цена, млн/т | Оплачиваемый объём | Закупка, млн | в т.ч. премия TOP, млн | Резервирование, млн |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 0.0 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 0.0 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2037 | Earth-Flex | 13.2 | 13.2 | 13.2 | 8.90 | 13.2 | 117.4 | 0.0 | 2.0 |
| 2038 | Earth-Core | 161.8 | 161.8 | 161.8 | 7.75 | 161.8 | 1253.7 | 0.0 | 72.8 |
| 2038 | Earth-Flex | 110.0 | 54.7 | 54.7 | 11.12 | 54.7 | 609.0 | 0.0 | 16.5 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 55.0 | 3.00 | 100.0 | 300.0 | 0.0 | 0.0 |
| 2038 | Emergency | 80.0 | 39.2 | 39.2 | 13.80 | 39.2 | 541.0 | 0.0 | 28.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 0.0 | 85.5 |
| 2039 | Earth-Flex | 110.0 | 105.5 | 105.5 | 11.12 | 105.5 | 1173.8 | 0.0 | 16.5 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 66.0 | 3.00 | 120.0 | 360.0 | 0.0 | 0.0 |
| 2039 | Emergency | 80.0 | 15.1 | 15.1 | 13.80 | 15.1 | 208.9 | 0.0 | 28.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 0.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 0.0 | 16.5 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 66.0 | 3.00 | 120.0 | 360.0 | 0.0 | 0.0 |
| 2040 | Emergency | 80.0 | 80.0 | 80.0 | 13.80 | 80.0 | 1104.0 | 0.0 | 28.0 |

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
| BASE_TOTAL_SERVICE | 2038 | total_service_level | 0.9970 | 0.9700 | >= | выполнено | ориентир |
| BASE_TOTAL_SERVICE | 2039 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | ориентир |
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 1.0000 | 0.9700 | >= | выполнено | ориентир |
| CAPEX_2037 | 2035 | cumulative_capex | 0.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2037 | 2036 | cumulative_capex | 1250.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2037 | 2037 | cumulative_capex | 1430.0000 | 1800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2035 | cumulative_capex | 0.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2036 | cumulative_capex | 1250.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2037 | cumulative_capex | 1430.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2038 | cumulative_capex | 1430.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2039 | cumulative_capex | 1430.0000 | 2800.0000 | <= | выполнено | жёсткое |
| CAPEX_2040 | 2040 | cumulative_capex | 1430.0000 | 2800.0000 | <= | выполнено | жёсткое |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 12.3289 | 12.3288 | >= | выполнено | жёсткое |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 17.2604 | 17.2603 | >= | выполнено | жёсткое |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 23.4249 | 23.4247 | >= | выполнено | жёсткое |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 30.8222 | 35.4452 | >= | НАРУШЕНО | жёсткое |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 51.1757 | 45.3699 | >= | выполнено | жёсткое |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 55.3026 | 55.2945 | >= | выполнено | жёсткое |
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
| CAPACITY_EXCEEDED | 2037 | reserved_B_t_per_year | 13.1890 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_B_t | 13.1882 | 13.1890 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2038 | end_of_month_stock_t_in_worst_month | 51.1757 | 120.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2038 | intra_month_peak_stock_t_in_worst_month | 75.1341 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 161.7720 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 161.7714 | 161.7720 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_B_t_per_year | 110.0000 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_B_t | 54.7443 | 110.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_D_t | 100.0000 | 100.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2038 | reserved_E_t_per_year | 80.0000 | 80.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_E_t | 39.2000 | 80.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2039 | end_of_month_stock_t_in_worst_month | 55.3026 | 120.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2039 | intra_month_peak_stock_t_in_worst_month | 85.9692 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_B_t_per_year | 110.0000 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_B_t | 105.5084 | 110.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_D_t | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2039 | reserved_E_t_per_year | 80.0000 | 80.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_E_t | 15.1382 | 80.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| STORAGE_OVERFLOW | 2040 | end_of_month_stock_t_in_worst_month | 54.6481 | 120.0000 | <= | выполнено | жёсткое |
| INTRA_MONTH_PEAK | 2040 | intra_month_peak_stock_t_in_worst_month | 92.0231 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 110.0000 | 110.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 109.9992 | 110.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_D_t | 120.0000 | 120.0000 | <= | выполнено | жёсткое |
| CAPACITY_EXCEEDED | 2040 | reserved_E_t_per_year | 80.0000 | 80.0000 | <= | выполнено | жёсткое |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_E_t | 79.9992 | 80.0000 | <= | выполнено | жёсткое |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | выполнено | жёсткое |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | выполнено | жёсткое |

## Нарушения

| Правило | Строгость | Год | Месяц | Источник | Факт | Лимит | Превышение | Сообщение |
|---|---|---:|---:|---|---:|---:|---:|---|
| RESERVE_45D | жёсткое | 2038 | 1 |  | 30.822 | 35.445 | 4.623 | 2038-01: физический запас 30.822 т < 45-дневного резерва 35.445 т |
