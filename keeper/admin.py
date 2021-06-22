from django.contrib import admin

from .models import ProtectedFileModel
from .models import ProtectedUrlModel
from .models import UserExtModel

admin.site.register(ProtectedFileModel)
admin.site.register(ProtectedUrlModel)
admin.site.register(UserExtModel)
