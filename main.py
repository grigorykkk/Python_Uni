"""Консольный интерфейс сервиса поиска благотворительных мероприятий."""

from pathlib import Path
from typing import Any

from events import find_event, search_events, sort_events
from registrations import (
    cancel_registration,
    create_registration,
    get_user_registrations,
    is_event_available,
)
from reports import build_statistics
from storage import load_json, save_json
from users import create_user, find_user
from utils import can_participate, input_int, input_non_empty


PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
EVENTS_FILE = DATA_DIR / "events.json"
ORGANIZATIONS_FILE = DATA_DIR / "organizations.json"
USERS_FILE = DATA_DIR / "users.json"
REGISTRATIONS_FILE = DATA_DIR / "registrations.json"


def load_data() -> dict[str, list[dict[str, Any]]]:
    """Загружает коллекции проекта из JSON-файлов."""
    return {
        "events": load_json(EVENTS_FILE),
        "organizations": load_json(ORGANIZATIONS_FILE),
        "users": load_json(USERS_FILE),
        "registrations": load_json(REGISTRATIONS_FILE),
    }


def save_data(data: dict[str, list[dict[str, Any]]]) -> None:
    """Сохраняет все коллекции проекта в JSON-файлы."""
    save_json(EVENTS_FILE, data["events"])
    save_json(ORGANIZATIONS_FILE, data["organizations"])
    save_json(USERS_FILE, data["users"])
    save_json(REGISTRATIONS_FILE, data["registrations"])


def show_events(
    events: list[dict[str, Any]],
    organizations: list[dict[str, Any]],
    registrations: list[dict[str, Any]],
) -> None:
    """Выводит список мероприятий и сведения об организациях."""
    if not events:
        print("\nМероприятия не найдены.")
        return

    organization_map = {item["id"]: item for item in organizations}
    print("\n=== Мероприятия ===")
    for event in events:
        organization = organization_map.get(event["organization_id"], {})
        registered_count = sum(
            registration.get("event_id") == event["id"]
            and registration.get("status") == "Зарегистрирован"
            for registration in registrations
        )
        available_places = max(event["capacity"] - registered_count, 0)
        print(f"\n[{event['id']}] {event['name']}")
        print(
            f"Направление: {event['category']} | Город: {event['city']}"
        )
        print(
            f"Дата: {event['date']} | "
            f"Минимальный возраст: {event['min_age']}+"
        )
        print(
            f"Организация: {organization.get('name', 'не указана')} "
            f"({organization.get('contact', 'нет контакта')})"
        )
        print(f"Свободных мест: {available_places} из {event['capacity']}")
        print(f"Описание: {event['description']}")


def show_user_registrations(
    user_id: int,
    events: list[dict[str, Any]],
    registrations: list[dict[str, Any]],
) -> None:
    """Выводит регистрации выбранного пользователя."""
    event_map = {event["id"]: event for event in events}
    user_registrations = get_user_registrations(registrations, user_id)
    if not user_registrations:
        print("\nУ вас пока нет регистраций.")
        return

    print("\n=== Мои регистрации ===")
    for registration in user_registrations:
        event = event_map.get(registration["event_id"], {})
        print(
            f"[{registration['id']}] "
            f"{event.get('name', 'Мероприятие удалено')} "
            f"— {event.get('date', 'дата неизвестна')} — "
            f"{registration['status']}"
        )


def register_for_event(
    data: dict[str, list[dict[str, Any]]], user: dict[str, Any]
) -> None:
    """Регистрирует текущего пользователя на выбранное мероприятие."""
    event_id = input_int("Введите ID мероприятия: ", min_value=1)
    event = find_event(data["events"], event_id)
    if event is None:
        print("Мероприятие с таким ID не найдено.")
        return
    if not can_participate(user["age"], event["min_age"]):
        print(
            f"Для участия необходимо достичь возраста {event['min_age']} лет.")
        return
    if not is_event_available(data["events"], data["registrations"], event_id):
        print("Свободных мест нет.")
        return

    try:
        registration = create_registration(
            data["registrations"], data["events"], user["id"], event_id
        )
        save_data(data)
    except (OSError, ValueError) as error:
        print(f"Регистрация не выполнена: {error}")
        return

    print(
        f"Регистрация выполнена. Номер регистрации: {registration['id']}. "
        f"Дата: {registration['registration_date']}"
    )


