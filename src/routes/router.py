from fastapi import APIRouter

from routes.activities import router as activities_router
from routes.buildings import router as buildings_router
from routes.organizations import router as organizations_router


router = APIRouter()

router.include_router(organizations_router, prefix="/organizations",
                      tags=["Organizations"])
router.include_router(buildings_router, prefix="/buildings",
                      tags=["Buildings"])
router.include_router(activities_router, prefix="/activities",
                      tags=["Activities"])
