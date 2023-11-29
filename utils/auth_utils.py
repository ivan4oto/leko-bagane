

from dependencies import get_redis
from services.cache_service import CacheService
from services.token_service import TokenService

redis = get_redis()
cache_service = CacheService(redis)
token_service = TokenService(cache_service)




async def get_auth_headers(athlete_id: str):
    token = await token_service.get_athlete_access_token(athlete_id)
    return  {
        "Authorization": f"Bearer {token}"
    }