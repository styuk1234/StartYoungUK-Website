from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name="register"),
    path('home', views.userhome, name='userhome'),
    path('profile', views.profile, name="profile"),
    # path('donate', views.donate, name="donate-money"),
    path('sdp', views.sdp, name="sdp"),
    path('mentor', views.mentor, name="mentor"),
    
]