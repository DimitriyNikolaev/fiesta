# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.conf.urls import patterns,url
from fiesta_core.core.application import Application

from views import NewsStream,SingleNewsView, AdvertisementView, ContactView


class BlogApp(Application):
    name = 'blog'
    #views
    news_stream = NewsStream
    single_news = SingleNewsView
    advertisement = AdvertisementView
    contact = ContactView
    def get_urls(self):
        urlpatterns = patterns('',
        url(r'^$',self.news_stream.as_view(), name='index'),
        url(r'^(?P<type>\d+)$',self.news_stream.as_view(), name='stream_type'),
        url(r'^news/(?P<pk>\d+)/$', self.single_news.as_view(), name='single_news'),
        url(r'^advertisement',self.advertisement.as_view(),name='advertisement'),
        url(r'^contact',self.contact.as_view(),name='contact')
        )
        return self.post_process_urls(urlpatterns)

application = BlogApp()


