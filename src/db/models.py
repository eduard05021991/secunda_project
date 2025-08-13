from db.session import Base
from api.v1.activity.model import Activity, OrganizationActivity
from api.v1.building.model import Building
from api.v1.organization.model import Organization, PhoneNumber

all_models = [
    Base,
    Activity,
    OrganizationActivity,
    Building,
    Organization,
    PhoneNumber
]
