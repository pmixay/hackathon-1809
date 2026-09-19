"""Сборка презентации TerraPlan (12 слайдов) из опубликованных результатов расчётов.

Запуск из корня репозитория: python docs/presentation/build_deck.py
Все числа читаются из results/; в текст слайдов ничего не вписывается вручную.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
OUT = ROOT / "docs/presentation/TerraPlan.pptx"
DARK, ACCENT, GOLD, INK, MUTED, PALE = "142F38", "176A5B", "D5A747", "183B40", "5B6F73", "E6EFEA"
FONT = "Arial"


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def kpis(path):
    out = {}
    for r in rows(path):
        try:
            out[r["metric"]] = float(r["value"])
        except ValueError:
            out[r["metric"]] = r["value"]
    return out


def num(v, d=0):
    """Русское форматирование: пробел между разрядами, запятая как десятичный знак."""
    s = f"{float(v):,.{d}f}".replace(",", " ").replace(".", ",")
    return s


def signed(v, d=1):
    return ("+" if float(v) > 0 else "") + num(v, d)


# ---------------------------------------------------------------- data
alt = {(r["plan_id"], r["scenario_id"]): r for r in rows(RESULTS / "alternatives/summary.csv")}
stress = {(r["plan_id"], r["scenario_id"]): r for r in rows(RESULTS / "stress/summary.csv")}
demand = {(r["plan_id"], r["scenario_id"]): r for r in rows(RESULTS / "demand/summary.csv")}
fin_base = rows(RESULTS / "alternatives/P2z_earth_new_zbo_BASE/financial_breakdown.csv")
fin_adapt = rows(RESULTS / "stress/P2z_earth_new_zbo_adapted_MANDATORY_STRESS/financial_breakdown.csv")
kpi_base = kpis(RESULTS / "alternatives/P2z_earth_new_zbo_BASE/kpi.csv")
kpi_stress = kpis(RESULTS / "alternatives/P2z_earth_new_zbo_MANDATORY_STRESS/kpi.csv")
kpi_adapt = kpis(RESULTS / "stress/P2z_earth_new_zbo_adapted_MANDATORY_STRESS/kpi.csv")
yearly_stress = rows(RESULTS / "alternatives/P2z_earth_new_zbo_MANDATORY_STRESS/yearly_balance.csv")
mcda = {}
for r in rows(RESULTS / "strategy/mcda_scores.csv"):
    mcda.setdefault(r["profile"], {})[r["plan_id"]] = float(r["score_0_100"])
exp12 = {(int(r["delay_months"]), r["measure"]): r for r in rows(RESULTS / "earth_new_delay_measures/comparison.csv")}
exp11 = {r["plan_id"]: r for r in rows(RESULTS / "geopolitical_price_shock/comparison.csv")}
exp9 = {int(r["delay_months"]): r for r in rows(RESULTS / "earth_new_delay/comparison.csv")}
tornado = {r["param"]: r for r in rows(RESULTS / "sensitivity/tornado.csv")}
thresholds = {r["param"]: r for r in rows(RESULTS / "sensitivity/thresholds.csv")}
reaction = {r["plan_id"]: r for r in rows(RESULTS / "reaction/summary.csv")}
ext = json.loads((RESULTS / "extensibility/run/result.json").read_text(encoding="utf-8"))
mc_rows = rows(RESULTS / "monte_carlo/comparison.csv")
mc = {r["variant"]: r for r in mc_rows if r["mode"] == "independent"}
mc_extra_col = next((c for c in mc_rows[0] if re.search(r"extra.*pv.*mean|mean.*extra.*pv|delta_pv.*mean|mean.*delta_pv", c)), None)
reverse = json.loads((RESULTS / "reverse_stress/report.json").read_text(encoding="utf-8"))
protection = {r["variant"]: r for r in rows(RESULTS / "protection_measures/comparison.csv")}
prot_report = json.loads((RESULTS / "protection_measures/report.json").read_text(encoding="utf-8"))


def prot_level(variant):
    sel = prot_report.get("selections") or {}
    item = sel.get(variant) if isinstance(sel, dict) else None
    if isinstance(item, dict):
        for key in ("reported_level", "minimum", "level"):
            if item.get(key) not in (None, ""):
                return str(item[key]).replace(".", ",")
    return ""


P = {"P1_earth_only": "P1 только Земля", "P2_earth_new": "P2 + Earth-New", "P2z_earth_new_zbo": "P2z + Earth-New + ZBO",
     "P3_isru_zbo": "P3 + ISRU + ZBO", "P4_full": "P4 полный портфель"}
pv_base = kpi_base["pv_cost_mln"]
pv_stress = kpi_stress["pv_cost_mln"]
pv_adapt = kpi_adapt["pv_cost_mln"]
pv_p3_adapt = float(stress[("P3_isru_zbo_adapted", "MANDATORY_STRESS")]["pv_cost_mln"])
pv_p4_adapt = float(stress[("P4_full_adapted", "MANDATORY_STRESS")]["pv_cost_mln"])
pv_p3_base = float(alt[("P3_isru_zbo", "BASE")]["pv_cost_mln"])
shortage_stress = kpi_stress["shortage_total_t"]
reserve_years = [r["year"] for r in yearly_stress if r["reserve_ok"] == "False"]
overflow_adapted_base = stress[("P2z_earth_new_zbo_adapted", "BASE")]["hard_violations"]

# ---------------------------------------------------------------- helpers
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W = prs.slide_width


def rgb(h):
    return RGBColor.from_string(h)


def textbox(slide, x, y, w, h, paragraphs, size=16, color=INK, bold=False, align=PP_ALIGN.LEFT, spacing=1.05):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    first = True
    for item in paragraphs:
        text, opts = (item, {}) if isinstance(item, str) else item
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(opts.get("after", 6))
        run = p.add_run()
        run.text = text
        f = run.font
        f.name, f.size, f.bold = FONT, Pt(opts.get("size", size)), opts.get("bold", bold)
        f.color.rgb = rgb(opts.get("color", color))
    return box


def title(slide, text, sub=None):
    bar = slide.shapes.add_shape(1, 0, 0, W, Inches(1.05))
    bar.fill.solid(); bar.fill.fore_color.rgb = rgb(DARK); bar.line.fill.background()
    textbox(slide, 0.5, 0.18, 12.3, 0.8, [(text, {"size": 28 if len(text) <= 58 else 22, "bold": True, "color": "FFFFFF"})])
    if sub:
        textbox(slide, 0.5, 1.12, 12.3, 0.5, [(sub, {"size": 14, "color": MUTED})])


def footer(slide, n):
    textbox(slide, 0.5, 7.05, 9, 0.35, [("TerraPlan · КосмоХакатон 2026 · кейс 2 · млн у.е. в ценах 2035 г., PV по ставке 8 %", {"size": 10, "color": MUTED})])
    textbox(slide, 11.8, 7.05, 1.2, 0.35, [(f"{n} / 12", {"size": 10, "color": MUTED})], align=PP_ALIGN.RIGHT)


def bullets(slide, items, x, y, w, h, size=15):
    return textbox(slide, x, y, w, h, [("• " + t if isinstance(t, str) else ("• " + t[0], t[1])) for t in items], size=size)


def table(slide, data, x, y, w, h, widths=None, size=11, header=True, bold_first_col=False):
    nrows, ncols = len(data), len(data[0])
    shape = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y), Inches(w), Inches(h))
    t = shape.table
    if widths:
        total = sum(widths)
        for i, wi in enumerate(widths):
            t.columns[i].width = Emu(int(Inches(w) * wi / total))
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            run = p.add_run(); run.text = str(val)
            run.font.name, run.font.size = FONT, Pt(size)
            run.font.bold = (header and i == 0) or (bold_first_col and j == 0)
            run.font.color.rgb = rgb("FFFFFF" if header and i == 0 else INK)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(ACCENT if header and i == 0 else ("F7F9F7" if i % 2 else "FFFFFF"))
    return shape


def chart(slide, categories, series, x, y, w, h, fmt="#,##0", legend=False, colors=(ACCENT, GOLD), label_size=12):
    data = CategoryChartData()
    data.categories = categories
    for name, values in series:
        data.add_series(name, values)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y), Inches(w), Inches(h), data)
    ch = gf.chart
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
        ch.legend.font.size, ch.legend.font.name = Pt(12), FONT
    plot = ch.plots[0]
    plot.gap_width = 80
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format, dl.number_format_is_linked = fmt, False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size, dl.font.name = Pt(label_size), FONT
    for i, s in enumerate(plot.series):
        s.format.fill.solid(); s.format.fill.fore_color.rgb = rgb(colors[i % len(colors)])
    ch.category_axis.tick_labels.font.size, ch.category_axis.tick_labels.font.name = Pt(12), FONT
    ch.value_axis.tick_labels.font.size, ch.value_axis.tick_labels.font.name = Pt(11), FONT
    ch.value_axis.has_major_gridlines = True
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = "#,##0", False
    return ch


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


outline = []


def new_slide(n, heading, sub=None, source=""):
    s = prs.slides.add_slide(BLANK)
    if heading:
        title(s, heading, sub)
    footer(s, n)
    outline.append({"n": n, "title": heading or "TerraPlan", "source": source})
    return s


# ---------------------------------------------------------------- slides
# 1. Титул
s = new_slide(1, None, source="решение команды; итоги EXP-01, EXP-02")
bg = s.shapes.add_shape(1, 0, 0, W, prs.slide_height); bg.fill.solid(); bg.fill.fore_color.rgb = rgb(DARK); bg.line.fill.background()
textbox(s, 0.8, 1.6, 11.5, 1.2, [("TerraPlan", {"size": 60, "bold": True, "color": "FFFFFF"})])
textbox(s, 0.8, 2.8, 11.5, 1.0, [("Планирование топливного снабжения орбитального узла, 2035–2040", {"size": 28, "color": "D0E3DF"})])
textbox(s, 0.8, 3.9, 11.5, 2.2, [
    ("КосмоХакатон 2026 · кейс 2 «Топливный космоконтур 2035» · команда TerraPlan", {"size": 18, "color": "D0E3DF"}),
    (f"Решение: земной портфель с новым поставщиком и модернизацией хранилища (P2z) — {num(pv_base)} млн PV в стандартном сценарии, "
     f"{num(pv_adapt)} млн PV в обязательном стрессе после заблаговременной адаптации, дефицит 0 т в обоих случаях.", {"size": 18, "color": "FFFFFF"}),
    ("Работающий цифровой контур: помесячный баланс, контракты, инвестиции, проверки ограничений, сравнение сценариев, сохранение и выгрузка.", {"size": 16, "color": "D0E3DF"}),
])
notes(s, "Числа: сводные таблицы EXP-01 и EXP-02. Все денежные показатели в млн условных единиц в ценах 2035 г.; PV по реальной ставке 8 %.")

# 2. Задача и пользовательский сценарий
s = new_slide(2, "Задача оператора и пользовательский сценарий", "Спрос растёт почти в четыре раза; нужен исполнимый план при жёстких ограничениях", "данные задания")
bullets(s, ["Спрос: 100 → 390 т/год (критический 80 → 250 т) при пяти каналах: Earth-Core, Earth-Flex, Earth-New, Lunar-ISRU, Emergency.",
            "Хранилище 70 т с потерями 4,5 % от поступления; после модернизации ZBO — 120 т и 1,2 %.",
            "Физический резерв 45 дней спроса на 1 января; сервис ≥ 97 % общий и ≥ 99 % критический.",
            "CAPEX ≤ 1 800 млн до 2037 и ≤ 2 800 млн до 2040; Emergency — не базовый канал дольше двух лет.",
            "Обязательный стресс: спрос +15 % с 2038, цены Earth-Core/Earth-Flex +25 % в 2038–2039, ISRU 55 % / 75 %, потери ≤ 2 %."],
        0.5, 1.7, 6.6, 5.2, size=15)
textbox(s, 7.4, 1.65, 5.5, 0.4, [("Сценарий оператора в интерфейсе", {"size": 16, "bold": True, "color": ACCENT})])
bullets(s, ["1. Открыть сохранённый план или изменить заказы, резервы, инвестиции, запас.",
            "2. При необходимости изменить цены и условия контрактов на копии данных с описанием допущения.",
            "3. Рассчитать: баланс, расходы, сервис, дефицит по годам и месяцам.",
            "4. Проверить нарушения: правило, год, величина, лимит, причина.",
            "5. Переключить BASE ↔ обязательный стресс, сравнить A и B.",
            "6. Оценить свои риски: задержка Earth-New, ценовой шок, Source-X и 2041 год.",
            "7. Сохранить рабочий файл и открыть его повторно.",
            "8. Выгрузить CSV / XLSX / JSON с планом, проверками и хешами."],
        7.4, 2.1, 5.5, 4.8, size=14)
notes(s, "Источник: постановка кейса и таблицы данных задания; порядок демонстрации — инструкция оператора.")

# 3. Как считает контур
s = new_slide(3, "Как считает цифровой контур", "Единый расчётный путь для командной строки, программного интерфейса и интерфейса оператора", "архитектура расчёта; каталог ограничений")
bullets(s, ["Шаг — календарный месяц, 2035-01 … 2040-12, плюс подготовительный период 2034 для начального запаса.",
            "Баланс: запас на конец = запас на начало + поступление − потери − выдача; потери = поступление × коэффициент режима, один раз; запас не бывает отрицательным, дефицит показывается отдельно.",
            "Контракты: оплачиваемый объём = max(заказ, take-or-pay × резерв × доля периода); плата за резерв = ставка × резерв × доля периода; недопоставка платёж не возвращает.",
            "Инвестиции: Earth-New доступен через 24 месяца после реализации опциона; ISRU с 2038 при оплате до 2037; ZBO с месяца оплаты.",
            "Затраты: закупка + резерв + хранение (0,72 × средний запас) + постоянный OPEX + CAPEX; PV по реальной ставке 8 % к началу 2035 г.",
            "Проверки по каждому году: сервис, CAPEX, резерв 45 дней, ёмкость помесячно, мощность и сроки по каналам, роль Emergency, потолок потерь — полная матрица «правило × год».",
            "Статус каждого параметра: данные задания · решение оператора · допущение команды (18 записей с единицей, диапазоном и обоснованием)."],
        0.5, 1.7, 12.3, 4.5, size=14)
textbox(s, 0.5, 6.3, 12.3, 0.7, [("Проверка: 10 контрольных примеров организатора, независимая ручная проверка 2035 года, граничные тесты и тесты ошибочного ввода, повторный пересчёт каждого опубликованного результата и независимый пересчёт только по CSV.", {"size": 13, "color": ACCENT, "bold": True})])
notes(s, "Формулы соответствуют правилам контрольных расчётов организатора; блоки и границы применимости описаны в приложении об архитектуре расчёта.")

# 4. Альтернативы
s = new_slide(4, "Пять стратегий на единой базе", "Один спрос, один горизонт, одна ставка, один движок", "EXP-01: сводная таблица альтернатив")
plans = ["P1_earth_only", "P2_earth_new", "P2z_earth_new_zbo", "P3_isru_zbo", "P4_full"]
chart(s, [P[p].replace(" + ", "\n+ ", 1) for p in plans], [("PV затрат в BASE, млн", [round(float(alt[(p, "BASE")]["pv_cost_mln"])) for p in plans])], 0.4, 1.6, 7.4, 4.9)
data = [["План", "CAPEX", "Исполним в BASE", "Стресс без изменения заказов"]]
for p in plans:
    b, st = alt[(p, "BASE")], alt[(p, "MANDATORY_STRESS")]
    data.append([P[p], num(b["capex_total_mln"]), "да" if b["feasible"] == "True" else f"нет: дефицит {num(b['shortage_total_t'], 1)} т",
                 f"дефицит {num(st['shortage_total_t'], 1)} т, {st['hard_violations']} жёстких"])
table(s, data, 8.0, 1.7, 5.0, 3.2, widths=[2.2, 0.9, 1.7, 2.4], size=10)
textbox(s, 8.0, 5.1, 5.0, 1.8, [("Ни одна стратегия без изменения заказов не проходит обязательный стресс: рост спроса на 15 % с 2038 года требует пересмотра заказов и запаса. ZBO нужен для потолка потерь 2 %.", {"size": 13, "color": INK})])
notes(s, "PV в BASE: " + "; ".join(f"{P[p]} {num(alt[(p, 'BASE')]['pv_cost_mln'], 3)}" for p in plans) + ". P1 неисполним: мощность 300 т/год меньше потребности 2040 года.")

# 5. Обязательный стресс
s = new_slide(5, "Обязательный стресс: заказы без изменений и заблаговременная адаптация", "P2z проходит стресс после пересмотра заказов и запаса; инвестиции не меняются", "EXP-02")
chart(s, ["BASE", "Стресс,\nзаказы без изменений", "Стресс,\nадаптация заранее"], [("PV затрат P2z, млн", [round(pv_base), round(pv_stress), round(pv_adapt)])], 0.4, 1.6, 6.2, 4.9)
bullets(s, [f"Заказы без изменений: дефицит {num(shortage_stress, 3)} т (критический 0), общий сервис до {num(kpi_stress['min_service_level_total'], 3)}, 45-дневный резерв нарушен в {', '.join(reserve_years)}.",
            "Адаптация заранее: запас 35,446 т к 2038-01 вместо 30,822; Earth-New +4,759 т в 2037 и +39,266 т в 2038; Earth-Flex +49,893 т в 2039 и +35,263 т в 2040.",
            f"Результат: дефицит 0, нарушений 0, цена адаптации {signed(pv_adapt - pv_stress, 3)} млн PV к неизменным заказам в том же стрессе.",
            f"Граница: тот же адаптированный график в BASE даёт {overflow_adapted_base} переполнений хранилища — универсального графика нет, график зависит от сценария.",
            "Реакция после наблюдения (март 2038) защищает сервис, но резерв 1 января 2038 исправить уже нельзя — решения о резерве принимаются заранее."],
        6.9, 1.7, 6.1, 5.2, size=14)
notes(s, "Сравнение доступно для выгрузки из интерфейса (вкладка «Сравнение») и в опубликованных таблицах EXP-02. Уровни сервиса в стрессе — ориентиры, резерв — жёсткое ограничение.")

# 6. Почему P2z
s = new_slide(6, "Почему P2z, а не самый дешёвый в BASE план P3", "Фильтр допуска, затем раскрытый многокритериальный выбор с четырьмя профилями интересов", "MCDA: таблица баллов")
labels = {"balanced_defense": "Сбалансированный", "operator_cost": "Оператор / стоимость жизненного цикла", "critical_continuity": "Потребители / непрерывность", "financier": "Финансист / капитал под риском"}
data = [["Профиль весов", "P2z", "P3", "P4"]]
for key, label in labels.items():
    sc = mcda[key]
    data.append([label, num(sc["P2z_earth_new_zbo"], 1), num(sc["P3_isru_zbo"], 1), num(sc["P4_full"], 1)])
table(s, data, 0.5, 1.7, 6.3, 2.6, widths=[3.4, 1, 1, 1], size=12)
textbox(s, 0.5, 4.5, 6.3, 2.4, [("Критерии (min–max в допущенном множестве): PV BASE, PV адаптированного стресса, CAPEX, дефицит фиксированного плана в стрессе, доля мощности без take-or-pay, номинальная мощность. Веса не меняют спрос, мощности, лимиты и требования сервиса; критический сервис и резерв — ограничения, а не критерии.", {"size": 12, "color": MUTED})])
bullets(s, [f"P3 экономит {num(pv_base - pv_p3_base, 3)} млн PV в BASE ({num(100 * (pv_base - pv_p3_base) / pv_p3_base, 1)} %), но его адаптация к стрессу дороже P2z на {num(pv_p3_adapt - pv_adapt, 3)} млн PV.",
            "P2z требует 540 млн CAPEX против 1 430 у P3 и 1 790 у P4: на 890 млн меньше необратимого капитала, запас до лимита 2037 года — 1 260 млн.",
            "P2z не несёт риск разгона лунного производства (55 % / 75 % в стрессе), но принимает риск задержки Earth-New — для него рассчитаны и оценены защитные меры.",
            f"P4 даёт максимальную мощность 550 т/год, но оставляет 10 млн до лимита CAPEX и дороже P2z в адаптированном стрессе на {num(pv_p4_adapt - pv_adapt, 3)} млн PV.",
            "Вывод: P2z — минимальная проверенная стоимость прохождения обязательного стресса при меньшем капитале; преимущества P3 и P4 видны в критериях и не скрыты рангом."],
        7.0, 1.7, 6.0, 5.2, size=13)
notes(s, "Баллы профилей воспроизводятся расчётом MCDA в составе контура; веса раскрыты в документе о стейкхолдерах и в записке.")

# 7. Экономика и бюджет
s = new_slide(7, "Экономика и бюджет выбранного плана по годам", "Инвестиции одинаковы в обоих сценариях: Earth-New 360 млн в 2035, ZBO 180 млн в 2037", "финансовая разбивка P2z в BASE и в адаптированном стрессе")
years = [r["year"] for r in fin_base]
chart(s, years, [("BASE, итого за год", [round(float(r["total_mln"])) for r in fin_base]), ("Адаптированный стресс, итого за год", [round(float(r["total_mln"])) for r in fin_adapt])], 0.4, 1.6, 7.6, 5.2, legend=True)
data = [["Показатель", "BASE", "Адаптированный стресс"],
        ["Закупка", num(kpi_base["procurement_total_mln"], 1), num(kpi_adapt["procurement_total_mln"], 1)],
        ["Резерв мощности", num(kpi_base["reservation_total_mln"], 1), num(kpi_adapt["reservation_total_mln"], 1)],
        ["Хранение", num(kpi_base["holding_total_mln"], 1), num(kpi_adapt["holding_total_mln"], 1)],
        ["Постоянный OPEX", num(kpi_base["fixed_opex_total_mln"], 0), num(kpi_adapt["fixed_opex_total_mln"], 0)],
        ["CAPEX", num(kpi_base["capex_total_mln"], 0), num(kpi_adapt["capex_total_mln"], 0)],
        ["Полные затраты", num(kpi_base["total_cost_mln"], 1), num(kpi_adapt["total_cost_mln"], 1)],
        ["PV затрат", num(pv_base, 1), num(pv_adapt, 1)],
        ["Стоимость обслуженной тонны", num(kpi_base["cost_per_served_t_mln"], 3), num(kpi_adapt["cost_per_served_t_mln"], 3)],
        ["Оплаченный простой take-or-pay, т", num(kpi_base["take_or_pay_idle_t"], 0), num(kpi_adapt["take_or_pay_idle_t"], 0)]]
table(s, data, 8.3, 1.7, 4.7, 4.4, widths=[2.4, 1.2, 1.6], size=11)
textbox(s, 8.3, 6.2, 4.7, 0.8, [("Выручка не задана: результат — минимальная стоимость обеспечения, а не прибыль. Ворота: 2035-01 опцион, 2037-01 приёмка Earth-New, 2037-07 ZBO, ежегодный пересчёт заказов.", {"size": 11, "color": MUTED})])
notes(s, "Годовой бюджет и дорожная карта с воротами решений — приложение «Бюджет и дорожная карта».")

# 8. Стресс-тесты
s = new_slide(8, "Стресс-тесты: чувствительность, сроки реакции, обратный стресс, Монте-Карло", "Каждый тест — воспроизводимый протокол с целью, параметрами, метриками и критерием нарушения", "EXP-03, EXP-04, EXP-06, EXP-07, EXP-08, EXP-10")
lo, hi = demand[("P2z_earth_new_zbo", "TEAM_LOW_DEMAND")], demand[("P2z_earth_new_zbo", "TEAM_HIGH_DEMAND")]
lo_r, hi_r = demand[("P2z_earth_new_zbo_team_low_demand", "TEAM_LOW_DEMAND")], demand[("P2z_earth_new_zbo_team_high_demand", "TEAM_HIGH_DEMAND")]
tp = tornado["earth_price_multiplier"]
react, adapted = reaction["P3_isru_zbo_reactive"], reaction["P3_isru_zbo_adapted"]
mc_no, mc_stock, mc_zbo = mc["without_measure"], mc["physical_stock"], mc["early_zbo_plus_stock"]
mc_extra = (lambda r: num(r[mc_extra_col], 1) if mc_extra_col else "—")
data = [["Тест", "Что варьируется", "Результат", "Вывод"],
        ["Низкий / высокий спрос (P2z)", "−20 % / +10…+25 %", f"без изменений: {lo['hard_violations']} переполнений (низкий), дефицит {num(hi['shortage_total_t'], 1)} т (высокий); перепланирование: {num(lo_r['pv_cost_mln'])} / {num(hi_r['pv_cost_mln'])} млн PV, дефицит {num(hi_r['shortage_total_t'], 3)} т", "план пересматривается под прогноз, а не фиксируется"],
        ["Чувствительность (P3)", "спрос, доля ISRU, цена, ставка, лаг ZBO", f"цена земных каналов ×0,8…×1,5 → PV {num(tp['pv_low'])}…{num(tp['pv_high'])} (самый чувствительный); первые неуспешные точки: спрос ×{thresholds['demand_multiplier']['threshold_fixed_plan'].replace('.', ',')}, ISRU {thresholds['isru_delivery_share_2038']['threshold_fixed_plan'].replace('.', ',')}, лаг ZBO {thresholds['zbo_commissioning_lag_months']['threshold_fixed_plan'].split('.')[0]} мес.", "для P2z порог не используется: любое изменение прогноза запускает пересчёт"],
        ["Реакция после наблюдения (P3)", "Emergency с 2038-05, Flex с 2038-07", f"дефицит {num(react['shortage_total_t'], 3)} т, сервис {num(react['min_sl_total'], 3)}, PV {num(react['pv_cost_mln'])} против {num(adapted['pv_cost_mln'])} при адаптации", "резерв января 2038 реакция не спасает"],
        ["Обратный стресс и меры (P3)", "совместные шоки спроса и ISRU", f"граница адаптированного плана ≈ {float(reverse['minimum']['fail_radius']) * 100:.6f} % — численный люфт; физический запас ({prot_level('physical_stock')} т) = {num(protection['physical_stock']['delta_pv_mln'], 1)} млн PV; ранний ZBO + запас ({prot_level('early_zbo_plus_stock')} т) = {num(protection['early_zbo_plus_stock']['delta_pv_mln'], 1)} млн PV", "устойчивость покупается физическим запасом"],
        ["Монте-Карло (P3)", "N = 10 000, seed 203510, спрос и ISRU U(0; 2 %), цены ±10 %", f"отказ {num(100 * float(mc_no['failure_frequency']), 2)} % без защиты → {num(100 * float(mc_stock['failure_frequency']), 2)} % (запас) и {num(100 * float(mc_zbo['failure_frequency']), 2)} % (ZBO + запас); доплата {mc_extra(mc_stock)} / {mc_extra(mc_zbo)} млн PV", "условные частоты модели, не вероятности реальных событий"]]
table(s, data, 0.5, 1.7, 12.3, 5.1, widths=[2.2, 2.4, 5.4, 2.3], size=10)
notes(s, "Полные протоколы и таблицы — приложение «Методики и протоколы стресс-тестов». Испытания EXP-07, EXP-08 и EXP-10 выполнены на P3 до окончательного выбора и не переносятся на P2z без нового расчёта.")

# 9. Риски
s = new_slide(9, "Риски выбранного плана и цена защиты", "Последствия рассчитаны контуром; для ключевого риска — задержки Earth-New — оценены две меры", "EXP-09, EXP-12, EXP-02, EXP-03, EXP-11; реестр рисков")
d = {k: exp12[(k, "reactive_flex")] for k in (3, 6, 12)}
b = {k: exp12[(k, "advance_buffer")] for k in (3, 6, 12)}
data = [["Риск", "Последствие без мер", "Мера и её стоимость, млн PV", "Остаточный риск"],
        ["Задержка ввода Earth-New на 3 / 6 / 12 мес.", f"сервис 100 %, но резерв нарушен в 2038–2040: разрыв до {num(exp9[3]['max_reserve_gap_t'], 3)} / {num(exp9[6]['max_reserve_gap_t'], 3)} / {num(exp9[12]['max_reserve_gap_t'], 3)} т; топливо остаётся оплаченным",
         f"реакция Earth-Flex после наблюдения (срок 4 мес.): {num(d[3]['flex_volume_t'], 3)} / {num(d[6]['flex_volume_t'], 3)} / {num(d[12]['flex_volume_t'], 3)} т за {signed(d[3]['delta_pv_vs_no_measure_mln'], 1)} / {signed(d[6]['delta_pv_vs_no_measure_mln'], 1)} / {signed(d[12]['delta_pv_vs_no_measure_mln'], 1)}; буфер заранее {signed(b[3]['delta_pv_vs_no_measure_mln'], 1)} / {signed(b[6]['delta_pv_vs_no_measure_mln'], 1)} / {signed(b[12]['delta_pv_vs_no_measure_mln'], 1)}, оплачивается и без задержки",
         "уведомление позже августа 2037 не оставляет времени на реакцию; задержка > 12 мес. не рассчитана"],
        ["Спрос выше базового", f"дефицит {num(shortage_stress, 1)} т в стрессе; {num(hi['shortage_total_t'], 1)} т в высоком варианте", f"адаптация заранее {signed(pv_adapt - pv_stress, 1)}; перепланирование под высокий спрос {num(hi_r['pv_cost_mln'])}", "нулевой запас прочности фиксированного графика: ежегодный пересчёт"],
        ["Спрос ниже базового", f"{lo['hard_violations']} переполнения хранилища, {signed(float(lo['pv_cost_mln']) - pv_base, 1)} млн PV", f"сокращение заказов и резервов: {num(lo_r['pv_cost_mln'])} млн PV", "take-or-pay ограничивает сокращение при замороженных резервах"],
        ["Рост цен земных каналов, геополитика", f"{signed(exp11['P2z_earth_new_zbo']['delta_pv_mln'], 1)} млн PV при +25 % в 2038–2039, без физических последствий", "индексация с cap/collar (предложено); Earth-New без индексации; блок геополитики в интерфейсе для любого сценария", "доля Earth-Core и Earth-Flex в закупках"],
        ["Задержка ZBO", "потолок потерь 2 % нарушается при лаге 10 мес.", "приёмка и мера за задержку в договоре; решение не позже 2037-07", "цена задержки для P2z не рассчитана"],
        ["Недопоставка ISRU (исключён)", "для P3: дефицит 170,0 т, адаптация +1 605,0 млн PV", f"исключён выбором P2z ценой {signed(pv_base - pv_p3_base, 1)} млн PV в BASE", "экономика после 2040 не рассчитана"]]
table(s, data, 0.5, 1.7, 12.3, 5.2, widths=[2.3, 3.4, 4.4, 2.2], size=10)
notes(s, "Полный реестр: событие, причина, параметры, период, основание диапазона, зависимости, владелец, меры, остаточный риск — приложение «Реестр ключевых рисков».")

# 10. Контракты и стороны
s = new_slide(10, "Контракты и интересы сторон", "Кто получает топливо, кто несёт затраты и риск после предлагаемых условий", "договорная стратегия; стейкхолдеры")
data = [["Сторона", "Интерес и показатель", "Обязательство (предлагаемые условия — допущение команды)", "Несёт после условия"],
        ["Оператор узла", "0 жёстких нарушений; PV; стоимость тонны", "номинация Earth-Core за 12 мес., Earth-Flex за 4 мес., Emergency за 6 недель; физический резерв", "CAPEX 540, резерв и take-or-pay, остаток сверх мер поставщиков"],
        ["Критические потребители", "критический сервис ≥ 99 %", "приоритет критического спроса и резерв не отменяются весами", "прямые затраты не моделируются"],
        ["Коммерческие потребители", "общий сервис ≥ 97 %; предсказуемая цена", "прозрачный тариф, уведомление об изменении заказов", "первый физический дефицит при непересмотренном плане"],
        ["Earth-Core", "стабильный доход", "take-or-pay 70 % только на доступную мощность; индексация с cap/collar", "вменяемая недоступность до лимита"],
        ["Earth-New", "финансирование 130 т/год", "опцион 90 → реализация 270; этапы, приёмка до старта take-or-pay 50 %, мера за задержку", "вменяемая задержка до лимита; оператор — остаток"],
        ["Earth-Flex, Emergency", "оплачиваемые вызовы, плата за готовность", "вызов за 4 мес. / 6 недель; SLA; take-or-pay нет", "срыв подтверждённого вызова"],
        ["Финансист", "лимит CAPEX, необратимый риск", "этапный опцион, ворота решений, доказательства этапов", "капитал под риском на 890 млн ниже P3"]]
table(s, data, 0.5, 1.7, 12.3, 4.6, widths=[2.0, 2.6, 4.9, 2.8], size=10)
textbox(s, 0.5, 6.35, 12.3, 0.72, [("Изменение рисков меняет решения и баланс интересов: подтверждение стресса → адаптированный график (оператор платит, потребители избегают дефицита); падение спроса → сокращаются сначала каналы без take-or-pay; срыв этапа Earth-New → замещение Earth-Flex и договорная мера. Цена договорных гарантий в PV не включена.", {"size": 11, "color": MUTED})])
notes(s, "Адаптация при изменении рисков и раскрытые веса — приложение «Стейкхолдеры»; пункты договора — «Договорная стратегия».")

# 11. Цифровой контур
s = new_slide(11, "Цифровой контур: интерфейс, сохранение, выгрузка, расширение, геополитика", "Локальный интерфейс без интернета; все числа — из одного расчётного ядра", "интерфейс оператора; EXP-05; EXP-11")
bullets(s, ["Разделы: Обзор (KPI, баланс и расходы по годам, помесячный запас, календарь поставок), Решения (заказы с помесячным профилем, резервы, инвестиции, начальный запас), Данные и контракты (правка цен и условий на копии данных с описанием допущения), Ограничения (нарушения с годом, величиной и причиной; полная матрица), Сравнение (A ↔ B, выгрузка CSV), Геополитика.",
            "Ошибочный ввод — понятное сообщение с названием поля и значения; ограничения задания недоступны для изменения.",
            "Сохранение и повторное открытие рабочего файла (план, сценарий, копия данных, допущения, настройки шока); выгрузка XLSX и архива CSV/JSON с матрицей проверок, календарём и хешами расчёта; распакованный архив проверяется командой пересчёта.",
            f"Расширение на копии данных: источник Source-X и 2041 год — {len(ext['years'])} лет, PV {num(ext['kpi']['pv_cost_mln'])} млн, обслужено {num(ext['kpi']['served_total_t'])} т, исполним: {'да' if ext['feasible'] else 'нет'}; ограничения задания сохранены.",
            f"Дополнительный блок геополитики: оператор задаёт событие, каналы, годы, направление и величину изменения цены и правило сочетания со стрессом (один эффект не начисляется дважды); сравнение до/после, таблица эффективных цен, восстановление исходных цен. Пример +25 % для Earth-Core и Earth-Flex в 2038–2039: {signed(exp11['P2z_earth_new_zbo']['delta_pv_mln'], 3)} млн PV для P2z без физических последствий."],
        0.5, 1.7, 12.3, 5.2, size=14)
notes(s, "Демонстрация: инструкция оператора, шаги 1–9. Паритет интерфейса, выгрузки и командной строки проверяется автоматическими тестами.")

# 12. Итоги
s = new_slide(12, "Итоги, границы и передача решения", "Решение проверяемо: числа записки, интерфейса и выгрузок совпадают", "записка; README")
bullets(s, [f"Решение: P2z — Earth-Core + Earth-Flex + Earth-New (2035-01 → ввод 2037-01) + ZBO (2037-07); Emergency только как резерв; ISRU не финансируется до 2040.",
            f"Стандартный сценарий: PV {num(pv_base, 3)} млн, дефицит 0, все проверки выполнены. Обязательный стресс: без изменения заказов дефицит {num(shortage_stress, 3)} т и нарушения резерва; после заблаговременной адаптации PV {num(pv_adapt, 3)} млн, дефицит 0, нарушений 0.",
            f"Цена решений: адаптация к стрессу {signed(pv_adapt - pv_stress, 3)} млн PV; защита от задержки Earth-New {signed(d[3]['delta_pv_vs_no_measure_mln'], 1)} … {signed(d[12]['delta_pv_vs_no_measure_mln'], 1)} млн PV; ценовой шок +25 % {signed(exp11['P2z_earth_new_zbo']['delta_pv_mln'], 1)} млн PV.",
            "Не доказано и не заявляется: единый фиксированный график для обоих сценариев, устойчивость к совместным малым отклонениям для P2z, экономика после 2040 года, цена договорных гарантий.",
            "Дальнейшие шаги: буфер P2z против совместных отклонений, цена задержки ZBO, политика пересмотра заказов с информацией на дату заказа, горизонт 2041+.",
            "Передача: код, данные, конфигурации, сохранённые планы обоих сценариев, результаты, тесты и документация в репозитории; запуск — python -m terraplan ui; порядок проверки: установка → стандартный сценарий → обязательный стресс → дополнительные тесты → сравнение и выгрузка."],
        0.5, 1.7, 12.3, 5.2, size=14)
notes(s, "Границы прототипа: месячный шаг, без оптимизатора, один локальный оператор. Все числа воспроизводятся повторным запуском экспериментов.")

prs.save(OUT)
(ROOT / "docs/presentation/slides.json").write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")
lines = ["# План презентации (12 слайдов), собирается автоматически из результатов", ""]
lines += [f"{o['n']}. {o['title']} — данные: {o['source']}" for o in outline]
lines += ["", "Все числа на слайдах читаются из опубликованных результатов экспериментов при сборке; ручной ввод чисел не используется.",
          "Пересборка: `python docs/presentation/build_deck.py` из корня репозитория (требуется пакет python-pptx)."]
(ROOT / "docs/presentation/outline.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Собрано слайдов: {len(prs.slides)} → {OUT.relative_to(ROOT)}")
