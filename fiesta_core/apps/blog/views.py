# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.conf import settings
from models import News
from fiesta_core.global_utils.redis_adapter import redis_adapter

def gat_news_base_queryset():
    return News.objects.select_related('news_photos').filter(is_displayed=True)

class NewsStream(ListView):
    context_object_name = "news"
    template_name = 'blog/news_stream.html'
    paginate_by = 20
    model = News

    def get_search_query(self):
        q = self.request.GET.get('q', None)
        return q.strip() if q else q

    def get_queryset(self):
        q = self.get_search_query()
        if q:
            self.search_signal.send(sender=self, query=q, user=self.request.user)
            return gat_news_base_queryset().filter(title__icontains=q, is_displayed=True).order_by('date_added')
        else:
            if 'type' in self.kwargs:
                return gat_news_base_queryset().filter(type=self.kwargs['type']).order_by('date_added')
            else:
                return gat_news_base_queryset().filter().order_by('date_added')

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
        context['views_count'] = 0
        return context;

    def get(self, request, *args, **kwargs):
        if settings.UNIC_TMP_USER_ID in request.COOKIES:
            redis_adapter().sadd('news_%s' % '')
        return self.render_to_response(self.get_context_data(), **kwargs)
        pass

