import pytest


@pytest.fixture
def sample_organizations():
    return [{"id": 1, "name": "Фонд помощи", "contact": "help@example.ru"}]


@pytest.fixture
def sample_events():
    return [
        {
            "id": 1,
            "name": "Помощь животным",
            "category": "Животные",
            "city": "Москва",
            "date": "2026-09-20",
            "min_age": 14,
            "capacity": 40,
            "organization_id": 1,
            "description": "Приют",
        },
        {
            "id": 2,
            "name": "Праздник для детей",
            "category": "Дети",
            "city": "Екатеринбург",
            "date": "2026-09-28",
            "min_age": 16,
            "capacity": 25,
            "organization_id": 2,
            "description": "Подарки",
        },
        {
            "id": 3,
            "name": "Уборка парка",
            "category": "Экология",
            "city": "Москва",
            "date": "2026-09-21",
            "min_age": 14,
            "capacity": 50,
            "organization_id": 3,
            "description": "Парк",
        },
    ]
