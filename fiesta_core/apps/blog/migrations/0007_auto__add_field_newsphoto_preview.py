# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NewsPhoto.preview'
        db.add_column('blog_newsphoto', 'preview',
                      self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NewsPhoto.preview'
        db.delete_column('blog_newsphoto', 'preview')


    models = {
        'blog.news': {
            'Meta': {'object_name': 'News'},
            'contacts': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 3, 0, 0)'}),
            'deadline_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'external_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_displayed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '2'}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'blog.newsphoto': {
            'Meta': {'ordering': "['display_order']", 'unique_together': "(('news', 'subnews', 'display_order'),)", 'object_name': 'NewsPhoto'},
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_newsphoto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'news_photos'", 'null': 'True', 'to': "orm['blog.News']"}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subnews': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subnews_photos'", 'null': 'True', 'to': "orm['blog.Subnews']"})
        },
        'blog.newstags': {
            'Meta': {'object_name': 'NewsTags'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags'", 'symmetrical': 'False', 'to': "orm['blog.News']"}),
            'tag_value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'blog.subnews': {
            'Meta': {'object_name': 'Subnews'},
            'contacts': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'deadline_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'external_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subnews'", 'to': "orm['blog.News']"}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        }
    }

    complete_apps = ['blog']