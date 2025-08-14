# src/api/router.py
from fastapi import APIRouter, Depends
from dependencies import verify_api_key
from api.v1.activity.router import router as activity_router
from api.v1.building.router import router as building_router
from api.v1.organization.router import router as organization_router


#router = APIRouter()
router = APIRouter(dependencies=[Depends(verify_api_key)])

router.include_router(activity_router, prefix='/activities')
router.include_router(building_router, prefix='/buildings')
router.include_router(organization_router, prefix='/organizations')
