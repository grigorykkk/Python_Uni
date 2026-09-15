"""Загрузка и сохранение коллекций проекта в JSON-файлах."""

import json
from pathlib import Path
from typing import Any


def load_json(filename: str | Path) -> list[dict[str, Any]]:
    """Загружает список словарей из JSON, обрабатывая ошибки формата."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Файл {filename} содержит некорректный JSON.") from error
    if not isinstance(data, list) or not all(
        isinstance(item, dict) for item in data
    ):
        raise ValueError(f"Файл {filename} должен содержать список объектов.")
    return data


def save_json(filename: str | Path, data: list[dict[str, Any]]) -> None:
    """Сохраняет коллекцию в JSON с отступами и кириллицей."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
