from django.db import models
from django.conf import settings

import uuid

def _tmpname(instance, filename):
    return f'{filename}-{str(uuid.uuid4())}'

class _ProtectedResourceBaseModel(models.Model):
    """ Base model for passowrd protected resources. """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    password = models.CharField(max_length=100)  # HASH

    class Meta:
        abstract=True

class SavedFileModel(_ProtectedResourceBaseModel):
    """ Plain model used for file saved in storage. """

    file = models.FileField(upload_to=_tmpname)

class SavedUrlModel(_ProtectedResourceBaseModel):
    """ Plain model used for file saved in storage. """

    url = models.URLField(max_length=2048)
