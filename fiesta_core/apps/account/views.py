# -*- coding: utf-8 -*-
import django

__author__ = 'dimitriy'
import urlparse
from django.views.generic import TemplateView,FormView
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import (authenticate, login as auth_login,
                                 logout as auth_logout)
from fiesta_core.apps.account.forms import EmailAuthenticationForm, EmailUserCreationForm, SocialUserForm
from models import SocialUser

class UserSignInView(TemplateView):
    template_name = 'account/signin_form.html'

class UserRegistrationView(TemplateView):
    template_name = 'account/registration_form.html'
    registration_prefix = 'registration'
    redirect_field_name = 'next'

    def check_redirect(self, context):
        redirect_to = context.get(self.redirect_field_name)
        if not redirect_to:
            return settings.LOGIN_REDIRECT_URL

        netloc = urlparse.urlparse(redirect_to)[1]
        if netloc and netloc != self.request.get_host():
            return settings.LOGIN_REDIRECT_URL

        return redirect_to
    def send_registration_email(self, user):
        pass

    def get_context_data(self, *args, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(*args, **kwargs)
        redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')
        context[self.redirect_field_name] = redirect_to
        context['registration_form'] = EmailUserCreationForm(
            prefix=self.registration_prefix
        )
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        redirect_to = self.check_redirect(context)

        registration_form = EmailUserCreationForm(
            prefix=self.registration_prefix,
            data=request.POST
        )
        context['registration_form'] = registration_form

        if registration_form.is_valid():
            self._register_user(registration_form)
            return HttpResponseRedirect(redirect_to)

        self.request.session.set_test_cookie()
        return self.render_to_response(context)

    def _register_user(self, form):
        """
        Register a new user from the data in *form*. If
        ``OSCAR_SEND_REGISTRATION_EMAIL`` is set to ``True`` a
        registration email will be send to the provided email address.
        A new user account is created and the user is then logged in.
        """
        user = form.save()

        if getattr(settings, 'FIESTA_SEND_REGISTRATION_EMAIL', True):
            self.send_registration_email(user)

        try:
            user = authenticate(
                username=user.email,
                password=form.cleaned_data['password1'])
        except SocialUser.MultipleObjectsReturned:
            # Handle race condition where the registration request is made
            # multiple times in quick succession.  This leads to both requests
            # passing the uniqueness check and creating users (as the first one
            # hasn't committed when the second one runs the check).  We retain
            # the first one and delete the dupes.
            users = SocialUser.objects.filter(email=user.email)
            user = users[0]
            for u in users[1:]:
                u.delete()

        auth_login(self.request, user)
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

class UserProfileView(FormView):
    template_name = 'account/user_profile.html'
    form_class = SocialUserForm


    def get_form_kwargs(self):
        kwargs = super(UserProfileView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        #messages.success(self.request, "Profile updated")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('fiesta:account:profile')
