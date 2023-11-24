from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tortoise.queryset import QuerySet
from tortoise.contrib.pydantic import pydantic_model_creator
from models.strava_wh_event import StravaWhEvent


templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

