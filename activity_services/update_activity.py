import json
from anyio import sleep
import requests
from http import HTTPStatus
from activity_services.get_activity import fetch_activity
from models.athlete_activity import AthleteActivity
from tortoise.transactions import in_transaction

from utils.auth_utils import get_auth_headers
from utils.misc_utils import find_nearest_key, seconds_to_minutes


heart_rate_dict = {
    120: "Е тва ти е възстановително",
    130: "Рекавъри рън. Браво научил си се да бягаш леко!",
    140: "Истинско леко багане брат!",
    145: "Първа зона. Евала топ бягане!",
    148: "Може маааалко да забързаш. На ръба на втора зона си ми.",
    153: "Е тва ти е топ за тренировки. Идялка! Утре искам пак такова!",
    157: "Това не ти е леко!",
    161: "Лактейт трешхолд. По-полека за къде се напъваме, рано е още.",
    165: "Ко праим брат? За къде бързаме?",
    168: "Пиши го темпово тва и утре искам да бягаш леко!",
    170: "Шалоу ще излитаме ли? Къв е тоя пулс я се успокой малко!",
    180: "Намали малко е, зима е още, ще ми претренираш на пролет и ще ближеш рани после.",
    200: "Вземи си купи един колан, пулса от китка е грешен."
}

moving_time_dict = {
    40: "Кво е тва? Лигавим се нещо?",
    50: "Абе и по-дълго можеше да е...",
    60: "Може да напрайш още едно такова днес.",
    70: "Става.",
    80: "Много добре идеалка брат!",
    120: "Мое го броим за нещо като дълго.",
    130: "Пиши го дълго бягане",
    150: "Ко напрай ти е... Ще стане маратонец от теб!"
}




async def create_item(name: str, description: str):
    async with in_transaction() as connection:
        item = AthleteActivity(name=name, description=description)
        await item.save(using_db=connection)
        return item

updatable_activity = {
    "description": None,
    "name": None,
}


async def update_activity(activity, name=None, description=None):
    print('inside update activity')
    url = f"https://www.strava.com/api/v3/activities/{activity_id}"
    athlete_id = activity.get("athlete", {}).get("id")
    if athlete_id is None:
        raise Exception("Athlete data missing from activity.")
    


    moving_time = seconds_to_minutes(activity["moving_time"])


    if activity["has_heartrate"]:
        description_text = find_nearest_key(activity["average_heartrate"], heart_rate_dict)
        description_text = "Your coach says: " + description_text
        updatable_activity["description"] = description_text.encode("utf-8")

    params = {k: v for k, v in updatable_activity.items() if v is not None}
    headers = await get_auth_headers(athlete_id)
    await sleep(6)
    response = requests.put(url, headers = headers, params=params)
    if response.status_code == HTTPStatus.OK:
        return response
    # Handle this properly
    return response


