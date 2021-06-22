""" This module contains routing for keeper app. """


from django.urls import path

from .views2 import HomeView


urlpatterns = [
	path('', HomeView.as_view())
]
