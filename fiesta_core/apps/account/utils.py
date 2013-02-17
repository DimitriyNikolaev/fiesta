# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

def upload_avatar_path(instance,filename):
    return 'imeges/users/%d_%s' % instance,instance.id,filename
