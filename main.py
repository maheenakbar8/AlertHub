from fastapi import FastAPI

app = FastAPI()


alerts = [
    {
        "id": 1,
        "title": "Heavy Rain Warning",
        "severity": "high"
    },
    {
        "id": 2,
        "title": "Road Closure",
        "severity": "medium"
    },
    {
        "id": 3,
        "title": "Power Outage",
        "severity": "low"
    }
]


@app.get("/")
def home():
    return {"message": "AlertHub is running!"}


@app.get("/alerts")
def get_alerts():
    return alerts