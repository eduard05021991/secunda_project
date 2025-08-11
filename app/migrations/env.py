from app.models.models import Organization
from app.models.models import Building
from app.models.models import Activity, OrganizationActivity


target_metadata = [Organization.metadata, Building.metadata, Activity.metadata]
