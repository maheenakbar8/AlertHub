from fastapi import FastAPI

from database import Base, engine


from routers.alerts import router as alerts_router
from routers.weather import router as weather_router

from contextlib import asynccontextmanager

from scheduler import start_scheduler


Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app):
    start_scheduler()

    yield

app = FastAPI(
    title="AlertHub",
    lifespan=lifespan
)


app.include_router(alerts_router)
app.include_router(weather_router)


@app.get("/")
def home():
    return {"message": "AlertHub is running!"}