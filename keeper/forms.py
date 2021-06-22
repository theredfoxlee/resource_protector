""" This module contains django-forms for keeper app. """

from django import forms

from .models import SavedFileModel
from .models import SavedUrlModel

class FileUploadForm(forms.ModelForm):
    """ Plain form used for file upload. """

    class Meta:
        model = SavedFileModel
        fields = ['file']  # binds to requests.FILES['file']

class UrlShorteningForm(forms.ModelForm):
    """ Plain form used for url shortening. """

    class Meta:
        model = SavedUrlModel
        fields = ['url']  # binds to requests.FILES['file']
