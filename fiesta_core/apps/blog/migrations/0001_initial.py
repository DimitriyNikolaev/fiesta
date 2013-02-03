# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table('blog_news', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='News', max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'Project-Id-Version: Django\nReport-Msgid-Bugs-To: \nPOT-Creation-Date: 2012-03-23 02:36+0100\nPO-Revision-Date: 2010-05-13 15:35+0200\nLast-Translator: Django team\nLanguage-Team: English <en@li.org>\nLanguage: en\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n', max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(default='')),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 27, 0, 0))),
            ('event_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('external_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('place_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('deadline_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('contacts', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
        ))
        db.send_create_signal('blog', ['News'])

        # Adding model 'Subnews'
        db.create_table('blog_subnews', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.News'])),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'Project-Id-Version: Django\nReport-Msgid-Bugs-To: \nPOT-Creation-Date: 2012-03-23 02:36+0100\nPO-Revision-Date: 2010-05-13 15:35+0200\nLast-Translator: Django team\nLanguage-Team: English <en@li.org>\nLanguage: en\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n', max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(default='')),
            ('event_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('external_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('place_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('deadline_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('contacts', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
        ))
        db.send_create_signal('blog', ['Subnews'])

        # Adding model 'NewsPhoto'
        db.create_table('blog_newsphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='news_photos', null=True, to=orm['blog.News'])),
            ('subnews', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subnews_photos', null=True, to=orm['blog.Subnews'])),
            ('is_newsphoto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('blog', ['NewsPhoto'])

        # Adding model 'NewsTags'
        db.create_table('blog_newstags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('blog', ['NewsTags'])

        # Adding M2M table for field news on 'NewsTags'
        db.create_table('blog_newstags_news', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newstags', models.ForeignKey(orm['blog.newstags'], null=False)),
            ('news', models.ForeignKey(orm['blog.news'], null=False))
        ))
        db.create_unique('blog_newstags_news', ['newstags_id', 'news_id'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table('blog_news')

        # Deleting model 'Subnews'
        db.delete_table('blog_subnews')

        # Deleting model 'NewsPhoto'
        db.delete_table('blog_newsphoto')

        # Deleting model 'NewsTags'
        db.delete_table('blog_newstags')

        # Removing M2M table for field news on 'NewsTags'
        db.delete_table('blog_newstags_news')


    models = {
        'blog.news': {
            'Meta': {'object_name': 'News'},
            'contacts': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 27, 0, 0)'}),
            'deadline_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'external_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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