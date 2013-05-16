# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

import redis


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def redis_adapter():
    return redis.Redis(connection_pool=pool)