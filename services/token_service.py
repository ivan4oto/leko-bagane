import json
import os
from dotenv import load_dotenv
import requests
from models.tokens import RefreshToken
from services.cache_service import CacheService

load_dotenv()


STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
AUTH_URL = "https://www.strava.com/oauth/token"


class TokenService():
    def __init__(self, cache_service: CacheService) -> None:
        self.cache_service = cache_service
        pass

    async def get_athlete_access_token(self, athlete_id: str):
        token = self.cache_service.get_athlete_access_token_from_cache(athlete_id)
        if token:
            return token
        refresh_token = await RefreshToken.filter(athlete__athlete_id=athlete_id).first()

        return await self.__fetch_new_token(refresh_token)


        
    async def __fetch_new_token(self, refresh_token: str):
        response = requests.post(AUTH_URL, data = {
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "code": refresh_token,
            "grant_type": "authorization_code"
        })
        parsed_response = json.loads(response.text)
        return parsed_response['access_token']
        