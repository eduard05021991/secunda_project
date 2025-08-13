from fastapi import APIRouter

from api.v1.activity.router import router as activity_router

router = APIRouter()

router.include_router(activity_router, prefix='/activities')
