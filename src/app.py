from fastapi import FastAPI

from api.router import router


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
    application.include_router(router, prefix="/api/v1")

    return application


app = get_application()
