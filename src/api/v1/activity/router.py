# src/api/v1/activity/router.py
from fastapi import APIRouter, Depends, Query
from starlette import status

from api.v1.activity.repository import ActivityRepository, \
    get_activity_repository
from api.v1.activity.schema import ActivityBase, ActivityCreate

router = APIRouter()

from dependencies import verify_api_key


@router.get(
    "/",
    response_model=list[ActivityBase],
    summary="Получить список деятельностей",
    description="Возвращает список всех видов деятельности",
)
async def get(
        activity_ids: list[int] | None = Query(None),
        repository: ActivityRepository = Depends(get_activity_repository)
):
    return await repository.get_activities(activity_ids=activity_ids)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую деятельность",
    description="Создаёт новый вид деятельности",
)
async def create_activity(
        activity: ActivityCreate,
        repository: ActivityRepository = Depends(get_activity_repository)
):
    await repository.create_activity(
        name=activity.name,
        parent_id=activity.parent_id,
        level=activity.level
    )
