""" This module contains forms for ResourceProtector app. """


from django import forms

from .models2 import ProtectedFileModel
from .models2 import ProtectedUrlModel


class ProtectedFileForm(forms.ModelForm):
    """ Form used for file upload (+ for model binding). """
    class Meta:
        model = ProtectedFileModel
        fields = ['file']


class ProtectedUrlForm(forms.ModelForm):
    """ Form used for url retrival (+ for model binding). """
    class Meta:
        model = ProtectedUrlModel
        fields = ['url']


class PasswordForm(forms.Form):
    """ Form used for password retrival. """
    password = forms.CharField(max_length=100)
