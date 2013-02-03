# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls import patterns,url
from fiesta_core.core.application import Application
from views import NewsList

class BlogApplication(Application):
    name='blog_dashboard'

    news_list = NewsList()

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^/$', self.news_list.as_view(), name='news_list'),
            #url(r'^add_news$',)
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required

application = BlogApplication()
