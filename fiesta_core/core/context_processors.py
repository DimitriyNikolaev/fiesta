# -*- coding: utf-8 -*-
from django.core.context_processors import csrf

__author__ = 'dimitriy'

def user_metadata(request):
    avatar = "/static/img/default_avatar.png"
    #if request.user.is_authenticated():
        #avatar = request.user.get_profile().avatar.url

    c = {'current_path': request.path, 'user': request.user, 'avatar': avatar}

    c.update(csrf(request))
    return c
