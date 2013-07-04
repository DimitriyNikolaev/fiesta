# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import datetime, date
from fiesta_core.global_utils.redis_adapter import redis_adapter
from model_extension import RedisKeys
from utils import upload_to_path
from fiesta_core.defaults import FIESTA_NEWSLINE_ENTITY_TYPES, FIESTA_BLOG_LANGS, FIESTA_NEWS_CITY, news_types


class News(models.Model):
    type = models.PositiveSmallIntegerField(_('Type'),null=False, default=0, blank=False, choices=FIESTA_NEWSLINE_ENTITY_TYPES)
    lang = models.CharField(_('Language'), max_length=2, null=False, blank=False, default='ru', choices=FIESTA_BLOG_LANGS)
    title = models.CharField(_('Title'),max_length=255, null=False, default='', blank=False)
    description = models.TextField(_('Description'), null=True, blank=True, default='')
    text = models.TextField(_('Text'), null=False, blank=False, default='' )
    date_added = models.DateTimeField('Date added',null=False,blank=False, default=datetime.now())
    event_date = models.DateTimeField(_('Event date'), null=True, blank=True)
    external_link = models.URLField(_('Externallink'), null=True, blank=True)
    place_name = models.CharField(_('Place name'), null=True, blank=True, max_length=100)
    deadline_date = models.DateTimeField(_('Deadline date'), null=True, blank=True)
    contacts = models.CharField(_('Contacts'), null=True, blank=True, max_length=120)
    is_displayed = models.BooleanField(_('Is_displayed'), null=False, blank=False, default=True)
    city = models.PositiveSmallIntegerField(_('City'), null=True, blank=True, choices=FIESTA_NEWS_CITY)


    @property
    def views_count(self):
        return redis_adapter.scard(RedisKeys.news_views % self.id)
    @property
    def verbal_type(self):
        return news_types[self.type]

    @models.permalink
    def get_absolute_url(self):
        u"""Return a product's absolute url"""
        return ('catalogue:detail', (), {
            'product_slug': self.slug,
            'pk': self.id})





class Subnews(models.Model):
    news = models.ForeignKey(News, null=False, blank=False, related_name='subnews')
    title = models.CharField(_('Title'),max_length=255, null=False, default='', blank=False)
    text = models.TextField(_('Text'), null=False, blank=False, default='' )
    event_date = models.DateTimeField(_('Event date'), null=True, blank=True)
    external_link = models.URLField(_('Externallink'), null=True, blank=True)
    place_name = models.CharField(_('Place name'), null=True, blank=True, max_length=100)
    deadline_date = models.DateTimeField(_('Deadline date'), null=True, blank=True)
    contacts = models.CharField(_('Contacts'), null=True, blank=True, max_length=120)

class NewsPhoto(models.Model):
    news = models.ForeignKey(News,verbose_name=_('News photo'), null=True, blank=True, related_name='news_photos')
    subnews = models.ForeignKey(Subnews, verbose_name=_('Subnews photo'), null=True, blank=True, related_name='subnews_photos')
    is_newsphoto = models.BooleanField(_('is_newsphoto'), null=False, blank=False)
    image = models.ImageField(upload_to=upload_to_path)
    preview = models.ImageField(upload_to=upload_to_path, null=True, blank=True, default=None)
    thumbnail = models.ImageField(upload_to=upload_to_path, null=True, blank=True, default=None)
    display_order = models.PositiveIntegerField(_("Display Order"), default=0,
        help_text=_("""An image with a display order of
                       zero will be the primary image for a product"""))


    class Meta:
        unique_together = ("news", "subnews", "display_order")
        ordering = ["display_order"]
        verbose_name = _('News Photo')
        verbose_name_plural = _('News Photo')


    def save(self, force_insert=False, force_update=False, using=None):
        try:
            obj =  NewsPhoto.objects.get(id=self.id)
            if obj.image.path != self.image.path:
                obj.image.delete()
                obj.preview.delete()
                obj.thumbnail.delete()
        except:
            pass
        super(NewsPhoto, self).save()
    def delete(self, using=None):
        try:
            obj = NewsPhoto.objects.get(id=self.id)
            obj.image.delete()
            obj.preview.delete()
            obj.thumbnail.delete()
        except (NewsPhoto.DoesNotExist, ValueError):
            pass
        super(NewsPhoto, self).delete()




class NewsTags(models.Model):
    tag_value = models.CharField(_('News tag value'), max_length=100, null=False, blank=False)
    news = models.ManyToManyField(News, related_name='tags')
    pass




