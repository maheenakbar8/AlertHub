from fastapi import FastAPI

from database import Base, engine
from routers.alerts import router as alerts_router


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(alerts_router)


@app.get("/")
def home():
    return {"message": "AlertHub is running!"}