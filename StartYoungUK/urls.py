"""StartYoungUK URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from home import views as home_views
from verify_email import views as verify_email_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django_otp.admin import OTPAdminSite
from decouple import config
import os


urlpatterns = [
    path("", include("home.urls")),
    path("home/", home_views.home, name="home"),
    path("about/", include("about.urls")),
    path("users/", include("users.urls")),
    path("join-us/", include("contact.urls")),
    path("register", user_views.register, name="register"),
    # path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    # path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path("login/", user_views.captcha_login, name="login"),
    path("logout/", user_views.captcha_logout, name="logout"),
    path(
        str(os.environ("ADMIN_URL")) + "/admin_tools_stats/",
        include("admin_tools_stats.urls"),
    ),
    path(str(os.environ("ADMIN_URL")), admin.site.urls, name="admin"),
    path("donate/", include("sponsor.urls")),
    path("buddy_approvals/", home_views.approve_buddies, name="buddy_approvals"),
    path("letter_tracker/", home_views.letter_tracker, name="letter_tracker"),
    # path('verification/', include('verify_email.urls')),
    path(
        "verification/user/verify-email/<useremail>/<usertoken>/",
        user_views.verify_user_and_activate,
        name="verify-email",
    ),
    path(
        "verification/user/verify-email/request-new-link/<useremail>/<usertoken>/",
        verify_email_views.request_new_link,
        name="request-new-link-from-token",
    ),
    path(
        "verification/user/verify-email/request-new-link/",
        verify_email_views.request_new_link,
        name="request-new-link-from-email",
    ),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "reset_password_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("buddy/", home_views.buddy_system, name="buddy-system"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "StartYoungUK.views.error_404"
handler500 = "StartYoungUK.views.error_500"
# handler403 = 'StartYoungUK.views.error_403'
# handler400 = 'StartYoungUK.views.error_400'

# Enable OTP on login
if os.environ("ENABLE_AUTHENTICATOR", cast=bool):
    admin.site.__class__ = OTPAdminSite
