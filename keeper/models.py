from django.db import models
from django.conf import settings
from django.contrib.auth import hashers
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime
import uuid

def _tmpname(instance, filename):
    return f'{filename}-{str(uuid.uuid4())}'

class _ProtectedResourceBaseModel(models.Model):
    """ Base model for passowrd protected resources. """

    # Used for old resources purging via purge() method.
    created = models.DateTimeField(auto_now_add=True)

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

    @classmethod
    def purge(cls, seconds=24*60*60):
        max_resource_age_s = datetime.timedelta(seconds=seconds)
        edge_date = timezone.now() - max_resource_age_s
        return cls.objects.filter(created__lt=edge_date).delete()[0]

    class Meta:
        abstract=True

class SavedFileModel(_ProtectedResourceBaseModel):
    """ Plain model used for file saved in storage. """

    file = models.FileField(upload_to=_tmpname)

class SavedUrlModel(_ProtectedResourceBaseModel):
    """ Plain model used for file saved in storage. """

    url = models.URLField(max_length=2048)

class UserExtModel(models.Model):
    """ Extended information about user. """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    last_user_agent = models.CharField(max_length=1000, default=None, null=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_ext_model(sender, instance, created, **kwargs):
    if created:
        UserExtModel.objects.create(user=instance)
