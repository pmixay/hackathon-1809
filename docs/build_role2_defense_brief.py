"""Build the compact Role-2 defense brief PDF from repository evidence."""

from __future__ import annotations

import csv
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "role2_defense_brief_ru.pdf"

NAVY = colors.HexColor("#16324F")
TEAL = colors.HexColor("#0F766E")
GOLD = colors.HexColor("#D69E2E")
PALE_TEAL = colors.HexColor("#E6F4F1")
PALE_BLUE = colors.HexColor("#EDF4FA")
PALE_GOLD = colors.HexColor("#FFF7DF")
LIGHT = colors.HexColor("#F5F7F9")
MID = colors.HexColor("#D4DEE7")
TEXT = colors.HexColor("#18222D")
MUTED = colors.HexColor("#546575")
RED = colors.HexColor("#9B2C2C")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def fnum(value: str) -> float:
    return float(value)


def fmt(value: float, digits: int = 1) -> str:
    return f"{value:,.{digits}f}".replace(",", " ").replace(".", ",")


def load_evidence() -> dict[str, object]:
    alternatives = rows(ROOT / "results" / "alternatives" / "summary.csv")
    stress = rows(ROOT / "results" / "stress" / "summary.csv")
    scores = rows(ROOT / "results" / "strategy" / "mcda_scores.csv")

    a = {(r["plan_id"], r["scenario_id"]): r for r in alternatives}
    adapted_variants = {"adapted plan", "адаптированный план"}
    s = {
        (r["plan_id"], r["scenario_id"]): r
        for r in stress
        if r["variant"] in adapted_variants
    }
    selected = a[("P2z_earth_new_zbo", "BASE")]
    selected_fixed = a[("P2z_earth_new_zbo", "MANDATORY_STRESS")]
    selected_adapted = s[("P2z_earth_new_zbo_adapted", "MANDATORY_STRESS")]
    p3_base = a[("P3_isru_zbo", "BASE")]
    p3_adapted = s[("P3_isru_zbo_adapted", "MANDATORY_STRESS")]
    p4_adapted = s[("P4_full_adapted", "MANDATORY_STRESS")]
    return {
        "a": a,
        "selected": selected,
        "selected_fixed": selected_fixed,
        "selected_adapted": selected_adapted,
        "p3_base": p3_base,
        "p3_adapted": p3_adapted,
        "p4_adapted": p4_adapted,
        "scores": scores,
    }


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def page_decor(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 9 * mm, width, 9 * mm, fill=1, stroke=0)
    canvas.setFont("Arial", 7.5)
    canvas.setFillColor(colors.white)
    canvas.drawString(13 * mm, height - 6 * mm, "TERRAPLAN  /  ROLE 2  /  DEFENSE BRIEF")
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 13 * mm, 7 * mm, f"19.09.2026  |  page {doc.page}")
    canvas.setStrokeColor(MID)
    canvas.line(13 * mm, 10 * mm, width - 13 * mm, 10 * mm)
    canvas.restoreState()


def table(data, widths, header_rows=1, font_size=7.7, aligns=None) -> Table:
    header_style = ParagraphStyle(
        "table-header", fontName="Arial-Bold", fontSize=font_size,
        leading=font_size + 1.4, textColor=colors.white, wordWrap="CJK",
    )
    cell_style = ParagraphStyle(
        "table-cell", fontName="Arial", fontSize=font_size,
        leading=font_size + 1.9, textColor=TEXT, wordWrap="CJK",
    )
    wrapped = []
    for row_no, row in enumerate(data):
        wrapped.append([
            value if isinstance(value, Paragraph) else Paragraph(escape(str(value)), header_style if row_no < header_rows else cell_style)
            for value in row
        ])
    t = Table(wrapped, colWidths=widths, repeatRows=header_rows, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, header_rows - 1), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, header_rows - 1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, MID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for row in range(header_rows, len(data)):
        commands.append(("BACKGROUND", (0, row), (-1, row), LIGHT if row % 2 else colors.white))
    if aligns:
        for col, align in enumerate(aligns):
            commands.append(("ALIGN", (col, header_rows), (col, -1), align))
    t.setStyle(TableStyle(commands))
    return t


