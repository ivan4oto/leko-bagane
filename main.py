import json
import os
from dotenv import load_dotenv
from pygments import highlight
import requests
from typing import Union
from pygments.lexers.data import JsonLexer
from pygments.formatters import HtmlFormatter

from fastapi import FastAPI, Query, Response
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
import db_config

from activity_services.update_activity import update_activity
from models.strava_wh_event import StravaWhEvent, StravaWhEventIn

from views.events_view import router as events_router

app = FastAPI()

app.include_router(router=events_router)

register_tortoise(
    app,
    config=db_config.TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


load_dotenv()

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
CALLBACK_URL = os.getenv('CALLBACK_URL')


@app.get("/login")
def read_root():
    return RedirectResponse(
        url=f"http://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}&response_type=code&redirect_uri=http://127.0.0.1:8000/exchange_token&approval_prompt=force&scope=activity:write,activity:read_all,read"
        )

@app.post("/wh")
async def webhook_root(event: StravaWhEventIn):
    event_obj = StravaWhEvent(**event.model_dump())
    await event_obj.save()
    return event_obj


@app.get("/webhook_init")
def trigger_webhook():
    client_id = ""
    STRAVA_CLIENT_SECRET
    callback_url = CALLBACK_URL
    verify_token = "nqkyv string"


@app.get("/exchange_token")
def exchange_token(state: str = Query(None), code: str = Query(None), scope: str = Query(None)):
    # You can use the state, code, and scope variables here as needed
    url = "https://www.strava.com/oauth/token"
    data = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(url, data=data)
    parsed_response = json.loads(response.text)
    access_token = parsed_response["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # response = get_strava_activity(headers, '10256064515')
    # response = get_strava_activities(headers=headers)
    response = update_activity(headers, '4592416914', 'Леко Багане Тест')
    data = response.json()

    # Dump it back into a string with indentation
    json_string = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)


    formatted_html = highlight(json_string, JsonLexer(), HtmlFormatter(full=True, style='colorful'))
    return Response(content=formatted_html, media_type="text/html") 

def get_strava_activity(headers, id):
    url = f"https://www.strava.com/api/v3/activities/{id}?include_all_efforts=false"
    response = requests.get(url, headers=headers)

    return response

def get_strava_activities(headers, before=None, after=None, page=None, per_page=None):
    """
    Fetches activities from Strava API.

    :param access_token: Strava API access token.
    :param before: Only return activities before this UNIX timestamp (optional).
    :param after: Only return activities after this UNIX timestamp (optional).
    :param page: Page number (optional).
    :param per_page: Number of items per page (optional).
    :return: Response from the Strava API.
    """
    url = "https://www.strava.com/api/v3/athlete/activities"

    params = {
        "before": '1610236800',
        "after": '1609459200',
        "page": 1,
        "per_page": 5
    }

    # Filter out None values from params
    params = {k: v for k, v in params.items() if v is not None}

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)

    return response

