"""Функции работы с организациями-благотворителями."""

from typing import Any


def find_organization(
    organizations: list[dict[str, Any]], organization_id: int
) -> dict[str, Any] | None:
    """Возвращает организацию по идентификатору или ``None``."""
    return next(
        (
            organization
            for organization in organizations
            if organization.get("id") == organization_id
        ),
        None,
    )
