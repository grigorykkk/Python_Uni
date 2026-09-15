"""Формирование статистики по мероприятиям и регистрациям."""

from typing import Any


def build_statistics(
    events: list[dict[str, Any]], registrations: list[dict[str, Any]]
) -> dict[str, Any]:
    """Возвращает основные показатели сервиса."""
    active = [
        registration
        for registration in registrations
        if registration.get("status") == "Зарегистрирован"
    ]
    counts = {
        event["id"]: sum(item.get("event_id") == event["id"]
                         for item in active)
        for event in events
    }
    popular = max(events, key=lambda event: counts[event["id"]], default=None)
    if popular is not None:
        popular = dict(popular)
        popular["registrations_count"] = counts[popular["id"]]
    return {
        "events_count": len(events),
        "users_count": len({item.get("user_id") for item in registrations}),
        "active_registrations_count": len(active),
        "most_popular_event": popular,
    }
