# -*- coding: utf-8 -*-
__author__ = 'dimitriy'


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from fiesta_core.apps.account.models import SocialUser


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = SocialUser

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = ('username', 'last_name', 'first_name',
                    'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'timezone'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )

admin.site.unregister(User)
admin.site.register(SocialUser, CustomUserAdmin)