from redis import Redis, ConnectionPool
from dotenv import load_dotenv
import os

load_dotenv()

# Redis connection pool
connection_pool = ConnectionPool(host=os.getenv('REDIS_HOST', 'redis'), 
                                 port=os.getenv('REDIS_PORT', 6379), 
                                 db=os.getenv('REDIS_DB', 0), 
                                 password=os.getenv('REDIS_PASSWORD', None))

def get_redis() -> Redis:
    return Redis(connection_pool=connection_pool)