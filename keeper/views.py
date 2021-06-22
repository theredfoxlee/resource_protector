from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import BaseUserManager
from django.urls import reverse

from .forms import FileUploadForm
from .forms import UrlShorteningForm
from .forms import PasswordForm
from .models import SavedFileModel
from .models import SavedUrlModel
from .models import UserExtModel

import string
import random

def _gen_password(N):
    # https://stackoverflow.com/a/2257449
    return ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(N)
    )

@login_required
def home(request):
    # TODO: Refactor
    user_agent = request.META.get('HTTP_USER_AGENT')

    if user_agent:
        user_ext_model = UserExtModel.objects.get(user=request.user)
        user_ext_model.last_user_agent = user_agent
        user_ext_model.save()

    message = 'Upload some files or save URLs, m8!'

    file_upload_form = None
    url_shortening_form = None

    url = ''
    password = ''

    if request.method == 'POST':
        password = _gen_password(10)

        if 'FileUploadSubmit' in request.POST:
            file_upload_form = FileUploadForm(request.POST, request.FILES)

            if file_upload_form.is_valid():

                saved_file_model = file_upload_form.save(commit=False)
                saved_file_model.user = request.user
                saved_file_model.password = password
                saved_file_model.save()

                file_upload_form = FileUploadForm()
                url_shortening_form = UrlShorteningForm()

                url = reverse('get_file', kwargs={'uuid': str(saved_file_model.uuid)})

                file_upload_form = FileUploadForm()
                url_shortening_form = UrlShorteningForm()

                #return redirect('home')
            else:
                message = 'Failed to upload file / FileUploadSubmit not valid.'
        elif 'UrlShorteningForm' in request.POST:
            url_shortening_form = UrlShorteningForm(request.POST)

            if url_shortening_form.is_valid():
                saved_url_model = url_shortening_form.save(commit=False)
                saved_url_model.user = request.user
                saved_url_model.password = password
                saved_url_model.save()

                url = reverse('get_url', kwargs={'uuid': str(saved_url_model.uuid)})

                file_upload_form = FileUploadForm()
                url_shortening_form = UrlShorteningForm()

                #return redirect('home')
            else:
                message = 'Failed to upload file / UrlShorteningForm not valid.'
        else:
            message = 'Unknown form!'

            file_upload_form = FileUploadForm()
            url_shortening_form = UrlShorteningForm()

    if file_upload_form is None:
        file_upload_form = FileUploadForm()

    if url_shortening_form is None:
        url_shortening_form = UrlShorteningForm()

    saved_file_models = SavedFileModel.objects.filter(user=request.user)
    saved_url_models = SavedUrlModel.objects.filter(user=request.user)

    return render(request, 'keeper/home.html', {
        'file_upload_form': file_upload_form,
        'url_shortening_form': url_shortening_form,
        'message': message,
        'saved_file_models': saved_file_models,
        'saved_url_models': saved_url_models,
        'user': str(request.user),
        'url': url,
        'password': password,
    })

def get_file(request, uuid):
    message = 'Give me resource password, m8!'

    password_form = None

    if request.method == 'POST':
        password_form = PasswordForm(request.POST)

        if password_form.is_valid():
            try:
                saved_file_model = SavedFileModel.objects.get(uuid=uuid)
                if saved_file_model:
                    if password_form.cleaned_data['password'] == saved_file_model.password:
                        response = HttpResponse(
                            saved_file_model.file,
                            content_type='application/octet-stream'
                        )
                        response['Content-Disposition'] = f'attachment; filename={saved_file_model.get_original_filename()}'
                        return response
                    else:
                        message = 'Wrong password, m8!'
            except Exception as e:
                message = f'Exception: {str(e)}'
        else:
            message = 'Invalid form'

    if password_form is None:
        password_form = PasswordForm()

    return render(request, 'keeper/resource.html', {
        'form': password_form,
        'action': reverse('get_file', kwargs={'uuid': str(uuid)}),
        'message': message
    })

def get_url(request, uuid):
    message = 'Give me resource password, m8!'

    password_form = None

    if request.method == 'POST':
        password_form = PasswordForm(request.POST)

        if password_form.is_valid():
            try:
                saved_url_model = SavedUrlModel.objects.get(uuid=uuid)
                if saved_url_model:
                    if password_form.cleaned_data['password'] == saved_url_model.password:
                        return redirect(saved_url_model.url)
                    else:
                        message = 'Wrong password, m8!'
            except Exception as e:
                message = f'Exception: {str(e)}'
        else:
            message = 'Invalid form'

    if password_form is None:
        password_form = PasswordForm()

    return render(request, 'keeper/resource.html', {
        'form': password_form,
        'action': reverse('get_url', kwargs={'uuid': str(uuid)}),
        'message': message
    })
