"""Функции доступности мероприятий и управления регистрациями."""

from datetime import date
from typing import Any

from events import find_event


ACTIVE_STATUS = "Зарегистрирован"
CANCELLED_STATUS = "Отменена"


def get_registration_status(is_available: bool) -> str:
    """Возвращает текстовый статус доступности регистрации."""
    return "Доступно для регистрации" if is_available else "Мест нет"


def is_event_available(
    events: list[dict[str, Any]],
    registrations: list[dict[str, Any]],
    event_id: int,
) -> bool:
    """Проверяет, осталось ли свободное место на мероприятии."""
    event = find_event(events, event_id)
    if event is None:
        return False
    active_count = sum(
        registration.get("event_id") == event_id
        and registration.get("status") == ACTIVE_STATUS
        for registration in registrations
    )
    return active_count < event["capacity"]


def create_registration(
    registrations: list[dict[str, Any]],
    events: list[dict[str, Any]],
    user_id: int,
    event_id: int,
    registration_date: date | None = None,
) -> dict[str, Any]:
    """Создаёт регистрацию, если мероприятие существует и доступно."""
    if find_event(events, event_id) is None:
        raise ValueError("Мероприятие не найдено.")
    duplicate = any(
        registration.get("user_id") == user_id
        and registration.get("event_id") == event_id
        and registration.get("status") == ACTIVE_STATUS
        for registration in registrations
    )
    if duplicate:
        raise ValueError("Вы уже зарегистрированы на это мероприятие.")
    if not is_event_available(events, registrations, event_id):
        raise ValueError("Свободных мест нет.")
    new_registration = {
        "id": max(
            (registration.get("id", 0) for registration in registrations),
            default=0,
        )
        + 1,
        "user_id": user_id,
        "event_id": event_id,
        "registration_date": (registration_date or date.today()).isoformat(),
        "status": ACTIVE_STATUS,
    }
    registrations.append(new_registration)
    return new_registration


def cancel_registration(
    registrations: list[dict[str, Any]], registration_id: int, user_id: int
) -> dict[str, Any]:
    """Отменяет активную регистрацию пользователя."""
    registration = next(
        (
            item
            for item in registrations
            if item.get("id") == registration_id
            and item.get("user_id") == user_id
            and item.get("status") == ACTIVE_STATUS
        ),
        None,
    )
    if registration is None:
        raise ValueError("Активная регистрация не найдена.")
    registration["status"] = CANCELLED_STATUS
    return registration


def get_user_registrations(
    registrations: list[dict[str, Any]], user_id: int
) -> list[dict[str, Any]]:
    """Возвращает все регистрации пользователя, включая отменённые."""
    return [
        registration
        for registration in registrations
        if registration.get("user_id") == user_id
    ]
