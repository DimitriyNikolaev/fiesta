# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.views.generic import ListView, CreateView
from fiesta_core.apps.blog.models import News
from forms import NewsForm,MewsPhotoImageSet

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

class AddOrUpdateNewsView(CreateView):
    template_name = 'dashboard/blog/news_add_or_update.html'
    model = News
    context_object_name = 'news'
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        ctx = super(AddOrUpdateNewsView, self).get_context_data(**kwargs)
        if 'photos_formset' not in ctx:
            ctx['photos_formset'] = MewsPhotoImageSet()
        return ctx