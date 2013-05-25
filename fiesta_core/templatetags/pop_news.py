# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
import pickle
from django import template
from fiesta_core.global_utils.redis_adapter import redis_adapter
from fiesta_core.apps.blog.model_extension import RedisKeys

register = template.Library()
@register.inclusion_tag('fiesta/blog/pop_news.html', takes_context=True)
def pop_news_list(context):
    pop_news_idlist  = redis_adapter.zrange(RedisKeys.pop_news,0,3)
    pipe = redis_adapter.pipeline()
    for id in pop_news_idlist:
        pipe.get(RedisKeys.preview_news_key % id)
    result = [ pickle.loads(preview_serialized) for preview_serialized in pipe.execute()]
    return {'pop_news': result}