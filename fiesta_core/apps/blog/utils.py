# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

def upload_to_path(instance,filename):
    if instance.is_newsphoto is not None:
        return'images/%s' % '%(news)s/%(id)d/%(id)d_%(fn)s'% {'news': 'news' if instance.is_newsphoto else 'subnews','id':instance.news.id,'fn':filename}
    else:
        return 'imeges/temp/%s/%s/%s' % instance,instance.id,filename
