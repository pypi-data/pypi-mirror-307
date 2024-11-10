import json
import math
import os
from numbers import Number

import redis
from redis.exceptions import AuthenticationError
from redis.exceptions import ConnectionError


class RedisClient:
    def __init__(self, host=None, port=None, db=None):
        self.r = redis.StrictRedis(
            host=os.environ.get('redis_host'),
            port=int(os.environ.get('redis_port')),
            db=int(os.environ.get('redis_db')),
            password=os.environ.get('redis_password'),
            socket_connect_timeout=15,
        )

        try:
            self.r.ping()
        except AuthenticationError:
            raise Exception('Redis authentication failed')
        except ConnectionError as e:
            raise Exception(f'Redis connection failed, {e}')
        except Exception as e:
            raise Exception(f'Redis error {e}')

    def refresh_progress(self, task_id, progress):
        if not isinstance(progress, Number):
            raise TypeError('progress must be a number type')

        if progress < 0 or progress > 1:
            raise ValueError('progress must be between 0 and 100')

        self.r.hset(f'model_status:{task_id}', 'progress', str(math.floor(progress * 1000) / 1000))

    def get_progress(self, task_id):
        res = self.r.hget(f'model_status:{task_id}', 'progress')
        return float(res) if res else -1

    def push_result(self, task_id, result):
        if not isinstance(result, dict):
            raise TypeError('result must be a dict type')
        self.r.hset(f'model_status:{task_id}', 'result', json.dumps(result).encode('utf-8'))

    def get_result(self, task_id):
        res = self.r.hget(f'model_status:{task_id}', 'result')
        return json.loads(res.decode('utf-8')) if res else None
