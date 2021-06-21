from django.db import models
from django.conf import settings

import uuid

def _tmpname(instance, filename):
    return f'{filename}-{str(uuid.uuid4())}'


class SavedFileModel(models.Model):
    """ Plain model used for file saved in storage. """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to=_tmpname)
