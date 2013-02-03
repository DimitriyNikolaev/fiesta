# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.views.generic import ListView
from fiesta_core.apps.blog.models import News

class NewsList(ListView):
    template_name = 'dashboard/blog/news_list.html'
    model=News
    paginate_by = 20
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        ctx = super(NewsList, self).get_context_data(**kwargs)
        #ctx['form'] = self.form
        return ctx

    def get_queryset(self):
        return News.objects.all()