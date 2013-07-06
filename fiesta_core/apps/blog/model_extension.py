# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

class RedisKeys:
    news_views = 'news_views_%s'
    pop_news = 'pop_news'
    preview_news_key = 'preview_news_%s'

class NewsPreview:
    def __init__(self,id, title, preview, slug):
        self.id = id
        self.title = title
        self.preview = preview
        self.slug = slug
