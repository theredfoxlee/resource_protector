from django.contrib import admin

from .models import SavedFileModel
from .models import SavedUrlModel

admin.site.register(SavedFileModel)
admin.site.register(SavedUrlModel)
