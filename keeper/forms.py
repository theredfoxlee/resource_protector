""" This module contains django-forms for keeper app. """

from django import forms


class FileUploadForm(forms.Form):
    """ Plain form used for file upload. """

    file = forms.FileField()  # binds to requests.FILES['file']


class UrlShorteningForm(forms.Form):
    """ Plain form used for url shortening. """

    url = forms.URLField(max_length=2048)
