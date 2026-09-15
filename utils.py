"""Вспомогательные функции ввода, преобразования и проверки данных."""


def can_participate(user_age: int, event_min_age: int) -> bool:
    """Проверяет, подходит ли пользователь по возрасту."""
    return user_age >= event_min_age


def input_int(
    prompt: str, min_value: int | None = None, max_value: int | None = None
) -> int:
    """Запрашивает целое число и повторяет ввод при ошибке."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Введите целое число.")
            continue
        if min_value is not None and value < min_value:
            print(f"Введите число не меньше {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Введите число не больше {max_value}.")
            continue
        return value


def input_non_empty(prompt: str) -> str:
    """Запрашивает непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Поле не может быть пустым.")
