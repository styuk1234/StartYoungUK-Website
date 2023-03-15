from django.urls import path, include
from . import views
from paypal.standard.ipn import urls as paypal_urls

urlpatterns = [
    path('', views.sponsor, name="sponsor-us"),
    path('paypal/', include(paypal_urls)),
    path('paypal-return/', views.PaypalReturnView.as_view(), name='paypal-return'),
    path('paypal-cancel/', views.PaypalCancelView.as_view(), name='paypal-cancel'),
]
