# src/app.py
import db.models

from fastapi import FastAPI

from api.router import router

from fastapi.openapi.models import APIKey
from fastapi.security import APIKeyHeader

from dependencies import verify_api_key


def get_application() -> FastAPI:
    application = FastAPI(
        title="Organization Directory API",
        description="REST API для справочника организаций, зданий и "
                    "деятельностей. Поддерживает CRUD-операции и "
                    "поиск по различным критериям. "
                    "Все запросы требуют API-ключа в заголовке X-API-Key.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    application.openapi_schema = None
    api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)
    application.dependency_overrides[verify_api_key] = verify_api_key
    application.include_router(router, prefix="/api/v1")

    return application


app = get_application()
