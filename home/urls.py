from django.urls import path, include
from . import views
from sponsor.views import PaypalCancelView, PaypalReturnView
from django.conf import settings
from django.conf.urls.static import static
from paypal.standard.ipn import urls as paypal_urls

urlpatterns = [
    path("", views.home, name="home-page"),
    path("terms-and-conditions/", views.TermsAndConditions.as_view(), name="tnc"),
    path("privacy-policy/", views.PrivacyPolicy.as_view(), name="privacy-policy"),
    path("copyright-notice/", views.CopyrightPolicy.as_view(), name="copyright-notice"),
    path("donate-campaign/<slug:slug>", views.campaign_donate, name="campaign-donate"),
    path("paypal/", include(paypal_urls)),
    path("paypal-return/", PaypalReturnView.as_view(), name="paypal-return"),
    path("paypal-cancel/", PaypalCancelView.as_view(), name="paypal-cancel"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
