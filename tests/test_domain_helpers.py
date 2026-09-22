import pytest

from organizations import find_organization
from reports import build_statistics
from users import create_user
from utils import can_participate, input_int, input_non_empty


def test_find_organization(sample_organizations):
    assert find_organization(sample_organizations, 1)["name"] == "Фонд помощи"
    assert find_organization(sample_organizations, 999) is None


def test_build_statistics(sample_events):
    registrations = [
        {"id": 1, "user_id": 1, "event_id": 1, "status": "Зарегистрирован"},
        {"id": 2, "user_id": 2, "event_id": 1, "status": "Зарегистрирован"},
        {"id": 3, "user_id": 1, "event_id": 2, "status": "Отменена"},
    ]
    result = build_statistics(sample_events, registrations)
    assert result["events_count"] == 3
    assert result["users_count"] == 2
    assert result["active_registrations_count"] == 2
    assert result["most_popular_event"]["id"] == 1


def test_build_statistics_without_events():
    result = build_statistics([], [])
    assert result["most_popular_event"] is None


def test_can_participate():
    assert can_participate(18, 18)
    assert not can_participate(17, 18)


def test_input_int_repeats_after_invalid_value(monkeypatch, capsys):
    answers = iter(["не число", "0", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert input_int("Возраст: ", min_value=1, max_value=10) == 5
    assert "Введите целое число" in capsys.readouterr().out


def test_input_non_empty_repeats_after_blank(monkeypatch):
    answers = iter(["", "Анна"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert input_non_empty("Имя: ") == "Анна"


def test_create_user_rejects_invalid_data():
    with pytest.raises(ValueError, match="корректный e-mail"):
        create_user([], "Анна", 20, "invalid-email")
    with pytest.raises(ValueError, match="от 1 до 120"):
        create_user([], "Анна", 121, "anna@example.ru")
