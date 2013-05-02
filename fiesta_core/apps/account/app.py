# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.contrib.auth.decorators import login_required
from django.conf.urls import url, patterns
from fiesta_core.core.application import Application

from fiesta_core.apps.account.views import UserRegistrationView, UserProfileView

class AccountApplication(Application):
    name = 'account'
    user_registration = UserRegistrationView
    user_profile = UserProfileView

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^registration/$',self.user_registration.as_view(), name='registration' ),
            url(r'^profile/$',login_required(self.user_profile.as_view()), name='profile')
        )
        return urlpatterns
application = AccountApplication()