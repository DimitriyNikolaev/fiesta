# -*- coding: utf-8 -*-

__author__ = 'dimitriy'
import datetime
from pytz import utc
from django import forms
from django.forms import ModelForm, DateField
from fiesta_core.apps.blog.models import News,NewsPhoto, NewsTags, Subnews
from fiesta_core.forms.widgets import ImageInput, JSDateTimePickerWidget
from django.forms.models import inlineformset_factory
from fiesta_core.global_utils.image_utils import get_preview, get_thumbnail

from django import conf

from django.utils import encoding

try:
    # Django 1.5 have some permutations.
    from django.utils import text as src_pkg
    from django.utils.text import slugify as dj_slugify
except ImportError:
    from django.template import defaultfilters as src_pkg
    from django.template.defaultfilters import slugify as dj_slugify
import unidecode
def slugify(value):
    value = encoding.smart_unicode(value)
    return dj_slugify(encoding.smart_unicode(unidecode.unidecode(value)))


class NewsForm(ModelForm):
    date_added =  forms.DateField(input_formats=('%d.%m.%Y',))
    #time_added = forms.TimeField(widget=JSDateTimePickerWidget(), input_formats=('%H:%M',))
    event_date = forms.DateField(input_formats=('%d.%m.%Y',), required=False)
    deadline_date = forms.DateField(input_formats=('%d.%m.%Y',), required=False)
    def __init__(self,*args,**kwargs):
        ModelForm.__init__(self,*args,**kwargs)
        #first argument, index is the position of the field you want it to come before
        self.fields.insert(6,'time_added',forms.TimeField(widget=JSDateTimePickerWidget(), input_formats=('%H:%M',), required=True))
        if not self.instance.id:
            self.instance.date_added = utc.localize(datetime.datetime.today())

        self.fields['time_added'].initial = self.instance.date_added.time()
    class Meta:
        model = News

        # widgets = {
        #     'time_added':JSDateTimePickerWidget()
        #     }



    def save(self):
        object = super(NewsForm, self).save(False)
        object.date_added = utc.localize(datetime.datetime.combine(self.cleaned_data['date_added'], self.cleaned_data['time_added']))
        object.save()
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
        if not self.cleaned_data['slug'] or self.cleaned_data['slug'] == '':
            self.cleaned_data['slug'] = slugify(self.cleaned_data['title'])

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
        if not obj.preview:
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
    event_date = forms.DateField(input_formats=('%d.%m.%Y',), required=False)
    deadline_date = forms.DateField(input_formats=('%d.%m.%Y',), required=False)
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
        exclude = ('news','is_newsphoto','display_order', 'preview', 'thumbnail')

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