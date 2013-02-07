# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.conf.urls import patterns, url, include
from django.contrib.admin.views.decorators import staff_member_required
from fiesta_core.apps.dashboard.views import IndexView


from fiesta_core.core.application import Application
from fiesta_core.apps.dashboard.blog.app import application as blog_app


class DashboardApplication(Application):
    name = 'dashboard'

    index_view = IndexView
    blog_application = blog_app

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.index_view.as_view(), name='dashboard-index'),
            url(r'^blog/',include(self.blog_application.urls))
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = DashboardApplication()
