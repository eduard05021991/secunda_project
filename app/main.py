from fastapi import FastAPI, Depends
from app.database import engine, Base, get_db
from app.dependencies import verify_api_key
from app.routes import activities, buildings, organizations
import time
from sqlalchemy.exc import OperationalError


app = FastAPI()

# Include routers
app.include_router(activities.router, prefix="/api/v1/activities", tags=["activities"], dependencies=[Depends(verify_api_key)])
app.include_router(buildings.router, prefix="/api/v1/buildings", tags=["buildings"], dependencies=[Depends(verify_api_key)])
app.include_router(organizations.router, prefix="/api/v1/organizations", tags=["organizations"], dependencies=[Depends(verify_api_key)])

# Retry connection to database
retries = 5
while retries > 0:
    try:
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError as e:
        print(f"Database connection failed: {e}. Retrying ({retries} attempts left)...")
        retries -= 1
        time.sleep(5)
else:
    raise Exception("Failed to connect to database after multiple attempts")

@app.get("/")
async def root():
    return {"message": "Welcome to the Secunda API!"}
