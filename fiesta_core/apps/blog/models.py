# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import datetime, date

from utils import upload_to_path

class News(models.Model):
    type = models.CharField(_('Type'),max_length=10, null=False, default='News', blank=False)
    title = models.CharField(_('Title'),max_length=255, null=False, default=_(''), blank=False)
    text = models.TextField(_('Text'), null=False, blank=False, default='' )
    date_added = models.DateTimeField('Date added',null=False,blank=False, default=datetime.now())
    event_date = models.DateTimeField(_('Event date'), null=True, blank=True)
    external_link = models.URLField(_('Externallink'), null=True, blank=True)
    place_name = models.CharField(_('Place name'), null=True, blank=True, max_length=100)
    deadline_date = models.DateTimeField(_('Deadline date'), null=True, blank=True)
    contacts = models.CharField(_('Contacts'), null=True, blank=True, max_length=120)
    is_displayed = models.BooleanField(_('Is_displayed'), null=False, blank=False, default=True)



class Subnews(models.Model):
    news = models.ForeignKey(News, null=False, blank=False)

    title = models.CharField(_('Title'),max_length=255, null=False, default=_(''), blank=False)
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


class NewsTags(models.Model):
    tag_value = models.CharField(_('News tag value'), max_length=100, null=False, blank=False)
    news = models.ManyToManyField(News, related_name='tags')
    pass




