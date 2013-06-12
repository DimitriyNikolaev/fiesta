# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
import pickle
from django import template
from fiesta_core.global_utils.redis_adapter import redis_adapter
from fiesta_core.apps.blog.model_extension import RedisKeys, NewsPreview
from fiesta_core.apps.blog.models import News

register = template.Library()
@register.inclusion_tag('fiesta/blog/pop_news.html', takes_context=True)
def pop_news_list(context):
    pop_news_idlist  = redis_adapter.zrange(RedisKeys.pop_news,0,3)
    if len(pop_news_idlist) > 0:
        pipe = redis_adapter.pipeline()
        for id in pop_news_idlist:
            pipe.get(RedisKeys.preview_news_key % id)
        exec_res = pipe.execute()
        if len(exec_res) > 0:
            result = []
            for ind,preview_serialized in enumerate(exec_res):
                if preview_serialized is not None:
                    result.append(pickle.loads(preview_serialized))
                else:
                    id = pop_news_idlist[ind] if len(pop_news_idlist) > ind else 0
                    if id > 0:
                        news = News.objects.get(pk=id)
                        photos = news.news_photos.all()
                        preview = NewsPreview(news.id,news.title, photos[0].preview.url if photos.count() > 0 else '')
                        preview_serialized = pickle.dumps(preview)
                        redis_adapter.set(RedisKeys.preview_news_key % news.id, preview_serialized)
                        result.append(preview)



    return {'pop_news': result}