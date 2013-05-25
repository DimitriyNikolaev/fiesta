# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

import redis


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis_adapter = redis.Redis(connection_pool=pool)