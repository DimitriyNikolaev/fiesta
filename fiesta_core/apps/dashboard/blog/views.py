# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from datetime import timedelta, datetime
from pytz import utc
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from fiesta_core.apps.blog.models import News, Subnews
from forms import NewsForm,NewsPhotoImageSet, SubnewsForm, SubnewsPhotoImageSet
from fiesta_core.apps.blog.model_extension import NewsPreview, RedisKeys
from fiesta_core.global_utils.redis_adapter import redis_adapter
from django.conf import settings
import pickle

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
        return News.objects.all().order_by('-date_added')

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

        photos_formset = NewsPhotoImageSet(self.request.POST, self.request.FILES, instance=self.object)

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
            #save preview to redis
            photos = news.news_photos.all()
            preview = NewsPreview(news.id,news.title, photos[0].thumbnail.url if photos.count() > 0 else '')
            preview_serialized = pickle.dumps(preview)
            redis_adapter.set(RedisKeys.preview_news_key % news.id, preview_serialized)
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
        ctx['subnews_list'] = self.object.subnews.all()
        return ctx
    def form_invalid(self, form):

        photos_formset = NewsPhotoImageSet(self.request.POST, self.request.FILES, instance=self.object)

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
            #save preview to redis
            photos = news.news_photos.all()
            preview = NewsPreview(news.id,news.title, photos[0].thumbnail.url if photos.count() > 0 else '')
            preview_serialized = pickle.dumps(preview)
            redis_adapter.set(RedisKeys.preview_news_key % news.id, preview_serialized)

            if not news.is_displayed:
                redis_adapter.zrem(RedisKeys.pop_news, news.id)
            elif news.date_added + timedelta(days=settings.TOP_NEWS_LIVETIME) > utc.localize(datetime.today()):
                redis_adapter.zadd(RedisKeys.pop_news, news.id, news.views_count)
            return HttpResponseRedirect(self.get_success_url())

        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the below errors"))


        news.delete()
        ctx = self.get_context_data(form=form, photo_formset=photos_formset)
        return self.render_to_response(ctx)

    def get_success_url(self):
        return reverse('fiesta:dashboard:news_list')

class AddSubnewsView(CreateView):
    template_name = 'dashboard/blog/subnews_add_or_update.html'
    model = Subnews
    context_object_name = 'subnews'
    form_class = SubnewsForm

    def get_context_data(self, **kwargs):
        ctx = super(AddSubnewsView, self).get_context_data(**kwargs)
        if 'photos_formset' not in ctx:
            ctx['photos_formset'] = SubnewsPhotoImageSet()
        ctx['parent'] = News.objects.get(pk=self.kwargs.get('parent', None))
        return ctx
    def form_invalid(self, form):

        photos_formset = SubnewsPhotoImageSet(self.request.POST, self.request.FILES)

        messages.error(self.request,
            _("Your submitted data was not valid - please "
              "correct the below errors"))
        ctx = self.get_context_data(form=form, photos_formset=photos_formset)
        return self.render_to_response(ctx)

    def form_valid(self, form):
        news = News.objects.get(pk=self.kwargs.get('parent', None))
        if(news):
            subnews = form.save(False)
            news.subnews.add(subnews)
            photos_formset = SubnewsPhotoImageSet(self.request.POST,
                self.request.FILES,
                instance=subnews)
            is_valid = all([photos_formset.is_valid()])
            if is_valid:
                photos_formset.save()
                return HttpResponseRedirect(self.get_success_url())

            messages.error(self.request,
                _("Your submitted data was not valid - please "
                "correct the below errors"))


            subnews.delete()
        ctx = self.get_context_data(form=form, photo_formset=photos_formset)
        return self.render_to_response(ctx)


    def get_success_url(self):
        return reverse('fiesta:dashboard:edit_news', kwargs={'pk':self.kwargs.get('parent', None)})


class UpdateSubnewsView(UpdateView):
    template_name = 'dashboard/blog/subnews_add_or_update.html'
    model = Subnews
    context_object_name = 'subnews'
    form_class = SubnewsForm


    def get_context_data(self, **kwargs):
        ctx = super(UpdateSubnewsView, self).get_context_data(**kwargs)
        if 'photos_formset' not in ctx:
            ctx['photos_formset'] = SubnewsPhotoImageSet(instance=self.object)
        ctx['parent'] = self.object.news
        return ctx
    def form_invalid(self, form):

        photos_formset = SubnewsPhotoImageSet(self.request.POST, self.request.FILES)

        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the below errors"))
        ctx = self.get_context_data(form=form, photos_formset=photos_formset)
        return self.render_to_response(ctx)

    def form_valid(self, form):
        subnews = form.save()

        photos_formset = SubnewsPhotoImageSet(self.request.POST,
                                           self.request.FILES,
                                           instance=subnews)
        is_valid = all([photos_formset.is_valid()])
        if is_valid:
            photos_formset.save()
            return HttpResponseRedirect(self.get_success_url(subnews.news.pk))

        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the below errors"))


        subnews.delete()
        ctx = self.get_context_data(form=form, photo_formset=photos_formset)
        return self.render_to_response(ctx)

    def get_success_url(self, pk):
        return reverse('fiesta:dashboard:edit_news',kwargs={'pk': pk})
