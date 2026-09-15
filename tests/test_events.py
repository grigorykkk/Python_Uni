from events import add_event, search_events, sort_events


def test_search_events_by_city(sample_events):
    result = search_events(sample_events, city="Москва")
    assert [event["id"] for event in result] == [1, 3]


def test_sort_events_by_date(sample_events):
    result = sort_events(sample_events, "дата")
    assert [event["id"] for event in result] == [1, 3, 2]


def test_add_event(sample_events):
    event = add_event(
        sample_events,
        "Новое мероприятие",
        "Экология",
        "Пермь",
        "2099-12-01",
        14,
        20,
        1,
        "Описание",
    )
    assert event["id"] == 4
    assert len(sample_events) == 4
