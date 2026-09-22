from registrations import (
    CANCELLED_STATUS,
    ACTIVE_STATUS,
    cancel_registration,
    create_registration,
    get_registration_status,
    get_user_registrations,
)


def test_registration_status_text():
    assert get_registration_status(True) == "Доступно для регистрации"
    assert get_registration_status(False) == "Мест нет"


def test_unknown_event_cannot_be_registered(sample_events):
    import pytest

    with pytest.raises(ValueError, match="не найдено"):
        create_registration([], sample_events, 1, 999)


def test_cancelled_registration_can_be_created_again(sample_events):
    registrations = []
    create_registration(registrations, sample_events, 1, 1)
    cancel_registration(registrations, 1, 1)
    new_registration = create_registration(registrations, sample_events, 1, 1)
    assert new_registration["id"] == 2
    assert registrations[0]["status"] == CANCELLED_STATUS
    assert registrations[1]["status"] == ACTIVE_STATUS


def test_cancel_registration_checks_owner(sample_events):
    import pytest

    registrations = []
    create_registration(registrations, sample_events, 1, 1)
    with pytest.raises(ValueError, match="не найдена"):
        cancel_registration(registrations, 1, 2)


def test_get_user_registrations_returns_all_statuses(sample_events):
    registrations = []
    create_registration(registrations, sample_events, 1, 1)
    cancel_registration(registrations, 1, 1)
    assert (
        get_user_registrations(registrations, 1)[0]["status"]
        == CANCELLED_STATUS
    )
