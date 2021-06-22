from django.contrib import admin

from .models import SavedFileModel
from .models import SavedUrlModel
from .models import UserExtModel

admin.site.register(SavedFileModel)
admin.site.register(SavedUrlModel)
admin.site.register(UserExtModel)
