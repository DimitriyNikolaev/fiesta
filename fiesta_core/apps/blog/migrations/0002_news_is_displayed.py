# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'News.is_displayed'
        db.add_column('blog_news', 'is_displayed',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'News.is_displayed'
        db.delete_column('blog_news', 'is_displayed')


    models = {
        'blog.news': {
            'Meta': {'object_name': 'News'},
            'contacts': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 2, 0, 0)'}),
            'deadline_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'external_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_displayed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Project-Id-Version: Django\\nReport-Msgid-Bugs-To: \\nPOT-Creation-Date: 2012-03-23 02:36+0100\\nPO-Revision-Date: 2010-05-13 15:35+0200\\nLast-Translator: Django team\\nLanguage-Team: English <en@li.org>\\nLanguage: en\\nMIME-Version: 1.0\\nContent-Type: text/plain; charset=UTF-8\\nContent-Transfer-Encoding: 8bit\\n'", 'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'News'", 'max_length': '10'})
        },
        'blog.newsphoto': {
            'Meta': {'object_name': 'NewsPhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_newsphoto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'news_photos'", 'null': 'True', 'to': "orm['blog.News']"}),
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
            'news': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.News']"}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Project-Id-Version: Django\\nReport-Msgid-Bugs-To: \\nPOT-Creation-Date: 2012-03-23 02:36+0100\\nPO-Revision-Date: 2010-05-13 15:35+0200\\nLast-Translator: Django team\\nLanguage-Team: English <en@li.org>\\nLanguage: en\\nMIME-Version: 1.0\\nContent-Type: text/plain; charset=UTF-8\\nContent-Transfer-Encoding: 8bit\\n'", 'max_length': '255'})
        }
    }

    complete_apps = ['blog']