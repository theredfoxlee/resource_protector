from django.db import models
from django.conf import settings
from django.contrib.auth import hashers

import uuid

def _tmpname(instance, filename):
    return f'{filename}-{str(uuid.uuid4())}'

class _ProtectedResourceBaseModel(models.Model):
    """ Base model for passowrd protected resources. """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)

    password = models.CharField(max_length=100, default=None, null=True)  # HASH

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_password = self.password

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.password != self._cached_password:
            # Password changed / newly set -> hash it.
            # ---
            # It's done here mainly because of admin
            # panel which treats password field as a
            # regular CharField.
            self.password = hashers.make_password(str(self.password))
        super().save(force_insert, force_update, *args, **kwargs)
        self._cached_password = self.password

    class Meta:
        abstract=True

class SavedFileModel(_ProtectedResourceBaseModel):
    """ Plain model used for file saved in storage. """

    file = models.FileField(upload_to=_tmpname)

class SavedUrlModel(_ProtectedResourceBaseModel):
    """ Plain model used for file saved in storage. """

    url = models.URLField(max_length=2048)
