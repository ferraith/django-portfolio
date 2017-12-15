"""URL declarations of the portfolio app."""
from django.urls import path

from portfolio import views


app_name = 'portfolio'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index')
]
