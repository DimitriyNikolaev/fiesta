# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django import forms
from models import SocialUser

class SocialUserForm(forms.ModelForm):
    class Meta:
        model = SocialUser
