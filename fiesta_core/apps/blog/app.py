# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.conf.urls import patterns,url
from fiesta_core.core.application import Application

from views import NewsStream


class BlogApp(Application):
    name = 'blog'
    #views
    news_stream = NewsStream
    def get_urls(self):
        urlpatterns = patterns('',
        url(r'^$',self.news_stream.as_view(), name='index')
        )
        return self.post_process_urls(urlpatterns)

application = BlogApp()


