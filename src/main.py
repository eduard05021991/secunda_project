# src/main.py
import uvicorn

from app import app
from config import settings

if __name__ == '__main__':
    print(settings.APP_HOST)
    uvicorn.run(
        app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
    )
