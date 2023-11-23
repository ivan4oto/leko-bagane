import requests
from http import HTTPStatus


updatable_activity = {
    "description": None,
    "name": None,
}


def update_activity(headers, activity_id, name=None, description=None):
    url = f"https://www.strava.com/api/v3/activities/{activity_id}"
    # Filter out None values from params
    updatable_activity["name"] = name
    updatable_activity["description"] = description

    params = {k: v for k, v in updatable_activity.items() if v is not None}
    response = requests.put(url, headers=headers, params=params)
    if response.status_code == HTTPStatus.OK:
        return response
    # Handle this properly
    return response