def cancel_user_registration(
    data: dict[str, list[dict[str, Any]]], user: dict[str, Any]
) -> None:
    """Отменяет регистрацию текущего пользователя."""
    show_user_registrations(user["id"], data["events"], data["registrations"])
    registration_id = input_int(
        "Введите ID регистрации для отмены: ", min_value=1)
    try:
        cancel_registration(data["registrations"], registration_id, user["id"])
        save_data(data)
    except (OSError, ValueError) as error:
        print(f"Отмена не выполнена: {error}")
        return
    print("Регистрация отменена.")


def show_statistics(
    events: list[dict[str, Any]], registrations: list[dict[str, Any]]
) -> None:
    """Выводит сводную статистику по мероприятиям."""
    statistics = build_statistics(events, registrations)
    print("\n=== Статистика ===")
    print(f"Всего мероприятий: {statistics['events_count']}")
    print(f"Всего пользователей зарегистрировано: {statistics['users_count']}")
    print(f"Активных регистраций: {statistics['active_registrations_count']}")
    if statistics["most_popular_event"]:
        event = statistics["most_popular_event"]
        print(
            f"Самое популярное мероприятие: {event['name']} "
            f"({event['registrations_count']} регистраций)"
        )


def get_current_user(users: list[dict[str, Any]]) -> dict[str, Any]:
    """Запрашивает данные пользователя и добавляет его при первом входе."""
    name = input_non_empty("Введите ваше имя: ")
    age = input_int("Введите ваш возраст: ", min_value=1, max_value=120)
    email = input_non_empty("Введите e-mail: ").lower()
    user = find_user(users, email)
    if user is not None:
        return user
    return create_user(users, name, age, email)


def main() -> None:
    """Запускает основной цикл приложения."""
    print("=== Сервис поиска благотворительных мероприятий ===")
    try:
        data = load_data()
        user = get_current_user(data["users"])
        save_data(data)
    except (OSError, ValueError, EOFError) as error:
        print(f"Не удалось запустить программу: {error}")
        return

    while True:
        print(
            "\nМеню:\n"
            "1. Показать все мероприятия\n"
            "2. Найти мероприятие\n"
            "3. Отсортировать мероприятия\n"
            "4. Зарегистрироваться на мероприятие\n"
            "5. Отменить регистрацию\n"
            "6. Мои регистрации\n"
            "7. Статистика\n"
            "0. Выход"
        )
        try:
            choice = input_int("Выберите действие: ", min_value=0, max_value=7)
        except (EOFError, KeyboardInterrupt):
            print("\nРабота завершена.")
            return

        if choice == 0:
            print("До свидания!")
            return
        if choice == 1:
            show_events(data["events"], data["organizations"],
                        data["registrations"])
        elif choice == 2:
            query = input("Поисковый запрос (можно оставить пустым): ").strip()
            category = input("Направление (можно оставить пустым): ").strip()
            city = input("Город (можно оставить пустым): ").strip()
            found = search_events(data["events"], query, category, city)
            show_events(found, data["organizations"], data["registrations"])
        elif choice == 3:
            sort_key = input(
                "Сортировка: дата, название, город: ").strip().lower()
            try:
                sorted_events = sort_events(data["events"], sort_key)
            except ValueError as error:
                print(error)
            else:
                show_events(
                    sorted_events, data["organizations"], data["registrations"]
                )
        elif choice == 4:
            register_for_event(data, user)
        elif choice == 5:
            cancel_user_registration(data, user)
        elif choice == 6:
            show_user_registrations(
                user["id"], data["events"], data["registrations"])
        elif choice == 7:
            show_statistics(data["events"], data["registrations"])


if __name__ == "__main__":
    main()
