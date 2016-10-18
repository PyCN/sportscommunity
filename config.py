import os
import sys
import _env    # noqa
import redis
# from pymongo import Connection

__author__ = 'ZivLi'

settings={
    'debug' : True,
}


PREFIX = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ''
    )
)
if PREFIX not in sys.path:
    sys.path.append(PREFIX)

MONGO = dict(host='mongodb://mongo:27017')

redis_recom = redis.Redis(host='redis', port='6379', db=4)
