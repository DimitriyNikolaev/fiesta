# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.conf.urls import patterns,url
from fiesta_core.core.application import Application

from views import NewsStream,SingleNewsView


class BlogApp(Application):
    name = 'blog'
    #views
    news_stream = NewsStream
    single_news = SingleNewsView
    def get_urls(self):
        urlpatterns = patterns('',
        url(r'^$',self.news_stream.as_view(), name='index'),
        url(r'^(?P<type>\d+)$',self.news_stream.as_view(), name='stream_type'),
        url(r'^news/(?P<pk>\d+)/$', self.single_news.as_view(), name='single_news')
        )
        return self.post_process_urls(urlpatterns)

application = BlogApp()


