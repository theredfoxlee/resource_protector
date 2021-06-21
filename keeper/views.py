from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import FileUploadForm
from .models import SavedFileModel


@login_required
def home(request):
    message = 'Upload some files, m8!'

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            sfm = SavedFileModel(user=request.user, file=request.FILES['file'])
            sfm.save()

            return redirect('home')
        else:
            message = 'Failed to upload file / form not valid.'
    else:
        form = FileUploadForm()

    return render(request, 'keeper/home.html', {'form': form, 'message': message})
