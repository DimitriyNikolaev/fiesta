# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django import forms
from django.forms import ModelForm
from fiesta_core.apps.blog.models import News,NewsPhoto, NewsTags
from fiesta_core.forms.widgets import ImageInput
from django.forms.models import inlineformset_factory



class NewsForm(ModelForm):
    class Meta:
        model = News


    def save(self):
        object.save()
        if hasattr(self, 'save_m2m'):
            self.save_m2m()
        return object



    def clean(self):
        data = self.cleaned_data
#        if 'parent' not in data and not data['title']:
#            raise forms.ValidationError(_("This field is required"))
#        elif 'parent' in data and data['parent'] is None and not data['title']:
#            raise forms.ValidationError(_("Parent products must have a title"))
            # calling the clean() method of BaseForm here is required to apply checks
        # for 'unique' field. This prevents e.g. the UPC field from raising
        # a DatabaseError.
        return super(NewsForm, self).clean()

class NewsImageForm(forms.ModelForm):
    class Meta:
        model = NewsPhoto
        exclude = ('subnews','is_newsphoto')

        # use ImageInput widget to create HTML displaying the
        # actual uploaded image and providing the upload dialog
        # when clicking on the actual image.
        widgets = {
            'image': ImageInput(),
            }

    def save(self, *args, **kwargs):
        # We infer the display order of the image based on the order of the image fields
        # within the formset.
        kwargs['commit'] = False
        obj = super(NewsImageForm, self).save(*args, **kwargs)
        obj.display_order = self.get_display_order()
        obj.save()
        return obj

    def get_display_order(self):
        return self.prefix.split('-').pop()



MewsPhotoImageSet = inlineformset_factory(News, NewsPhoto,
    form=NewsImageForm,
    extra=2)

