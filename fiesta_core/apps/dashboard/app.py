# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.conf.urls import patterns, url, include
from django.contrib.admin.views.decorators import staff_member_required
from fiesta_core.apps.dashboard.views import IndexView


from fiesta_core.core.application import Application


class DashboardApplication(Application):
    name = 'dashboard'

    index_view = IndexView

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.index_view.as_view(), name='index'),

        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = DashboardApplication()
