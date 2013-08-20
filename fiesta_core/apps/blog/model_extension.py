# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

class RedisKeys:
    news_views = 'news_views_%s'
    pop_news = 'pop_news'
    preview_news_key = 'preview_news_%s'
    pop_news_by_group = 'pop_news_%s'

class NewsPreview:
    def __init__(self,id, title, preview, slug, date_from, date_to,description, img):
        self.id = id
        self.title = title
        self.preview = preview
        self.slug = slug
        self.date_from = date_from
        self.date_to = date_to
        self.description = description
        self.img = img
