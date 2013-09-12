# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.core.management.base import BaseCommand
from fiesta_core.global_utils.redis_adapter import redis_adapter
from fiesta_core.apps.blog.model_extension import RedisKeys

class Command(BaseCommand):
    def handle(self, *args, **options):
        pop_news_idlist  = redis_adapter.zrevrange(RedisKeys.pop_news_by_city % '2',0,2)
        if len(pop_news_idlist) > 0:
            for id in pop_news_idlist:
                self.stdout.write(id)
                redis_adapter.zrem(RedisKeys.pop_news_by_city % '2',id)
        self.stdout.write("done")