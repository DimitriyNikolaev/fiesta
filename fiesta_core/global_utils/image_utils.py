# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from StringIO import StringIO
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
    img = img.resize((400,300), Image.ANTIALIAS)
    img.save(thumb, 'JPEG')
    if hasattr(original_image, 'path'):
        name = 'preview_%s' %  os.path.basename(original_image.path)
    else:
        name = 'preview_%s' %  original_image.name
    if hasattr(original_image, 'content_type'):
        content_type =  original_image.content_type
    else: u'image/jpeg'
    return InMemoryUploadedFile(thumb, field, name, content_type, thumb.len, original_image.charset)