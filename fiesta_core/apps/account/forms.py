# -*- coding: utf-8 -*-
__author__ = 'dimitriy'
import random
import string
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from models import SocialUser
from fiesta_core.forms.widgets import ImageInput

def generate_username():
    uname = ''.join([random.choice(string.letters + string.digits + '_') for i in range(30)])
    try:
        SocialUser.objects.get(username=uname)
        return generate_username()
    except SocialUser.DoesNotExist:
        return uname
class CommonPasswordValidator(validators.BaseValidator):
    # See http://www.smartplanet.com/blog/business-brains/top-20-most-common-passwords-of-all-time-revealed-8216123456-8216princess-8216qwerty/4519
    forbidden_passwords = [
        'password',
        '1234',
        '12345'
        '123456',
        '123456y',
        '123456789',
        'iloveyou',
        'princess',
        'monkey',
        'rockyou',
        'babygirl',
        'monkey',
        'qwerty',
        '654321',
        'dragon',
        'pussy',
        'baseball',
        'football',
        'letmein',
        'monkey',
        '696969',
        'abc123',
        'qwe123',
        'qweasd',
        'mustang',
        'michael',
        'shadow',
        'master',
        'jennifer',
        '111111',
        '2000',
        'jordan',
        'superman'
        'harley'
    ]
    message = _("Please choose a less common password")
    code = 'password'

    def __init__(self, password_file=None):
        self.limit_value = password_file

    def clean(self, value):
        return value.strip()

    def compare(self, value, limit):
        return value in self.forbidden_passwords

    def get_forbidden_passwords(self):
        if self.limit_value is None:
            return self.forbidden_passwords

class SocialUserForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['instance'] = user
        super(SocialUserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SocialUser
        fields=('username', 'first_name', 'last_name', 'avatar', 'aboutSelf', 'social_status')

    def save(self, commit=True):
        user = super(SocialUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    """
    Extends the standard django AuthenticationForm, to support 75 character
    usernames. 75 character usernames are needed to support the EmailOrUsername
    auth backend.
    """
    username = forms.EmailField(label=_('Email Address'))
class EmailUserCreationForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email Address'))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput,
                                validators=[validators.MinLengthValidator(6),
                                            CommonPasswordValidator()])
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput)

    class Meta:
        model = SocialUser
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            SocialUser.objects.get(email=email)
        except SocialUser.DoesNotExist:
            return email
        raise forms.ValidationError(_("A user with that email address already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')

        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = generate_username()
        user.avatar = '/media/no_avatar.png'

        if commit:
            user.save()
        return user



