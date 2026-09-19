"""Сборка финальных документов с проверяемым объёмом: управленческая записка и одностраничное резюме.

Зачем. Кейс требует управленческую записку объёмом 8–12 страниц и отдельное одностраничное резюме
сравнения сценариев. Markdown сам по себе объёма не имеет, поэтому здесь задана **фиксированная
вёрстка**, в которой число страниц вычисляется детерминированно и проверяется:

    страница A4, поля 20 мм, моноширинный шрифт 10,5 pt, одинарный интервал
    -> 96 знаков в строке, 52 строки на странице

Тот же макет выводится и в печатный HTML (`@page A4`, тот же шрифт и те же поля), поэтому число
страниц, напечатанное здесь, совпадает с тем, что увидит читатель при печати.

Что считается объёмом записки. Разделы 1–15 — тело записки. Приложения кейс прямо разрешает выносить
(«Схемы и подробные таблицы могут быть приложениями со ссылками из записки»), поэтому блок
«Приложения» и подробные таблицы, помеченные в тексте как приложение, собираются отдельным файлом
и в объём тела не входят.

Запуск:  python docs/build_note.py [--check]
Коды возврата: 0 — объём в требуемых границах; 1 — вне границ (при --check).
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "build"

WIDTH = 96              # знаков в строке
LINES_PER_PAGE = 52     # строк на странице
NOTE_PAGES = (8, 12)    # требование кейса к управленческой записке
ONE_PAGER_PAGES = (1, 1)


def layout_lines(markdown: str) -> list[str]:
    """Разложить Markdown в строки фиксированной ширины.

    Абзац переливается целиком, а не построчно: переносы строк в исходном Markdown — это разметка
    автора, а не вёрстка, и учитывать их как разрывы строк означало бы считать страницы по случайной
    ширине исходника. Таблицы, блоки кода и заголовки переливанию не подлежат.
    """
    lines: list[str] = []
    in_code = False
    paragraph: list[str] = []

    def flush(bullet: bool = False) -> None:
        if not paragraph:
            return
        text = " ".join(x.strip() for x in paragraph)
        indent = "  " if bullet else ""
        lines.extend(textwrap.wrap(text, width=WIDTH, subsequent_indent=indent) or [""])
        paragraph.clear()

    bullet_open = False
    for raw in markdown.splitlines():
        if raw.startswith("```"):
            flush(bullet_open); bullet_open = False
            in_code = not in_code
            lines.append(raw)
            continue
        if in_code or raw.lstrip().startswith("|"):
            flush(bullet_open); bullet_open = False
            # таблица или код: длинная строка занимает столько строк макета, сколько реально нужно
            lines.extend([raw[i:i + WIDTH] for i in range(0, max(len(raw), 1), WIDTH)] or [""])
            continue
        if not raw.strip():
            flush(bullet_open); bullet_open = False
            lines.append("")
            continue
        if raw.startswith("#"):
            flush(bullet_open); bullet_open = False
            lines.append("")
            marker, _, title = raw.partition(" ")
            wrapped = textwrap.wrap(raw, width=WIDTH, subsequent_indent=" " * (len(marker) + 1)) or [raw]
            lines.extend(wrapped)
            continue
        # маркер списка — только «- », «* » или «> »; «**жирный текст**» списком не является
        stripped = raw.lstrip()
        starts_item = bool(re.match(r"^(?:[-*>]\s|\d+\.\s)", stripped)) and not stripped.startswith("**")
        if starts_item:
            flush(bullet_open)
            bullet_open = True
        paragraph.append(raw)
    flush(bullet_open)
    return lines


def paginate(lines: list[str]) -> list[list[str]]:
    pages, page = [], []
    for line in lines:
        if line.startswith("## ") and len(page) > LINES_PER_PAGE - 6:
            pages.append(page)          # висячий заголовок: раздел не начинается в последних строках страницы
            page = []
        page.append(line)
        if len(page) >= LINES_PER_PAGE:
            pages.append(page)
            page = []
    if page:
        pages.append(page)
    return pages


APPENDIX_START = re.compile(r"<!--\s*appendix:start\s+«(?P<title>[^»]+)»(?:\s+ref=(?P<ref>\S+))?\s*-->")
APPENDIX_END = "<!-- appendix:end -->"


def extract_appendix_blocks(markdown: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Вынести помеченные подробные таблицы в приложение, оставив в теле ссылку на них.

    Кейс: «Схемы и подробные таблицы могут быть приложениями со ссылками из записки». Разметка
    хранится в Markdown комментариями, поэтому исходный документ на GitHub читается целиком,
    а в собранной записке те же таблицы печатаются приложением — без дублирования содержания.
    """
    blocks: list[tuple[str, str, str]] = []
    out, lines, i = [], markdown.splitlines(), 0
    while i < len(lines):
        m = APPENDIX_START.match(lines[i].strip())
        if not m:
            out.append(lines[i]); i += 1; continue
        title, ref = m.group("title"), m.group("ref") or ""
        i += 1
        body = []
        while i < len(lines) and lines[i].strip() != APPENDIX_END:
            body.append(lines[i]); i += 1
        i += 1
        n = len(blocks) + 1
        blocks.append((f"П{n}. {title.split('. ', 1)[-1]}" if title.startswith("П") else title, "\n".join(body), ref))
        out.append(f"> Подробности — приложение «{title}»"
                   + (f"; полная версия — `{ref}`." if ref else "."))
    return "\n".join(out), blocks


