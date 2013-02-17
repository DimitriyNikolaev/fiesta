# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.conf.urls import url, patterns
from fiesta_core.core.application import Application

from fiesta_core.apps.account.views import UserRegistrationView

class AccountApplication(Application):
    name = 'account'
    user_registration = UserRegistrationView

    def get_urls(self):
        urlpatterns = patterns(''.
            url(r'^registration/$',self.user_registration.as_view(), name='registration' ),
        )
application = AccountApplication()