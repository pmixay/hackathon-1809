"""Проверка живого стенда: какие маршруты отвечают и работает ли расчёт по ссылке.

Документы называют адрес стенда, а доступность проверяется этой командой, а не текстом:
стенд может быть перезапущен или обновлён, и утверждение в README не должно устаревать молча.

    python scripts/check_live.py                      # https://terra.arbuz.lol/
    python scripts/check_live.py http://127.0.0.1:8765

Код возврата: 0 — страница решения доступна; 1 — недоступна. Отсутствие пульта оператора
не считается ошибкой: он всегда запускается локально (`python -m terraplan ui`).
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

DEFAULT = "https://terra.arbuz.lol/"
TIMEOUT = 20


def probe(url: str, method: str = "GET", body: bytes | None = None) -> tuple[int, str]:
    request = urllib.request.Request(url, method=method, data=body,
                                     headers={"Content-Type": "application/json"} if body else {})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.status, response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", "") if exc.headers else ""
    except Exception as exc:                      # сеть, DNS, TLS
        return 0, f"{type(exc).__name__}: {exc}"


def main() -> int:
    base = (sys.argv[1] if len(sys.argv) > 1 else DEFAULT).rstrip("/")
    print(f"Живой стенд: {base}\n")
    page, _ = probe(f"{base}/")
    print(f"  {'страница решения':28s} /              HTTP {page or '—'}")
    console, _ = probe(f"{base}/console")
    api, _ = probe(f"{base}/api/bootstrap")
    print(f"  {'пульт оператора':28s} /console       HTTP {console or '—'}")
    print(f"  {'данные для пульта':28s} /api/bootstrap HTTP {api or '—'}")

    print()
    if page == 200:
        print("  Страница решения доступна.")
    else:
        print("  Страница решения НЕ доступна — используйте локальный запуск.")
    if console == 200 and api == 200:
        print("  Пульт оператора доступен на стенде: расчёт можно открыть по ссылке.")
    elif console == 403 or api == 403:
        print("  Пульт отвечает 403: сервер запущен без разрешённого имени узла.")
        print("  Исправление: python -m terraplan ui --allow-host <имя> --bind 0.0.0.0")
    else:
        print("  Пульт оператора на стенде не развёрнут (это допустимо).")
        print("  Локальный запуск: python -m terraplan ui  ->  http://127.0.0.1:8765/console")
    return 0 if page == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
