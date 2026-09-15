from datetime import date

import pytest

from registrations import (
    cancel_registration,
    create_registration,
    is_event_available,
)


def test_event_is_available(sample_events):
    assert is_event_available(sample_events, [], 1)


def test_create_registration(sample_events):
    registrations = []
    registration = create_registration(
        registrations, sample_events, 1, 1, date(2026, 9, 15)
    )
    assert registration["registration_date"] == "2026-09-15"
    assert registration["status"] == "Зарегистрирован"


def test_duplicate_registration_forbidden(sample_events):
    registrations = []
    create_registration(registrations, sample_events, 1, 1)
    with pytest.raises(ValueError, match="уже зарегистрированы"):
        create_registration(registrations, sample_events, 1, 1)


def test_cancel_registration(sample_events):
    registrations = []
    create_registration(registrations, sample_events, 1, 1)
    cancelled = cancel_registration(registrations, 1, 1)
    assert cancelled["status"] == "Отменена"


def test_capacity_limit(sample_events):
    sample_events[0]["capacity"] = 1
    registrations = []
    create_registration(registrations, sample_events, 1, 1)
    assert not is_event_available(sample_events, registrations, 1)
