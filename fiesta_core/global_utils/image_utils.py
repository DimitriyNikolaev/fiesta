# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from StringIO import StringIO
from django.conf import settings
import os

def get_preview(original_image, field):
    f = StringIO(original_image.read())
    thumb = StringIO()

    img = Image.open(f)

    if img.mode != "RGB":
        img = img.convert("RGB")


    # Метод thumb не используется, т.к. он не увеличивает размер изображения,
    # если оно меньше требуемого
    # img = img.crop((0, 0, min(img.size), min(img.size)))
    img = img.resize((settings.PREVIEW_IMG__WIDTH, settings.PREVIEW_IMG_HEIGHT), Image.ANTIALIAS)
    img.save(thumb, 'JPEG')
    if hasattr(original_image, 'path'):
        name = 'preview_%s' %  os.path.basename(original_image.path)
    else:
        name = 'preview_%s' %  original_image.name
    if hasattr(original_image, 'content_type'):
        content_type =  original_image.content_type
    else: u'image/jpeg'

    return InMemoryUploadedFile(thumb, field, name, content_type, thumb.len, original_image.charset)

def get_thumbnail(original_image,field):
    f = StringIO(original_image.read())
    thumb = StringIO()

    img = Image.open(f)

    if img.mode != "RGB":
        img = img.convert("RGB")


    # Метод thumb не используется, т.к. он не увеличивает размер изображения,
    # если оно меньше требуемого
    # img = img.crop((0, 0, min(img.size), min(img.size)))
    img.thumbnail((settings.THUMBNAIL_WIDTH, settings.THUMBNAIL_HEIGHT), Image.ANTIALIAS)
    img.save(thumb, 'JPEG')
    if hasattr(original_image, 'path'):
        name = 'thumb_%s' %  os.path.basename(original_image.path)
    else:
        name = 'thumb_%s' %  original_image.name
    if hasattr(original_image, 'content_type'):
        content_type =  original_image.content_type
    else: u'image/jpeg'
    original_image.seek(0)
    return InMemoryUploadedFile(thumb, field, name, content_type, thumb.len, original_image.charset)