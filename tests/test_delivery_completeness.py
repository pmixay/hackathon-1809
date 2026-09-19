"""Состав поставки по требованиям кейса и инструкции для жюри.

Кейс, раздел «Состав итогового решения» (`docs/organizer/case_statement_ru.md`), перечисляет, что
обязано быть в поставке, а раздел «Передача решения на GitVerse» — что обязано быть в README.
Здесь этот список проверяется как тест, чтобы пропавший документ или раздел не обнаружился на защите.

Проверяется наличие и минимальное содержание, а не качество текста: качество оценивает жюри.
"""
import re
from pathlib import Path

import pytest

from conftest import ROOT

NOTE = (ROOT / "docs" / "management_note.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
GUIDE = (ROOT / "docs" / "operator_guide.md").read_text(encoding="utf-8")
ONE_PAGER = (ROOT / "docs" / "one_pager_scenarios.md").read_text(encoding="utf-8")

LIVE_URL = "https://terra.arbuz.lol/"


# --- управленческая записка: разделы, перечисленные в кейсе -------------------------------
@pytest.mark.parametrize("heading", [
    "Логика архитектуры",           # логика архитектуры расчёта и снабжения
    "Методы и научные источники",
    "Данные и допущения",
    "Сравнение стратегий",
    "Контракты на запуск",
    "Экономика выбранного плана",
    "Методики и результаты стресс-тестов",
    "Реестр ключевых рисков",
    "Интересы заинтересованных сторон",
    "KPI надёжности",
    "Бюджет и дорожная карта",
])
def test_management_note_covers_every_required_section(heading):
    assert heading in NOTE, f"в записке нет раздела «{heading}», требуемого кейсом"


def test_one_pager_explains_what_stays_unchanged():
    """Кейс: одностраничник включает обоснование сохранения решений, если они не меняются."""
    assert "сохраняется" in ONE_PAGER.lower()


# --- состав поставки ----------------------------------------------------------------------
@pytest.mark.parametrize("label,path", [
    ("исходный код", "src/terraplan/engine.py"),
    ("данные организатора", "data/case/demand.csv"),
    ("конфигурации", "configs/assumptions.yaml"),
    ("протокол контрольных примеров", "tests/fixtures/control_cases.md"),
    ("протоколы стресс-тестов", "docs/stress_test_protocol.md"),
    ("инструкция оператора", "docs/operator_guide.md"),
    ("презентация", "docs/presentation/TerraPlan.pptx"),
    ("схема цепочки поставок", "docs/architecture.md"),
    ("контрактно-финансовая архитектура", "docs/contract_strategy.md"),
    ("бюджет и дорожная карта", "docs/roadmap_budget.md"),
    ("реестр рисков", "docs/risk_register.md"),
    ("карта интересов сторон", "docs/stakeholders.md"),
    ("KPI с формулами", "docs/kpi.md"),
    ("одностраничное резюме", "docs/one_pager_scenarios.md"),
])
def test_required_artifact_exists(label, path):
    assert (ROOT / path).exists(), f"нет обязательного материала: {label} ({path})"


@pytest.mark.parametrize("label,path", [
    ("стандартный сценарий", "results/alternatives/P2z_earth_new_zbo_BASE"),
    ("обязательный стресс", "results/stress/P2z_earth_new_zbo_adapted_MANDATORY_STRESS"),
    ("низкий и высокий спрос", "results/demand"),
    ("собственные риски команды", "results/risk_assessment.md"),
    ("перспективный горизонт", "results/extensibility"),
    ("сравнение сценариев", "results/stress"),
])
def test_required_reproducible_run_is_published(label, path):
    assert (ROOT / path).exists(), f"нет воспроизводимого расчёта: {label} ({path})"


def test_saved_plans_exist_for_both_scenarios():
    plans = {p.stem for p in (ROOT / "configs" / "plans").glob("*.json")}
    assert {"P2z_earth_new_zbo", "P2z_earth_new_zbo_adapted"} <= plans


@pytest.mark.parametrize("name", ["yearly_balance.csv", "results.xlsx", "export_envelope.json", "plan.json"])
def test_export_formats_are_published(name):
    """Кейс: выгрузка планов, результатов и сравнения в CSV или XLSX; план открывается повторно."""
    assert (ROOT / "results/alternatives/P2z_earth_new_zbo_BASE" / name).exists()


# --- README: то, что кейс требует в корне репозитория -------------------------------------
@pytest.mark.parametrize("label,pattern", [
    ("назначение решения", r"TerraPlan — работающий цифровой контур"),
    ("команда запуска", r"python -m terraplan ui"),
    ("зависимости", r"Python ≥ 3\.10"),
    ("последовательность проверки", r"## Порядок проверки"),
    ("рабочая ссылка", re.escape(LIVE_URL)),
])
def test_readme_has_what_the_case_requires(label, pattern):
    assert re.search(pattern, README), f"в README нет: {label}"


@pytest.mark.parametrize("directory", ["src", "data", "configs"])
def test_recommended_repository_layout(directory):
    assert (ROOT / directory).is_dir()


# --- инструкция по запуску и основным операциям -------------------------------------------
def test_operator_guide_covers_launch_and_main_operations():
    """Кейс: «инструкция по запуску и основным операциям»."""
    assert "## Запуск" in GUIDE
    for operation in ("Редактор", "Сохранение", "Выгрузка", "Расширение", "контракт", "Геополитич"):
        assert operation in GUIDE, f"в инструкции не описана операция: {operation}"
    assert "python -m terraplan ui" in GUIDE and "/console" in GUIDE


# --- живой стенд --------------------------------------------------------------------------
@pytest.mark.parametrize("path", [
    "README.md", "docs/operator_guide.md", "docs/management_note.md",
    "docs/one_pager_scenarios.md", "site/README.md", "docs/presentation/outline.md",
])
def test_live_stand_address_is_stated(path):
    assert LIVE_URL.rstrip("/") in (ROOT / path).read_text(encoding="utf-8"), \
        f"в {path} не указан адрес живого стенда"


def test_live_stand_always_offers_a_local_fallback():
    """Жюри не должно зависеть от доступности стенда: локальный запуск описан рядом с адресом.

    Утверждение о стенде проверяется не текстом, а командой `python scripts/check_live.py`,
    которая опрашивает реальные маршруты. Так документ не содержит хрупкого обещания.
    """
    for path in ("README.md", "site/README.md", "docs/operator_guide.md"):
        text = (ROOT / path).read_text(encoding="utf-8")
        assert "python -m terraplan ui" in text, f"{path}: рядом с адресом стенда нет локального запуска"


def test_publishing_behind_a_domain_is_documented():
    """Сервер за доменом без --allow-host отвечает 403 — это обязано быть в инструкции."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "--allow-host" in readme and "403" in readme
    assert "--allow-host" in (ROOT / "site" / "README.md").read_text(encoding="utf-8")
