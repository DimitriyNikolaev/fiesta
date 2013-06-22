# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
import pickle
from datetime import datetime, date, timedelta
from pytz import utc
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.conf import settings
from models import News, NewsPhoto
from fiesta_core.global_utils.redis_adapter import redis_adapter
from model_extension import RedisKeys
from cacheops import cached_as_with_params

@cached_as_with_params(News.objects.all())
def get_news_base_queryset(city, type):
    queryset = News.objects.filter(is_displayed=True, city=city)
    if type:
        queryset = queryset.filter(Q(type=type) | Q(type=1))
    queryset = queryset.order_by('-date_added').nocache()
    photos = NewsPhoto.objects.filter(display_order=0, subnews_id__isnull=True).nocache()
    photos_dict = {}
    for p in photos:
        photos_dict[p.news_id] = p
    for item in queryset:
        item.photo = photos_dict[item.id] if item.id in photos_dict.keys() else None
    return queryset

def get_news_search_queryset(city, q):
    queryset = News.objects.filter(is_displayed=True, city=city, title__icontains=q).order_by('-date_added')
    photos = NewsPhoto.objects.filter(display_order=0, subnews_id__isnull=True)
    photos_dict = {}
    for p in photos:
        photos_dict[p.news_id] = p
    for item in queryset:
        item.photo = photos_dict[item.id] if item.id in photos_dict.keys() else None
    return queryset


class NewsStream(ListView):
    context_object_name = "news"
    template_name = 'blog/news_stream.html'
    paginate_by = 7
    model = News

    def get_search_query(self):
        q = self.request.GET.get('q', None)
        return q.strip() if q else q

    def get_queryset(self):
        q = self.get_search_query()
        city = self.request.COOKIES[settings.UNIC_TMP_USER_CITY]
        if q:
            return get_news_search_queryset(city,q)
        else:
            if 'type' in self.kwargs:
                return get_news_base_queryset(city,self.kwargs['type'])
        return get_news_base_queryset(city,None)


    def get_context_data(self, **kwargs):
        context = super(NewsStream, self).get_context_data(**kwargs)
        q = self.get_search_query()
        if not q:
            context['summary'] = _('Latest news')
        else:
            context['summary'] = _("News matching '%(query)s'") % {'query': q}
            context['search_term'] = q
        return context

class SingleNewsView(DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'blog/single_news.html'

    def get_object(self):
        # Call the superclass
        object = super(SingleNewsView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        context = super(SingleNewsView, self).get_context_data(**kwargs)
        context['views_count'] = self.setAnalitic()
        return context;

    def setAnalitic(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if settings.UNIC_TMP_USER_ID in self.request.COOKIES:
            unicId = self.request.COOKIES[settings.UNIC_TMP_USER_ID]
            redis_adapter.sadd(RedisKeys.news_views % pk, unicId)
        views_count = redis_adapter.scard(RedisKeys.news_views % pk)
        if self.object.date_added + timedelta(days=settings.TOP_NEWS_LIVETIME) < utc.localize(datetime.today()):
            redis_adapter.zadd(RedisKeys.pop_news, pk, views_count)
        else:
            redis_adapter.zrem(RedisKeys.pop_news, pk)
        return views_count





