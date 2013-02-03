# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'dashboard/layout.html'

