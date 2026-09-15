"""Функции создания и поиска пользователей сервиса."""

from typing import Any


def find_user(
    users: list[dict[str, Any]], email: str
) -> dict[str, Any] | None:
    """Ищет пользователя по адресу электронной почты."""
    normalized_email = email.casefold().strip()
    return next(
        (user for user in users if user.get(
            "email", "").casefold() == normalized_email),
        None,
    )


def create_user(
    users: list[dict[str, Any]], name: str, age: int, email: str
) -> dict[str, Any]:
    """Проверяет данные и добавляет нового пользователя."""
    if not name.strip():
        raise ValueError("Имя пользователя не может быть пустым.")
    if not 1 <= age <= 120:
        raise ValueError("Возраст должен быть от 1 до 120 лет.")
    if "@" not in email or not email.strip():
        raise ValueError("Укажите корректный e-mail.")
    if find_user(users, email) is not None:
        raise ValueError("Пользователь с таким e-mail уже существует.")
    user = {
        "id": max((item.get("id", 0) for item in users), default=0) + 1,
        "name": name.strip(),
        "age": age,
        "email": email.strip().lower(),
    }
    users.append(user)
    return user
