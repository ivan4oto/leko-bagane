import json
import requests
from utils.auth_utils import get_auth_headers


async def fetch_activity(athlete_id, activity_id):
    url = f"https://www.strava.com/api/v3/activities/{activity_id}?include_all_efforts=false"
    headers = await get_auth_headers(athlete_id)
    response = requests.get(url, headers=headers)
    parsed_response = json.loads(response.text)

    return parsed_response