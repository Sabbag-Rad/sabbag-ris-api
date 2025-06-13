import redis
import os


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")


def get_redis_connection(host=REDIS_HOST, port=REDIS_PORT, db=0, password=None):
    print(f"Connecting to Redis at {host}:{port} with db={db}")
    return redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
