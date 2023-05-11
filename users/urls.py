from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from paypal.standard.ipn import urls as paypal_urls

urlpatterns = [
    path("", views.register, name="register"),
    # path('home', views.userhome, name='userhome'),
    path("profile", views.profile, name="profile"),
    path("past_donations", views.past_donations, name="past_donations"),
    # path('donate', views.donate, name="donate-money"),
    path("sdp", views.sdp, name="sdp"),
    path("mentor", views.buddy, name="mentor"),
    path("start_campaign", views.start_campaign, name="start_campaign"),
    path("paypal", include(paypal_urls)),
    path("sdp-return", views.PaypalReturnView.as_view(), name="sdp-return"),
    path("sdp-cancel", views.PaypalCancelView.as_view(), name="sdp-cancel"),
    # path(
    #     "donation_pdf_receipt", views.donation_pdf_receipt, name="donation_pdf_receipt"
    # ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
