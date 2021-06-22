from django.urls import path

from . import views, views2

urlpatterns = [
    path('', views2.HomeView.as_view(), name='home'),
    path('access/file/<str:uuid>', views2.ProtectedFileAccessView.as_view(), name='get_file'),
    path('access/url/<str:uuid>', views2.ProtectedUrlAccessView.as_view(), name='get_url'),

    path('protected_files/', views2.ProtectedFilesView.as_view(), name='protected_files'),
    path('protected_urls/', views2.ProtectedUrlsView.as_view(), name='protected_urls'),
]
