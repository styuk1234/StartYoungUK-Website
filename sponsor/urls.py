from django.urls import path
from . import views

urlpatterns = [
    path('', views.sponsor, name="sponsor-us"),
]
