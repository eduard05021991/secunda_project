from db.session import Base
from models import (
    Activity,
    OrganizationActivity,
    Building,
    Organization,
    PhoneNumber
)


all_models = [
    Base,
    Activity,
    OrganizationActivity,
    Building,
    Organization,
    PhoneNumber
]
