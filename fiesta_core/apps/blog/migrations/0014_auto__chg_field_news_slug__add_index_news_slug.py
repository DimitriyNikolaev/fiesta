# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'News.slug'
        db.alter_column(u'blog_news', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=140, unique=True, null=True))
        # Adding index on 'News', fields ['slug']
        db.create_index(u'blog_news', ['slug'])


    def backwards(self, orm):
        # Removing index on 'News', fields ['slug']
        db.delete_index(u'blog_news', ['slug'])


        # Changing field 'News.slug'
        db.alter_column(u'blog_news', 'slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40, null=True))

    models = {
        u'blog.news': {
            'Meta': {'object_name': 'News'},
            'city': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 9, 0, 0)'}),
            'deadline_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'external_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_displayed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '2'}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '140', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'blog.newsphoto': {
            'Meta': {'ordering': "['display_order']", 'unique_together': "(('news', 'subnews', 'display_order'),)", 'object_name': 'NewsPhoto'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_newsphoto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'news_photos'", 'null': 'True', 'to': u"orm['blog.News']"}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subnews': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subnews_photos'", 'null': 'True', 'to': u"orm['blog.Subnews']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'blog.newstags': {
            'Meta': {'object_name': 'NewsTags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags'", 'symmetrical': 'False', 'to': u"orm['blog.News']"}),
            'tag_value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'blog.subnews': {
            'Meta': {'object_name': 'Subnews'},
            'contacts': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'deadline_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'external_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subnews'", 'to': u"orm['blog.News']"}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        }
    }

    complete_apps = ['blog']