def main() -> None:
    pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
    evidence = load_evidence()
    selected = evidence["selected"]
    fixed = evidence["selected_fixed"]
    adapted = evidence["selected_adapted"]
    p3_base = evidence["p3_base"]
    p3_adapted = evidence["p3_adapted"]
    p4_adapted = evidence["p4_adapted"]
    alt = evidence["a"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUT), pagesize=A4, rightMargin=13 * mm, leftMargin=13 * mm,
        topMargin=15 * mm, bottomMargin=15 * mm, title="TerraPlan Role 2 defense brief",
        author="TerraPlan",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="brief-frame")
    doc.addPageTemplates(PageTemplate(id="brief", frames=[frame], onPage=page_decor))
    base = getSampleStyleSheet()
    title = ParagraphStyle("title", parent=base["Title"], fontName="Arial-Bold", fontSize=22,
                           leading=24, textColor=NAVY, alignment=TA_LEFT, spaceAfter=5)
    subtitle = ParagraphStyle("subtitle", parent=base["Normal"], fontName="Arial", fontSize=10,
                              leading=13, textColor=MUTED, spaceAfter=8)
    h1 = ParagraphStyle("h1", parent=base["Heading1"], fontName="Arial-Bold", fontSize=15,
                        leading=18, textColor=NAVY, spaceBefore=2, spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=base["Heading2"], fontName="Arial-Bold", fontSize=10.5,
                        leading=13, textColor=TEAL, spaceBefore=5, spaceAfter=4)
    body = ParagraphStyle("body", parent=base["BodyText"], fontName="Arial", fontSize=8.8,
                          leading=11.8, textColor=TEXT, spaceAfter=4)
    small = ParagraphStyle("small", parent=body, fontSize=7.3, leading=9.3, textColor=MUTED)
    callout = ParagraphStyle("callout", parent=body, fontName="Arial-Bold", fontSize=11.3,
                             leading=14, textColor=NAVY, borderColor=TEAL, borderWidth=1,
                             borderPadding=7, backColor=PALE_TEAL, spaceAfter=8)
    q = ParagraphStyle("q", parent=body, fontName="Arial-Bold", fontSize=8.8, leading=11, textColor=NAVY,
                       spaceBefore=3, spaceAfter=1)

    story = []
    story += [Spacer(1, 3 * mm), p("Финальная стратегия TerraPlan", title),
              p("Краткий бриф для руководителя и спикера - роль экономиста (R2)", subtitle)]

    base_gap = fnum(selected["pv_cost_mln"]) - fnum(p3_base["pv_cost_mln"])
    stress_saving = fnum(p3_adapted["pv_cost_mln"]) - fnum(adapted["pv_cost_mln"])
    capex_saving = fnum(p3_base["capex_total_mln"]) - fnum(selected["capex_total_mln"])
    p4_saving = fnum(p4_adapted["pv_cost_mln"]) - fnum(adapted["pv_cost_mln"])

    story.append(p(
        "<b>Выбор: P2z = Earth-New + ZBO, с пересматриваемыми заказами.</b><br/>"
        "Это не один фиксированный график на все случаи: архитектура постоянна, а объёмы A/B/C/E меняются "
        "по заранее заданным воротам спроса, цены и готовности мощности.", callout))

    kpis = [
        [p("Ключевой факт", small), p("Значение", small), p("Что сказать жюри", small)],
        ["PV в BASE", fmt(fnum(selected["pv_cost_mln"]), 3), f"Только на {fmt(base_gap, 3)} дороже P3."],
        ["PV адаптации к стрессу", fmt(fnum(adapted["pv_cost_mln"]), 3), f"На {fmt(stress_saving, 3)} дешевле P3 и на {fmt(p4_saving, 3)} дешевле P4."],
        ["CAPEX", fmt(fnum(selected["capex_total_mln"]), 0), f"На {fmt(capex_saving, 0)} ниже P3; запас до лимита 2037 = 1 260."],
        ["Сервис после адаптации", "100% / 100%", "Общий и критический спрос обслужены полностью; hard-нарушений 0."],
        ["Если заказы не менять", f"дефицит {fmt(fnum(fixed['shortage_total_t']), 3)} т", "Доказательство необходимости адаптации, а не провал выбранной архитектуры."],
        ["Граница", "2035-2040", "Преимущества ISRU после 2040 не рассчитаны и не используются как аргумент."],
    ]
    story += [table(kpis, [39 * mm, 34 * mm, 100 * mm], font_size=7.6), Spacer(1, 4 * mm)]

    story += [p("Аргумент в 25 секунд", h2), p(
        f"P3 минимален только в BASE: его преимущество {fmt(base_gap, 3)} млн PV, около 1%. "
        f"В обязательном стрессе адаптированный P2z дешевле P3 на {fmt(stress_saving, 3)} млн PV, "
        f"требует на {fmt(capex_saving, 0)} млн меньше необратимого CAPEX и не зависит от первого цикла ISRU. "
        "P4 даёт больше мощности, но почти исчерпывает лимит CAPEX. Поэтому P2z - лучший баланс цены, "
        "исполняемости и капитала на официальном горизонте.", body)]

    pros = [
        ["План", "Плюс", "Минус / почему не финал"],
        ["P1", "Самый низкий номинальный PV", f"Неисполним в BASE: дефицит {fmt(fnum(alt[('P1_earth_only','BASE')]['shortage_total_t']), 1)} т."],
        ["P2", "Низкий CAPEX, BASE исполним", "Без ZBO нарушает потолок потерь в стрессе; адаптация не доказана."],
        ["P2z", "Лучшие стресс-PV и CAPEX; нет ISRU-риска", "Риск задержки Earth-New; TOP C = 50%; нужен пересмотр заказов."],
        ["P3", "Самый дешёвый BASE; высокая no-TOP гибкость", "CAPEX +890 к P2z; стресс-адаптация дороже на 539,183."],
        ["P4", "Максимум обычной мощности: 550 т/год", "CAPEX 1 790: только 10 до лимита; стресс-PV выше P2z."],
    ]
    story += [p("Плюсы и минусы - мгновенно", h2), table(pros, [17 * mm, 67 * mm, 89 * mm], font_size=7.25)]

    story.append(PageBreak())
    story += [Spacer(1, 2 * mm), p("MCDA: решение можно пересчитать", h1), p(
        "Сначала жёсткий фильтр: BASE и адаптированный обязательный стресс должны быть исполнимы. "
        "P1/P2 не оцениваются. P2z/P3/P4 после адаптации дают 100% общего и критического сервиса; "
        "веса не могут компенсировать нарушение сервиса или 45-дневного резерва.", body)]

    metrics = [
        ["Архитектура", "BASE PV", "Стресс PV", "CAPEX", "Дефицит без пересмотра", "Без TOP", "Мощность"],
        ["P2z", "8 729,4", "10 097,5", "540", "95,9 т", "25,6%", "430"],
        ["P3", "8 638,9", "10 636,7", "1 430", "170,0 т", "54,8%", "420"],
        ["P4", "8 857,6", "10 578,2", "1 790", "170,0 т", "41,8%", "550"],
    ]
    story += [table(metrics, [25 * mm, 25 * mm, 26 * mm, 18 * mm, 36 * mm, 22 * mm, 21 * mm], font_size=7.2,
                    aligns=["LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"]), Spacer(1, 4 * mm)]

    profile_labels = {
        "balanced_defense": "Сбалансированный",
        "operator_cost": "Оператор / стоимость",
        "critical_continuity": "Потребители / непрерывность",
        "financier": "Финансист / капитал",
    }
    score_map = {}
    for row in evidence["scores"]:
        score_map.setdefault(row["profile"], {})[row["plan_id"]] = float(row["score_0_100"])
    score_table = [["Профиль", "P2z", "P3", "P4", "Победитель"]]
    for pid in profile_labels:
        vals = score_map[pid]
        score_table.append([
            profile_labels[pid], f"{vals['P2z_earth_new_zbo']:.1f}", f"{vals['P3_isru_zbo']:.1f}",
            f"{vals['P4_full']:.1f}", "P2z",
        ])
    story += [p("Итоговые баллы 0-100", h2), table(score_table, [66 * mm, 22 * mm, 22 * mm, 22 * mm, 41 * mm], font_size=7.8,
                    aligns=["LEFT", "RIGHT", "RIGHT", "RIGHT", "CENTER"]), Spacer(1, 3 * mm)]

    weights = [
        ["Критерий", "Баланс", "Оператор", "Потребители", "Финансист"],
        ["BASE PV", "15%", "20%", "5%", "20%"],
        ["Адаптированный стресс PV", "25%", "30%", "10%", "15%"],
        ["CAPEX", "20%", "15%", "5%", "40%"],
        ["Дефицит без пересмотра", "20%", "15%", "45%", "10%"],
        ["Доля мощности без TOP", "10%", "10%", "15%", "10%"],
        ["Обычная мощность", "10%", "10%", "20%", "5%"],
    ]
    story += [p("Раскрытые веса", h2), table(weights, [70 * mm, 24 * mm, 27 * mm, 27 * mm, 25 * mm], font_size=7.4,
                    aligns=["LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"])]

    story += [Spacer(1, 4 * mm), p("Как отвечать на критику MCDA", h2), p(
        "Баллы не доказывают абсолютный оптимум и не являются вероятностями. Они показывают, что вывод не "
        "держится на одном удобном наборе весов: P2z лидирует у оператора, потребителей, финансиста и в "
        "сбалансированном профиле. Сильные стороны соперников не скрыты: P3 лучше в BASE и гибкости, P4 - "
        "в мощности. Исходники: configs/mcda_profiles.yaml, experiments/run_mcda.py, results/strategy/.", body)]

    story.append(PageBreak())
    story += [Spacer(1, 2 * mm), p("Контракт: кто несёт какой риск", h1), p(
        "Главный принцип: TOP платится, когда поставщик реально сделал мощность доступной, но оператор не выбрал "
        "объём. Если мощность недоступна по вине поставщика, этот объём исключается из TOP и включается remedy.", callout)]

    contracts = [
        ["Риск", "Пункт", "Механизм", "Остаточный носитель риска"],
        ["Спрос ниже", "2.1-2.2", "Сократить E/B, затем C сверх 50% и A сверх 70%; не допускать overflow.", "Оператор: прогноз, резерв, неизбежный TOP."],
        ["Спрос выше", "2.3", "B за 4 месяца, E за 6 недель; подтверждение reserved capacity.", "Оператор - поздний заказ; поставщик - подтверждённый недовоз."],
        ["Earth-New задержан", "4.1-4.3", "Этапы, независимая приёмка, replacement/LD в согласованном лимите.", "C-поставщик до cap; оператор/страховщик - хвост и timely substitution."],
        ["Цена Земли", "5.1-5.3", "Публичный индекс, cap/collar, reopener вне диапазона.", "Внутри band - оператор; capped tail - поставщик; дальше переговоры."],
        ["ZBO задержан", "6.1-6.2", "Приёмка по storage/loss KPI, cure plan, delay damages.", "EPC до cap; оператор - дополнительное топливо и остаток."],
        ["Emergency недоступен", "7.1-7.2", "6-недельный SLA и remedy; запас обязан покрыть ожидание.", "E-поставщик - confirmed-call failure; оператор - standby и bridge stock."],
    ]
    story += [table(contracts, [30 * mm, 18 * mm, 70 * mm, 55 * mm], font_size=6.9)]

    story += [Spacer(1, 4 * mm), p("Критерии 17-18: интересы и адаптация", h2)]
    adapt = [
        ["Сторона", "Что защищаем", "Что меняется при риске"],
        ["Критические потребители", "99% сервис + приоритет + 45 дней", "Это hard gate: весами ухудшение не компенсируется."],
        ["Коммерческие", "97% общий сервис и предсказуемая цена", "Адаптация убирает 95,917 т дефицита; без неё shortage ложится первым на них."],
        ["Оператор", "Минимум PV при 0 hard violations", "Платит гибкость/буфер, но получает remedies за supplier fault."],
        ["Финансист", "Лимит CAPEX и stage gates", "540 млн CAPEX и 1 260 млн headroom вместо 1 430/1 790."],
        ["Поставщики A/B/C/E", "Понятные minimums и call-offs", "A/C сохраняют TOP floors; B/E получают премию за гибкость; supplier fault остаётся у поставщика."],
        ["ISRU-поставщик", "Будущий рынок", "Не финансируется сейчас; возвращается на новом post-2040 gate с данными зрелости."],
    ]
    story += [table(adapt, [40 * mm, 60 * mm, 73 * mm], font_size=7.05)]

    story += [Spacer(1, 4 * mm), p("Критические триггеры", h2), p(
        "Stress outlook до 2038 -> перейти на tested adapted P2z. Низкий спрос -> резать no-TOP раньше TOP. "
        "Milestone slip C -> substitute B/E + физический буфер + clause 4 claim. Reserve forecast близок к 45 "
        "дням -> запас имеет приоритет над баллом MCDA. Post-2040 growth -> новая оценка ISRU/P4.", body)]

    story.append(PageBreak())
    story += [Spacer(1, 2 * mm), p("Ответы на вероятные вопросы жюри", h1)]

    qa = [
        ("Почему не P3, если он самый дешёвый?", f"Он дешевле только в BASE на {fmt(base_gap, 3)} млн PV. В адаптированном обязательном стрессе P3 дороже на {fmt(stress_saving, 3)} млн PV и требует +{fmt(capex_saving, 0)} млн CAPEX. Мы покупаем устойчивость к заданному риску почти без потери BASE-экономики."),
        ("Почему не P4 - максимальная диверсификация?", "P4 даёт 550 т/год обычной мощности, но CAPEX 1 790 оставляет 10 млн до лимита 2037 и всё равно требует адаптации. Его стресс-PV выше P2z на 480,756 млн."),
        ("Вы называете P2z робастным?", "Нет. Мы защищаем архитектуру и правило адаптации, не один заказной план. Exact adapted P2z проходит стресс, но имеет лишь 0,000469 т запаса над резервом января 2040; в BASE тот же график даёт 17 overflow violations."),
        ("Что если Earth-New опоздает?", "EXP-09: задержки 3/6/12 месяцев не создают дефицит, но нарушают резерв 2038-2040. Поэтому milestone/acceptance/LD, ранний физический buffer и своевременные B/E call-offs являются частью стратегии."),
        ("Почему контрактный резерв не равен физическому?", "Emergency требует 6 недель. Контракт считается эквивалентом только если физический запас покрывает ожидание и зарезервированная E-мощность не меньше нормы. Иначе RESERVE_45D нарушен."),
        ("Где прибыль и окупаемость?", "Их нет в выводе: организатор не дал выручку или цену срыва миссии. Мы сравниваем PV стоимости обеспечения, CAPEX, сервис и риск, а не заявляем NPV бизнеса."),
        ("Не подобраны ли веса под P2z?", "Веса раскрыты до результата в четырёх профилях. P2z выигрывает во всех. Hard gates применены до MCDA, а преимущества P3/P4 показаны отдельно. Скрипт воспроизводим."),
        ("Что реально доказали внешние источники?", "Метод: stage gates, capacity options, quantity flexibility, TOP risk allocation и ZBO acceptance. Они не доказывают ни цены, ни CAPEX, ни 1,2% потерь кейса - эти числа только CASE_INPUT."),
        ("Как меняется решение после 2040?", "Пока никак: это граница данных. В 2040 открываем новый gate и сравниваем ISRU/P4 с расширенным спросом, зрелостью технологии и новой контрактной ценой."),
    ]
    for question, answer in qa:
        story.append(KeepTogether([p(question, q), p(answer, body)]))

    story += [Spacer(1, 3 * mm), p("Где проверять", h2), p(
        "Решение и аргумент: docs/management_note.md. MCDA: results/strategy/summary.md. Контракт: "
        "docs/contract_strategy.md. Критерии 17-18: docs/stakeholders.md. Числа: "
        "results/alternatives/summary.csv и results/stress/summary.csv. Источники и ограничения: docs/sources.md.", small)]
    story += [p(
        "Финальная фраза: P2z - не самая модная технология и не самый дешёвый BASE. Это минимальная проверенная "
        "стоимость полного исполнения обязательного стресса при существенно меньшем необратимом капитале, "
        "с явным владельцем каждого остаточного риска.", callout)]

    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    main()
