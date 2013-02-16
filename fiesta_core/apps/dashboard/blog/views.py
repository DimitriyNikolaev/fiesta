# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from fiesta_core.apps.blog.models import News
from forms import NewsForm,NewsPhotoImageSet

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

class AddNewsView(CreateView):
    template_name = 'dashboard/blog/news_add_or_update.html'
    model = News
    context_object_name = 'news'
    form_class = NewsForm


    def get_context_data(self, **kwargs):
        ctx = super(AddNewsView, self).get_context_data(**kwargs)
        if 'photos_formset' not in ctx:
            ctx['photos_formset'] = NewsPhotoImageSet()
        return ctx
    def form_invalid(self, form):

        photos_formset = NewsPhotoImageSet(self.request.POST, self.request.FILES)

        messages.error(self.request,
            _("Your submitted data was not valid - please "
              "correct the below errors"))
        ctx = self.get_context_data(form=form, photos_formset=photos_formset)
        return self.render_to_response(ctx)

    def form_valid(self, form):
        news = form.save()

        photos_formset = NewsPhotoImageSet(self.request.POST,
            self.request.FILES,
            instance=news)
        is_valid = all([photos_formset.is_valid()])
        if is_valid:
            photos_formset.save()
            return HttpResponseRedirect(self.get_success_url())

        messages.error(self.request,
            _("Your submitted data was not valid - please "
              "correct the below errors"))


        news.delete()
        ctx = self.get_context_data(form=form, photo_formset=photos_formset)
        return self.render_to_response(ctx)

    def get_success_url(self):
        return reverse('fiesta:dashboard:news_list')

class UpdateNewsView(UpdateView):
    template_name = 'dashboard/blog/news_add_or_update.html'
    model = News
    context_object_name = 'news'
    form_class = NewsForm


    def get_context_data(self, **kwargs):
        ctx = super(UpdateNewsView, self).get_context_data(**kwargs)
        if 'photos_formset' not in ctx:
            ctx['photos_formset'] = NewsPhotoImageSet(instance=self.object)
        return ctx
    def form_invalid(self, form):

        photos_formset = NewsPhotoImageSet(self.request.POST, self.request.FILES)

        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the below errors"))
        ctx = self.get_context_data(form=form, photos_formset=photos_formset)
        return self.render_to_response(ctx)

    def form_valid(self, form):
        news = form.save()

        photos_formset = NewsPhotoImageSet(self.request.POST,
                                           self.request.FILES,
                                           instance=news)
        is_valid = all([photos_formset.is_valid()])
        if is_valid:
            photos_formset.save()
            return HttpResponseRedirect(self.get_success_url())

        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the below errors"))


        news.delete()
        ctx = self.get_context_data(form=form, photo_formset=photos_formset)
        return self.render_to_response(ctx)

    def get_success_url(self):
        return reverse('fiesta:dashboard:news_list')
