# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
import pickle
from datetime import datetime, date, timedelta
from pytz import utc
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.conf import settings
from models import News, NewsPhoto
from fiesta_core.global_utils.redis_adapter import redis_adapter
from model_extension import RedisKeys
from cacheops import cached_as_with_params
from fiesta_core.defaults import FIESTA_NEWSLINE_ENTITY_SLUGTYPES

@cached_as_with_params(News.objects.all())
def get_news_base_queryset(city, type, actualize):
    queryset = News.objects.filter(is_displayed=True, city=city, is_archive=False)
    if type:
        queryset = queryset.filter(Q(type=type) | Q(type=2))
        if actualize == 'today':
            queryset = queryset.filter(Q(event_date = date.today())
                                       | Q(event_date__lt=date.today(), deadline_date__gte=date.today()))
        elif actualize == 'future':
            queryset = queryset.filter(event_date__gt = date.today())
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
    paginate_by = 12
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
                return get_news_base_queryset(city,self.kwargs['type'], self.kwargs['actualize'] if 'actualize' in self.kwargs else None)
            elif 'slug_type' in self.kwargs and self.kwargs['slug_type'] in FIESTA_NEWSLINE_ENTITY_SLUGTYPES:
                return get_news_base_queryset(city,FIESTA_NEWSLINE_ENTITY_SLUGTYPES[self.kwargs['slug_type']],self.kwargs['actualize'] if 'actualize' in self.kwargs else None)
        return get_news_base_queryset(city,None, None)


    def get_context_data(self, **kwargs):
        # if self.request.flavour == 'mobile':
        #     self.template_name = 'mobile/blog/news_stream.html'
        context = super(NewsStream, self).get_context_data(**kwargs)
        q = self.get_search_query()
        if not q:
            context['summary'] = _('Latest news')
        else:
            context['summary'] = _("News matching '%(query)s'") % {'query': q}
            context['search_term'] = q
        #context['items_per_page'] = self.paginate_by
        return context

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            self.template_name = 'blog/news_stream.html'
        else:
            self.template_name = 'blog/partial/news_stream_page.html'
        return super(NewsStream,self).get(request, args, kwargs)

class SingleNewsView(DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'blog/single_news.html'

    def get_object(self):
        # Call the superclass
        object = super(SingleNewsView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        # if self.request.flavour == 'mobile':
        #     print('mobile deteted')
        context = super(SingleNewsView, self).get_context_data(**kwargs)
        context['views_count'] = self.setAnalitic()
        return context;

    def setAnalitic(self):
        if self.object:
            pk = self.object.id
            if settings.UNIC_TMP_USER_ID in self.request.COOKIES:
                unicId = self.request.COOKIES[settings.UNIC_TMP_USER_ID]
                redis_adapter.sadd(RedisKeys.news_views % pk, unicId)
            views_count = redis_adapter.scard(RedisKeys.news_views % pk)
            if self.object.is_displayed and not self.object.is_archive and self.object.date_added + timedelta(days=settings.TOP_NEWS_LIVETIME) > utc.localize(datetime.today()):
                redis_adapter.zadd(RedisKeys.pop_news, pk, views_count)
            else:
                redis_adapter.zrem(RedisKeys.pop_news, pk)
            return views_count
        return 0;


class AdvertisementView(TemplateView):
    template_name = 'blog/advertisement.html'

class ContactView(TemplateView):
    template_name = 'blog/contact.html'


