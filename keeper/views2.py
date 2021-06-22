""" This module contains views for ResourceProtector app. """


from django.views.generic.base import View
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

from .forms2 import ProtectedFileForm
from .forms2 import ProtectedUrlForm
from .forms2 import PasswordForm

from .models2 import ProtectedFileModel
from .models2 import ProtectedUrlModel

import abc
import random
import string


class HomeView(LoginRequiredMixin, View):
    """ Home view of ResourceProtector app where resources (file/url) can be protected. """

    template_name = 'resource_protector/home.html'

    def get(self, request, *args, **kwargs):
        """ GET request handler. """
        return render(request, self.template_name, self.get_context_data(request=request))

    def post(self, request, *args, **kwargs):
        """ POST request handler. """
        context = {}

        if 'protected_file_submit' in request.POST:
            protected_file_form = ProtectedFileForm(request.POST, request.FILES)

            if protected_file_form.is_valid():
                # Retrieve model instance from ModelForm.
                protected_file = protected_file_form.save(commit=False)
                protected_file.user = request.user
                protected_file.password = gen_password(length=15)
                # Kepp the original file name for download.
                protected_file.original_name = request.FILES['file'].name
                # Upload file to S3 and save its "handle" in db.
                protected_file.save()

                protected_resource_name = 'file'

                context['protected_url'] = get_protected_resource_url(
                    resource_name=protected_resource_name,
                    uuid=protected_file.uuid
                )
                context['protected_password'] = str(protected_file.password)
                context['protected_resource_name'] = protected_resource_name
            else:
                # Leave populated form on site and print some errors.
                context['protected_file_form'] = protected_file_form
                context['error_message'] = 'ProtectedFileForm is not valid.'
        elif 'protected_url_submit' in request.POST:
            protected_url_form = ProtectedUrlForm(request.POST)

            if protected_url_form.is_valid():
                # Retrieve model instance from ModelForm.
                protected_url = protected_url_form.save(commit=False)
                protected_url.user = request.user
                protected_url.password = gen_password(length=15)
                protected_url.save()

                protected_resource_name = 'url'

                context['protected_url'] = get_protected_resource_url(
                    resource_name=protected_resource_name,
                    uuid=protected_url.uuid
                )
                context['protected_password'] = str(protected_url.password)
                context['protected_resource_name'] = protected_resource_name
            else:
                # Leave populated form on site and print some errors.
                context['protected_url_form'] = protected_url_form
                context['error_message'] = 'ProtectedUrlForm is not valid.'
        else:
            context['error_message'] = 'Invalid POST request.'

        return render(
            request,
            self.template_name,
            self.get_context_data(request=request, **context)
        )

    @staticmethod
    def get_context_data(request=None, **kwargs):
        """ Returns context with defaults. """
        context = kwargs.copy()
        # Empty strings are not used in home-template.
        if 'error_message' not in context:
            context['error_message'] = ''
        if'username' not in context:
            if request is not None:
                context['username'] = str(request.user)
            else:
                context['username'] = ''
        if 'protected_file_form' not in context:
            context['protected_file_form'] = ProtectedFileForm()
        if 'protected_url_form' not in context:
            context['protected_url_form'] = ProtectedUrlForm()
        if 'protected_url' not in context:
            context['protected_url'] = ''
            context['protected_password'] = ''
            context['protected_resource_name'] = ''
        return context

class ProtectedFilesView(LoginRequiredMixin, ListView):
    """ Generic view for html table of protected files. """

    template_name = 'resource_protector/protected_resource_list.html'

    model = ProtectedFileModel

    def get_context_data(self, **kwargs):
        """ Add enhanced_object_list to context (it's used to generate html table). """
        context = super().get_context_data(**kwargs)
        protected_resource_name = 'file'
        context['enhanced_object_list'] = [
            {
                'protected_url': get_protected_resource_url(
                    resource_name=protected_resource_name,
                    uuid=str(e.uuid)
                ),
                'password': str(e.password),
                'original_name': str(e.original_name),
                'created': str(e.created)
            }
            for e in self.object_list
        ]
        context['protected_resource_name'] = protected_resource_name
        context['username'] = self.request.user
        return context

class ProtectedUrlsView(LoginRequiredMixin, ListView):
    """ Generic view for html table of protected urls. """

    template_name = 'resource_protector/protected_resource_list.html'

    model = ProtectedUrlModel

    def get_context_data(self, **kwargs):
        """ Add enhanced_object_list to context (it's used to generate html table). """
        context = super().get_context_data(**kwargs)
        protected_resource_name = 'url'
        context['enhanced_object_list'] = [
            {
                'protected_url': get_protected_resource_url(
                    resource_name=protected_resource_name,
                    uuid=str(e.uuid)
                ),
                'password': str(e.password),
                'direct_url': str(e.url),
                'created': str(e.created)
            }
            for e in self.object_list
        ]
        context['protected_resource_name'] = protected_resource_name
        context['username'] = self.request.user
        return context

class _ProtectedResourceDownloadMixin(abc.ABC):
    """ Mixin used as a general logic for protected resource download. """

    template_name = 'resource_protector/protected_resource_download.html'

    protected_resource_model = None  # Override!

    def get(self, request, uuid, *args, **kwargs):
        """ GET request handler. """
        return render(request, self.template_name, self.get_context_data(request=request))

    def post(self, request, uuid, *args, **kwargs):
        """ POST request handler. """
        password_form = PasswordForm(request.POST)

        context = {}

        if password_form.is_valid():
            try:
                protected_resource = self.protected_resource_model.objects.get(uuid=uuid)
            except self.protected_resource_model.DoesNotExist:
                context['error_message'] = 'Resource does not exists.'
            else:
                if protected_resource.password == password_form.cleaned_data['password']:
                    return self.access_protected_resource(resource=protected_resource)
                else:
                    context['error_message'] = 'Invalid password.'
        else:
            context['error_message'] = 'PasswordForm is not valid.'

        return render(request, self.template_name, self.get_context_data(request=request, **context))

    @staticmethod
    def get_context_data(request=None, **kwargs):
        context = kwargs.copy()
        if 'password_form' not in kwargs:
            context['password_form'] = PasswordForm()
        if 'error_message' not in kwargs:
            context['error_message'] = ''
        return context

    @abc.abstractmethod
    def access_protected_resource(self, resource):
        """ Return `resourece` via HttpResponse. """

class ProtectedFileAccessView(_ProtectedResourceDownloadMixin, View):
    """ View used to access protected file. """

    protected_resource_model = ProtectedFileModel

    def access_protected_resource(self, resource):
        response = HttpResponse(
            resource.file,
            # TODO: add content_type guessing
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = (
            'attachment; filename='
            + resource.original_name
        )
        return response

class ProtectedUrlAccessView(_ProtectedResourceDownloadMixin, View):
    """ View used to access protected url. """

    protected_resource_model = ProtectedUrlModel

    def access_protected_resource(self, resource):
        return redirect(resource.url)


# -- View-utilities


def get_protected_resource_url(resource_name, uuid):
    """ Common way of creating urls for resources in ResourceProtector app. """
    return reverse(f'get_{resource_name}', kwargs={'uuid': uuid})

def gen_password(length):
    """ Common way of creating password of a given length in ResourceProtector app. """
    # Yup, it's taken from stackoverflow (https://stackoverflow.com/a/2257449).
    return ''.join(
        random.SystemRandom().choice(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            'abcdefghijklmnopqrstuvwxyz'
            '0123456789'
            '+/!@#$%^&*()'
        )
        for _ in range(length)
    )
