from datetime import datetime



class CacheService:
    def __init__(self, redis):
        self.redis = redis

    def store_athlete_access_token(self, athlete_id, access_token, expires_at):
        expires_at_datetime = datetime.utcfromtimestamp(expires_at)
        now = datetime.utcnow()
        expiration_seconds = int((expires_at_datetime - now).total_seconds())
        key = f"athlete_id:{athlete_id}"
        self.redis.setex(key, expiration_seconds, access_token)

    def get_athlete_access_token_from_cache(self, athlete_id):
        key = f"athlete_id:{athlete_id}"
        token = self.redis.get(key)
        if token:
            token = token.decode("utf-8")
            return token
        else:
            print("Token not found or expired.")
