import pytest

from storage import load_json, save_json
from users import create_user, find_user


def test_create_and_find_user():
    users = []
    user = create_user(users, "Анна", 20, "anna@example.ru")
    assert find_user(users, "ANNA@example.ru")["id"] == user["id"]


def test_user_ids_are_generated():
    users = [{"id": 7, "name": "Иван", "age": 25, "email": "i@example.ru"}]
    user = create_user(users, "Ольга", 22, "o@example.ru")
    assert user["id"] == 8


def test_json_round_trip(tmp_path):
    filename = tmp_path / "items.json"
    source = [{"id": 1, "name": "Тест"}]
    save_json(filename, source)
    assert load_json(filename) == source


def test_invalid_json_is_reported(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError, match="некорректный JSON"):
        load_json(filename)


def test_missing_json_returns_empty_collection(tmp_path):
    assert load_json(tmp_path / "missing.json") == []


def test_json_structure_is_checked(tmp_path):
    filename = tmp_path / "object.json"
    filename.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="список объектов"):
        load_json(filename)
