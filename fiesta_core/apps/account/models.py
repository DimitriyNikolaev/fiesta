# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.db import models
from django.contrib.auth.models import User, UserManager
from utils import upload_avatar_path

class SocialUser(User):
    objects = UserManager()
    avatar = models.ImageField(upload_to=upload_avatar_path)
    aboutSelf = models.TextField(max_length=300, blank=True, null=True)
    social_status = models.CharField(max_length=255, blank=True, null=True)