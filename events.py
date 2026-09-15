"""Функции поиска, проверки и сортировки благотворительных мероприятий."""

from datetime import date
from typing import Any


def find_event(
    events: list[dict[str, Any]], event_id: int
) -> dict[str, Any] | None:
    """Возвращает мероприятие по идентификатору или ``None``.

    Если мероприятие не найдено, возвращается ``None``.
    """
    return next(
        (event for event in events if event.get("id") == event_id),
        None,
    )


def search_events(
    events: list[dict[str, Any]],
    query: str = "",
    category: str = "",
    city: str = "",
) -> list[dict[str, Any]]:
    """Ищет мероприятия по тексту, направлению и городу."""
    query = query.casefold().strip()
    category = category.casefold().strip()
    city = city.casefold().strip()
    result = []
    for event in events:
        searchable_text = " ".join(
            str(event.get(field, ""))
            for field in ("name", "description", "category", "city")
        ).casefold()
        if query and query not in searchable_text:
            continue
        event_category = str(event.get("category", "")).casefold()
        if category and category not in event_category:
            continue
        if city and city not in str(event.get("city", "")).casefold():
            continue
        result.append(event)
    return result


def sort_events(
    events: list[dict[str, Any]], sort_key: str = "дата"
) -> list[dict[str, Any]]:
    """Возвращает копию списка мероприятий, отсортированную по полю."""
    keys = {
        "дата": "date",
        "date": "date",
        "название": "name",
        "name": "name",
        "город": "city",
        "city": "city",
    }
    field = keys.get(sort_key.casefold().strip())
    if field is None:
        raise ValueError("Доступна сортировка по: дата, название, город.")
    if field == "date":
        return sorted(
            events, key=lambda event: date.fromisoformat(event["date"])
        )
    return sorted(events, key=lambda event: str(event[field]).casefold())


def add_event(
    events: list[dict[str, Any]],
    name: str,
    category: str,
    city: str,
    event_date: str,
    min_age: int,
    capacity: int,
    organization_id: int,
    description: str,
) -> dict[str, Any]:
    """Добавляет мероприятие в коллекцию и возвращает созданную запись."""
    if any(
        event.get("name", "").casefold() == name.casefold()
        for event in events
    ):
        raise ValueError(
            "Мероприятие с таким названием уже существует."
        )
    if date.fromisoformat(event_date) < date.today():
        raise ValueError("Дата мероприятия не может быть в прошлом.")
    if min_age < 0 or capacity <= 0:
        raise ValueError("Возраст и вместимость должны быть положительными.")
    new_event = {
        "id": max((event.get("id", 0) for event in events), default=0) + 1,
        "name": name.strip(),
        "category": category.strip(),
        "city": city.strip(),
        "date": event_date,
        "min_age": min_age,
        "capacity": capacity,
        "organization_id": organization_id,
        "description": description.strip(),
    }
    events.append(new_event)
    return new_event
