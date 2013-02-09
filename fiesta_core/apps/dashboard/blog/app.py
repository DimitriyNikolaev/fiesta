# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls import patterns,url
from fiesta_core.core.application import Application
from views import NewsList,AddOrUpdateNewsView
from fiesta_core.apps.dashboard.nav import Node,register
from django.utils.translation import ugettext_lazy as _


node = Node(_('Blog'), 'fiesta:dashboard:news_list')
register(node, 10)


class BlogApplication(Application):
    name=None

    news_list = NewsList
    add_or_update_news = AddOrUpdateNewsView

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.news_list.as_view(), name='news_list'),
            url(r'^add_news/$',self.add_or_update_news.as_view(), name='add_or_update_news')
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required

application = BlogApplication()
