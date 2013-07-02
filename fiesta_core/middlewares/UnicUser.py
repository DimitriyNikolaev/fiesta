# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

import uuid
import time
import datetime
from django.utils.http import cookie_date
from django.conf import settings

class UnicUserMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if settings.UNIC_TMP_USER_ID not in request.COOKIES:
            request.COOKIES[settings.UNIC_TMP_USER_ID] = uuid.uuid1()
        if settings.UNIC_TMP_USER_CITY not in request.COOKIES:
            request.COOKIES[settings.UNIC_TMP_USER_CITY] = 1
        elif request.COOKIES[settings.UNIC_TMP_USER_CITY] == '0':
            request.COOKIES[settings.UNIC_TMP_USER_CITY] = 1

        return None

    def process_response(self, request, response):
        if hasattr(request, 'session'):
            if request.session.get_expire_at_browser_close():
                max_age = None
                expires = None
            else:
                max_age = request.session.get_expiry_age()
                expires_time = time.time() + max_age
                expires = cookie_date(expires_time)
        else:
            max_age = None
            expires_time = time.time()+1209960
            expires = cookie_date(expires_time)
        unicID = request.COOKIES[settings.UNIC_TMP_USER_ID] if settings.UNIC_TMP_USER_ID in request.COOKIES  else uuid.uuid1()
        user_city = request.COOKIES[settings.UNIC_TMP_USER_CITY] if settings.UNIC_TMP_USER_CITY in request.COOKIES else 1
        response.set_cookie(settings.UNIC_TMP_USER_ID, unicID, max_age=max_age,
                            expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                            path=settings.SESSION_COOKIE_PATH,
                            secure=settings.SESSION_COOKIE_SECURE or None,
                            httponly=settings.SESSION_COOKIE_HTTPONLY or None)
        response.set_cookie(settings.UNIC_TMP_USER_CITY, user_city, max_age=max_age,
                            expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                            path=settings.SESSION_COOKIE_PATH,
                            secure=settings.SESSION_COOKIE_SECURE or None)


        return response