""" This module contains models for ResourceProtector app. """


from django.db import models

from django.conf import settings

from django.dispatch import receiver
from django.utils import timezone

import datetime
import uuid


# -- Protected resource models


class ProtectedResourceModel(models.Model):
    """ Model used as base class for protected resources. """

    class Meta:
        abstract = True

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    password = models.CharField(max_length=150, default=None, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def purge(cls, seconds=None):
        """ Utility method for removing proteced resources older than `seconds`.
            ---
            Return: number of deleted protected resources.
        """
        if seconds is None:
            seconds = 24 * 60 * 60  # 1 day
        edge_date = timezone.now() - datetime.timedelta(seconds=seconds)
        return cls.objects.filter(created__lt=edge_date).delete()[0]

def _upload_to(instance, filename):
    """ Return `uuid` as new filename for the resource. """
    return str(instance.pk)

class ProtectedFileModel(ProtectedResourceModel):
    """ Model used to represent protected file resource. """

    file = models.FileField(upload_to=_upload_to)
    original_name = models.CharField(max_length=300)

class ProtectedUrlModel(ProtectedResourceModel):
    """ Model used to represent protected file resource. """

    url = models.URLField(max_length=2048)


# -- Utility models


class UserExtModel(models.Model):
    """ Model used to store additional information about `settings.AUTH_USER_MODEL`. """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    user_agent = models.CharField(max_length=1000, default=None, null=True)


# -- Models related signals


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_user_ext_model(sender, instance, created, **kwargs):
    """ Create UserExtModel instance on `settings.AUTH_USER_MODEL` creation. """
    if created:
        UserExtModel.objects.create(user=instance)
