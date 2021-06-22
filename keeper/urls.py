from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get/file/<str:uuid>', views.get_file, name='get_file'),
    path('get/url/<str:uuid>', views.get_url, name='get_url'),
]
