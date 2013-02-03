# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.conf.urls import patterns, include
from fiesta_core.core.application import Application

from fiesta_core.apps.blog.app import application as blog_app
from fiesta_core.apps.dashboard.app import application as dashboard_app

class FiestaBlog(Application):
    name = 'Fiesta'

    blog_app = blog_app
    dashboard_app = dashboard_app

    def get_urls(self):
        urlpatterns = patterns('',
            (r'', include(self.blog_app.urls)),
            (r'^dashboard/', include(self.dashboard_app.urls))
        )
        return urlpatterns

application = FiestaBlog()