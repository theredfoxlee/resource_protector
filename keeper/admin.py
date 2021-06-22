from django.contrib import admin

from .models2 import ProtectedFileModel
from .models2 import ProtectedUrlModel
from .models2 import UserExtModel2

admin.site.register(ProtectedFileModel)
admin.site.register(ProtectedUrlModel)
admin.site.register(UserExtModel2)
