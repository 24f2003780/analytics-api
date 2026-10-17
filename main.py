
from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_gu7edpreukx2z6mf9u008kmb"
EMAIL = "24f2003780@ds.study.iitm.ac.in"


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: list[Event]


@app.get("/")
def home():
    return {"status": "ok", "service": "analytics-api"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_totals = defaultdict(float)
    users = set()
    revenue = 0.0

    for event in request.events:
        users.add(event.user)

        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] += event.amount

    top_user = max(user_totals, key=user_totals.get, default=None)

    return {
        "email": EMAIL,
        "total_events": len(request.events),
        "unique_users": len(users),
        "revenue": round(revenue, 10),
        "top_user": top_user,
    }
