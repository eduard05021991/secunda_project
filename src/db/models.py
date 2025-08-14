# src/db/models.py
from db.session import Base

# Импорт всех моделей, чтобы SQLAlchemy зарегистрировал их в metadata до конфигурации
from api.v1.activity.model import Activity, OrganizationActivity
from api.v1.building.model import Building
from api.v1.organization.model import Organization, PhoneNumber


__all__ = [
    "Base",
    "Activity",
    "OrganizationActivity",
    "Building",
    "Organization",
    "PhoneNumber",
]
