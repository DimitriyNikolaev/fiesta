# -*- coding: utf-8 -*-
from django.core.context_processors import csrf
from fiesta_core.defaults import FIESTA_NEWS_CITY
from django.conf import settings
__author__ = 'dimitriy'

def user_metadata(request):
    avatar = "/static/fiesta_core/img/default_avatar.png"
    #if request.user.is_authenticated():
        #avatar = request.user.get_profile().avatar.url
    index_city = [t[0] for t in FIESTA_NEWS_CITY].index(int(request.COOKIES[settings.UNIC_TMP_USER_CITY]))
    if index_city > 0:
        city = FIESTA_NEWS_CITY[index_city][1]
    else:
        city = FIESTA_NEWS_CITY[0][1]
    c = {'current_path': request.path, 'user': request.user, 'avatar': avatar, 'city': city, 'site_domain': settings.SITE_DOMAIN }

    c.update(csrf(request))
    return c
