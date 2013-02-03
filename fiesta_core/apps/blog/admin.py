# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.contrib import admin
from models import News,NewsPhoto, NewsTags,Subnews

admin.site.register(News)
admin.site.register(NewsPhoto)
admin.site.register(NewsTags)
admin.site.register(Subnews)