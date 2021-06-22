from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import BaseUserManager

from .forms import FileUploadForm
from .forms import UrlShorteningForm
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

    if request.method == 'POST':
        password = _gen_password(10)

        if 'FileUploadSubmit' in request.POST:
            file_upload_form = FileUploadForm(request.POST, request.FILES)

            if file_upload_form.is_valid():

                saved_file_model = file_upload_form.save(commit=False)
                saved_file_model.user = request.user
                saved_file_model.password = password
                saved_file_model.save()

                return redirect('home')
            else:
                message = 'Failed to upload file / FileUploadSubmit not valid.'
        elif 'UrlShorteningForm' in request.POST:
            url_shortening_form = UrlShorteningForm(request.POST)

            if url_shortening_form.is_valid():
                saved_url_model = url_shortening_form.save(commit=False)
                saved_url_model.user = request.user
                saved_url_model.password = password
                saved_url_model.save()

                return redirect('home')
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
    })

def get_file(request, uuid):
    try:
        saved_file_model = SavedFileModel.objects.get(uuid=uuid)

        if saved_file_model:
            response = HttpResponse(
                saved_file_model.file,
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename={saved_file_model.file.name.lstrip(str(saved_file_model.uuid) + "__")}'
            return response
    except Exception as e:
        print('exception', str(e))
        return HttpResponse(f'I do not know you: {uuid}')

def get_url(request, uuid):
    try:
        saved_url_model = SavedUrlModel.objects.get(uuid=uuid)

        if saved_url_model:
            return redirect(saved_url_model.url)
    except Exception as e:
        print('exception', str(e))
        return HttpResponse(f'I do not know you: {uuid}')
