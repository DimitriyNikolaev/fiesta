# -*- coding: utf-8 -*-
__author__ = 'dimitriy'

from django import forms
from django.forms import ModelForm, DateField
from fiesta_core.apps.blog.models import News,NewsPhoto, NewsTags, Subnews
from fiesta_core.forms.widgets import ImageInput
from django.forms.models import inlineformset_factory
from fiesta_core.global_utils.image_utils import get_preview, get_thumbnail



class NewsForm(ModelForm):
    date_added = forms.DateField(input_formats=('%d-%m-%Y', '%d.%m.%Y', '%Y-%m-%d'))
    class Meta:
        model = News


    # def save(self):
    #     object = super(NewsForm, self).save(False)
    #     object.save()
    #     if hasattr(self, 'save_m2m'):
    #         self.save_m2m()
    #     return object



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
    type = forms.Select
    class Meta:
        model = NewsPhoto
        exclude = ('subnews','is_newsphoto', 'display_order', 'preview', 'thumbnail')

        # use ImageInput widget to create HTML displaying the
        # actual uploaded image and providing the upload dialog
        # when clicking on the actual image.
        widgets = {
            'image': ImageInput()
            }
    # def clean_preview(self):
    #     exist_preview = self.cleaned_data['preview']
    #     if exist_preview is None:
    #         image = self.cleaned_data['image']
    #         preview = get_preview(image,'preview')
    #         return preview
    #     return exist_preview


    def save(self, *args, **kwargs):
        # We infer the display order of the image based on the order of the image fields
        # within the formset.
        kwargs['commit'] = False
        obj = super(NewsImageForm, self).save(*args, **kwargs)
        obj.is_newsphoto = True
        preview = get_preview(self.cleaned_data['image'], 'preview')
        obj.preview.save(preview.name, preview)
        self.cleaned_data['image'].seek(0)
        thumbnail = get_thumbnail(self.cleaned_data['image'], 'thumbnail')
        obj.thumbnail.save(thumbnail.name,thumbnail)
        obj.display_order = self.get_display_order()
        obj.save()
        return obj

    def get_display_order(self):
        return self.prefix.split('-').pop()



NewsPhotoImageSet = inlineformset_factory(News, NewsPhoto,
    form=NewsImageForm,
    extra=5)

class SubnewsForm(ModelForm):
    class Meta:
        model = Subnews
        exclude = ('news')


    # def save(self):
    #     object = super(NewsForm, self).save(False)
    #     object.save()
    #     if hasattr(self, 'save_m2m'):
    #         self.save_m2m()
    #     return object

    def clean(self):
        data = self.cleaned_data
#        if 'parent' not in data and not data['title']:
#            raise forms.ValidationError(_("This field is required"))
#        elif 'parent' in data and data['parent'] is None and not data['title']:
#            raise forms.ValidationError(_("Parent products must have a title"))
            # calling the clean() method of BaseForm here is required to apply checks
        # for 'unique' field. This prevents e.g. the UPC field from raising
        # a DatabaseError.
        return super(SubnewsForm, self).clean()

class SubnewsImageForm(forms.ModelForm):
    type = forms.Select
    class Meta:
        model = NewsPhoto
        exclude = ('news','is_newsphoto')

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
        obj = super(SubnewsImageForm, self).save(*args, **kwargs)
        obj.display_order = self.get_display_order()
        obj.is_newsphoto = False
        obj.save()
        return obj

    def get_display_order(self):
        return self.prefix.split('-').pop()

SubnewsPhotoImageSet = inlineformset_factory(Subnews, NewsPhoto,
    form=SubnewsImageForm,
    extra=5)