from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tortoise.queryset import QuerySet
from tortoise.contrib.pydantic import pydantic_model_creator
from models.strava_wh_event import StravaWhEvent


templates = Jinja2Templates(directory="templates")
router = APIRouter()
StravaWhEvent_Pydantic = pydantic_model_creator(StravaWhEvent, name="StravaWhEvent")

@router.get("/strava-events/", response_class=HTMLResponse)
async def get_strava_events(request: Request):
    events = await StravaWhEvent_Pydantic.from_queryset(StravaWhEvent.all())
    return templates.TemplateResponse("strava_events.html", {"request": request, "events": events})

