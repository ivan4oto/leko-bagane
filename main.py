from datetime import datetime
import json
import os
from dotenv import load_dotenv
import redis
import requests

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
from celery_worker import update_athlete_activity_task
import db_config

from dependencies import get_redis
from models.athlete import Athlete
from models.athlete_activity import AthleteActivity
from models.strava_wh_event import StravaWhEvent, StravaWhEventIn
from models.tokens import RefreshToken
from models.webhook_validator import WebhookValidator
from services.cache_service import CacheService

from views.events_view import router as events_router
from views.general_views import router as general_view

app = FastAPI()

app.include_router(router=general_view)
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



def get_cache_service(redis: redis.Redis = Depends(get_redis)):
    return CacheService(redis)


async def handle_event(event: StravaWhEvent):
    print('handle event')
    print(event.aspect_type)
    print(event.object_type)
    if event.aspect_type == 'create' and event.object_type == 'activity':
        activity_id = event.object_id


        try:
            print('delay trigger')
            update_athlete_activity_task.delay(activity_id, name='NOVO IME', description='OPISANIE')
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/login")
def read_root():
    return RedirectResponse(
        url=f"http://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}&response_type=code&redirect_uri=http://127.0.0.1:8000/exchange_token&approval_prompt=force&scope=activity:write,activity:read_all,read"
        )

@app.post("/wh")
async def webhook_root(event: StravaWhEventIn):
    event_obj = StravaWhEvent(**event.model_dump())
    await handle_event(event)
    await event_obj.save()
    return event_obj

@app.get("/wh")
async def webhook_root(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    event = WebhookValidator(
        hub_mode=hub_mode, 
        hub_challenge=hub_challenge, 
        hub_verify_token=hub_verify_token
    )
    await event.save()
    
    return {"hub.challenge": hub_challenge}


@app.get("/webhook_init")
def trigger_webhook():
    client_id = STRAVA_CLIENT_ID
    client_secret = STRAVA_CLIENT_SECRET
    callback_url = CALLBACK_URL
    verify_token = "nqkavstringbate"

    url = "https://www.strava.com/api/v3/push_subscriptions"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'callback_url': callback_url,
        'verify_token': verify_token
    }

    response = requests.post(url, data=payload)
    return response.json()


@app.get("/exchange_token")
async def exchange_token(
    state: str = Query(None),
    code: str = Query(None),
    scope: str = Query(None),
    cache_service: CacheService = Depends(get_cache_service)
    ):
    url = "https://www.strava.com/oauth/token"
    data = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(url, data=data)
    parsed_response = json.loads(response.text)
    print(parsed_response)
    access_token = parsed_response["access_token"]
    

    refresh_token = parsed_response["refresh_token"]

    athlete_id = parsed_response["athlete"]["id"]
    athlete_first_name = parsed_response["athlete"]["firstname"]
    athlete_last_name = parsed_response["athlete"]["lastname"]
    athlete_sex = parsed_response["athlete"]["sex"]
    athlete_city = parsed_response["athlete"]["city"]
    
    # Store access_token in Redis
    expires_at = parsed_response["expires_at"]


    cache_service.store_athlete_access_token(athlete_id, access_token, expires_at) # STORING ACCESS_TOKEN IN REDIS


    athlete = await Athlete.filter(athlete_id=athlete_id).first()
    if athlete is None:
        athlete = await Athlete.create(
            athlete_id = athlete_id,
            first_name = athlete_first_name,
            last_name = athlete_last_name,
            sex = athlete_sex,
            city = athlete_city
        )

    expires_at_datetime = datetime.utcfromtimestamp(expires_at)
    await RefreshToken.create(token=refresh_token, athlete=athlete, expires=expires_at_datetime)

    return RedirectResponse(url="/") 


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


def get_headers(token: str):
    return  {
        "Authorization": f"Bearer {token}"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)