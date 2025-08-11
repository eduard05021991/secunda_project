from fastapi import FastAPI, Depends
from .routes import organizations, buildings, activities
from .database import Base, engine


app = FastAPI(
    title="Organization Directory API",
    description="REST API для справочника организаций, зданий и деятельностей. Поддерживает CRUD-операции и поиск по различным критериям. Все запросы требуют API-ключа в заголовке X-API-Key.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

Base.metadata.create_all(bind=engine)

app.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
app.include_router(buildings.router, prefix="/buildings", tags=["Buildings"])
app.include_router(activities.router, prefix="/activities", tags=["Activities"])
