from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('access/file/<str:uuid>', views.ProtectedFileAccessView.as_view(), name='get_file'),
    path('access/url/<str:uuid>', views.ProtectedUrlAccessView.as_view(), name='get_url'),

    path('protected_files/', views.ProtectedFilesView.as_view(), name='protected_files'),
    path('protected_urls/', views.ProtectedUrlsView.as_view(), name='protected_urls'),

    path('protected_files/alt', views.ProtectedFilesAltView.as_view(), name='protected_files_alt'),
    path('protected_urls/alt', views.ProtectedUrlsAltView.as_view(), name='protected_urls_alt'),
]