def split_body_and_appendices(markdown: str) -> tuple[str, str]:
    """Тело записки (разделы 1–15) и приложения; кейс разрешает выносить приложения отдельно."""
    body, blocks = extract_appendix_blocks(markdown)
    marker = "\n## Приложения"
    tail = ""
    if marker in body:
        i = body.index(marker)
        body, tail = body[:i], body[i:]
    parts = [tail] if tail.strip() else ["## Приложения", ""]
    for title, table, ref in blocks:
        parts += ["", f"### {title}", ""]
        if ref:
            parts.append(f"Полная версия — `{ref}`.")
            parts.append("")
        parts.append(table)
    return body, "\n".join(parts)


def write_text(pages: list[list[str]], path: Path, title: str) -> None:
    out = []
    for n, page in enumerate(pages, 1):
        out.append("\n".join(page).rstrip())
        out.append(f"\n{'':<{WIDTH - 20}}— {n} из {len(pages)} —\n" + "\f")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{title}\n\n" + "\n".join(out), encoding="utf-8")


def write_html(pages: list[list[str]], path: Path, title: str) -> None:
    """Печатный HTML с тем же макетом: A4, поля 20 мм, моноширинный 10,5 pt."""
    body = []
    for n, page in enumerate(pages, 1):
        text = html.escape("\n".join(page).rstrip())
        body.append(f'<section class="page"><pre>{text}</pre>'
                    f'<footer>— {n} из {len(pages)} —</footer></section>')
    path.write_text(
        "<!doctype html>\n<html lang=\"ru\"><head><meta charset=\"utf-8\">\n"
        f"<title>{html.escape(title)}</title>\n<style>\n"
        "@page { size: A4; margin: 20mm; }\n"
        "html, body { margin: 0; padding: 0; background: #fff; color: #111; }\n"
        "body { font-family: 'DejaVu Sans Mono', 'Courier New', monospace; font-size: 10.5pt; line-height: 1.0; }\n"
        ".page { width: 96ch; margin: 0 auto 8mm; padding: 0; page-break-after: always; position: relative; }\n"
        ".page:last-child { page-break-after: auto; }\n"
        "pre { margin: 0; white-space: pre-wrap; word-wrap: break-word; font: inherit; }\n"
        "footer { text-align: right; color: #666; padding-top: 6pt; }\n"
        "@media screen { body { padding: 8mm; background: #f4f4f4; } .page { background: #fff; padding: 10mm; box-shadow: 0 1px 4px rgba(0,0,0,.15); } }\n"
        "</style></head><body>\n" + "\n".join(body) + "\n</body></html>\n",
        encoding="utf-8")


def build(source: Path, stem: str, limits: tuple[int, int], title: str, split: bool) -> tuple[int, bool]:
    markdown = source.read_text(encoding="utf-8")
    body, appendices = split_body_and_appendices(markdown) if split else (markdown, "")
    pages = paginate(layout_lines(body))
    write_text(pages, OUT / f"{stem}.txt", title)
    write_html(pages, OUT / f"{stem}.html", title)
    if appendices.strip():
        app_pages = paginate(layout_lines(appendices))
        write_text(app_pages, OUT / f"{stem}_appendices.txt", title + " — приложения")
        write_html(app_pages, OUT / f"{stem}_appendices.html", title + " — приложения")
    lo, hi = limits
    ok = lo <= len(pages) <= hi
    print(f"{stem:22s} {len(pages):3d} стр.  требуется {lo}–{hi}  {'ОК' if ok else 'ВНЕ ГРАНИЦ'}"
          + (f"  (+ приложения {len(paginate(layout_lines(appendices)))} стр., в объём не входят)"
             if appendices.strip() else ""))
    return len(pages), ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="ненулевой код возврата, если объём вне границ")
    args = ap.parse_args()
    print(f"Фиксированная вёрстка: A4, поля 20 мм, моноширинный 10,5 pt -> {WIDTH} знаков × {LINES_PER_PAGE} строк на странице\n")
    _, ok_note = build(ROOT / "docs" / "management_note.md", "management_note", NOTE_PAGES,
                       "TerraPlan — управленческая записка", split=True)
    _, ok_one = build(ROOT / "docs" / "one_pager_scenarios.md", "one_pager", ONE_PAGER_PAGES,
                      "TerraPlan — одностраничное резюме сравнения сценариев", split=False)
    print(f"\nФайлы: {OUT.relative_to(ROOT)}/  (.txt — проверяемый макет, .html — печать в тот же макет)")
    return 0 if (ok_note and ok_one) or not args.check else 1


if __name__ == "__main__":
    sys.exit(main())
