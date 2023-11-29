import requests
from http import HTTPStatus
from models.athlete_activity import AthleteActivity
from tortoise.transactions import in_transaction

from utils.auth_utils import get_auth_headers



async def create_item(name: str, description: str):
    async with in_transaction() as connection:
        item = AthleteActivity(name=name, description=description)
        await item.save(using_db=connection)
        return item

updatable_activity = {
    "description": None,
    "name": None,
}


async def update_activity(athlete_id, activity_id, name=None, description=None):
    url = f"https://www.strava.com/api/v3/activities/{activity_id}"
    # Filter out None values from params
    updatable_activity["name"] = name
    updatable_activity["description"] = description

    params = {k: v for k, v in updatable_activity.items() if v is not None}
    headers = await get_auth_headers(athlete_id)
    response = requests.put(url, headers = headers, params=params)
    if response.status_code == HTTPStatus.OK:
        return response
    # Handle this properly
    return response