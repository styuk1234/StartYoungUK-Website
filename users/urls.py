from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.register, name="register"),
    path('home', views.userhome, name='userhome'),
    path('profile', views.profile, name="profile"),
    # path('donate', views.donate, name="donate-money"),
    path('sdp', views.sdp, name="sdp"),
    path('mentor', views.buddy, name="mentor"),
    path('start_campaign', views.start_campaign, name="start_campaign")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)