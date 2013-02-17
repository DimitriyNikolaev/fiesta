# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.views.generic import TemplateView

class UserRegistrationView(TemplateView):
    template_name = 'account/registration_form.html'
