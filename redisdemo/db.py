import os
import redis

NS = "redisdemo"
redis_pool = redis.ConnectionPool(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    db=int(os.getenv("REDIS_DB", "0")),
    decode_responses=True,  # auto decode byte to string
)


def get_redis():
    return redis.Redis(connection_pool=redis_pool)


def ns(*keys):
    lst = [NS]
    lst.extend(keys)
    return ":".join(lst)


def set(key, value):
    red = get_redis()
    red.set(ns(key), value)


def setm(dic):
    red = get_redis()
    pipe = red.pipeline()
    for k, v in dic.items():
        pipe.set(ns(k), v)
    pipe.execute()


def get(key):
    red = get_redis()
    return red.get(ns(key))


def delete(key):
    red = get_redis()
    return red.delete(ns(key))
