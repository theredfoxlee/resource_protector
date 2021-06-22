from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import FileUploadForm
from .forms import UrlShorteningForm
from .models import SavedFileModel
from .models import SavedUrlModel

@login_required
def home(request):
    message = 'Upload some files or save URLs, m8!'

    file_upload_form = None
    url_shortening_form = None

    if request.method == 'POST':

        if 'FileUploadSubmit' in request.POST:
            file_upload_form = FileUploadForm(request.POST, request.FILES)

            if file_upload_form.is_valid():
                saved_file_model = file_upload_form.save(commit=False)
                saved_file_model.user = request.user
                saved_file_model.save()

                return redirect('home')
            else:
                message = 'Failed to upload file / FileUploadSubmit not valid.'
        elif 'UrlShorteningForm' in request.POST:
            url_shortening_form = UrlShorteningForm(request.POST)

            if url_shortening_form.is_valid():
                saved_url_model = url_shortening_form.save(commit=False)
                saved_url_model.user = request.user
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

    return render(request, 'keeper/home.html', {
        'file_upload_form': file_upload_form,
        'url_shortening_form': url_shortening_form,
        'message': message,
    })
