import pytest

from events import find_event, search_events, sort_events


def test_find_event_returns_event_or_none(sample_events):
    assert find_event(sample_events, 2)["name"] == "Праздник для детей"
    assert find_event(sample_events, 999) is None


def test_search_events_by_query_and_category(sample_events):
    result = search_events(sample_events, query="парк", category="экология")
    assert [event["id"] for event in result] == [3]


def test_sort_events_by_name_and_city(sample_events):
    assert [
        event["id"] for event in sort_events(sample_events, "название")
    ] == [1, 2, 3]
    assert [
        event["id"] for event in sort_events(sample_events, "город")
    ] == [2, 1, 3]


def test_sort_events_rejects_unknown_key(sample_events):
    with pytest.raises(ValueError, match="Доступна сортировка"):
        sort_events(sample_events, "вместимость")


def test_add_event_rejects_duplicate_and_invalid_capacity(sample_events):
    with pytest.raises(ValueError, match="уже существует"):
        from events import add_event

        add_event(
            sample_events,
            "Помощь животным",
            "Животные",
            "Москва",
            "2099-12-01",
            14,
            20,
            1,
            "Описание",
        )
    with pytest.raises(ValueError, match="положительными"):
        from events import add_event

        add_event(
            sample_events,
            "Новое",
            "Экология",
            "Пермь",
            "2099-12-01",
            14,
            0,
            1,
            "Описание",
        )
