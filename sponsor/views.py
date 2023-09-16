from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from dotenv import load_dotenv
from paypal.standard.forms import PayPalPaymentsForm
from .forms import DonationForm
from django.contrib import messages
from .models import Donation
import os
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse

def sponsor(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == "donate_in_kind":
            # Send an email with the donation in kind information
            name = request.POST.get('Name')
            email = request.POST.get('Email')
            comment = request.POST.get('Comment')
            email_body = f"Name: {name}\nEmail: {email}\nMessage: {comment}"
            try:
                # Send the email
                send_mail(
                    f"New Donate In Kind Submission from: {name}",
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    ['codefest.youngcoders@gmail.com'],
                    fail_silently=False,
                )

                response_data = {'message': 'Message sent successfully!', 'status': 200}
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {'message': e, 'status': 500}
                return JsonResponse(response_data)
        else:
            form = DonationForm(request.POST)
            # Paypal Button instance
            paypal_dict = {
                "business": os.getenv("PAYPAL_BUSINESS_ACCOUNT"),
                "currency_code": "GBP",
                "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
                "return": request.build_absolute_uri(reverse("paypal-return")),
                "cancel_return": request.build_absolute_uri(reverse("paypal-cancel")),
            }

            if not request.user.is_authenticated and int(form["amount"].value()) > 40:
                messages.error(
                    request,
                    "We are not able to accept donations of more than £40 from unathenticated users. Please sign in to donate a larger amount!",
                )

            elif form.has_error("captcha"):
                messages.error(
                    request, 'Please solve the Captcha before you click "Donate"'
                )

            elif form.is_valid():
                donation = form.save(commit=False)
                donation.user_id = request.user.id if request.user.is_authenticated else 0
                form_data = DonationForm(instance=donation)

                paypal_dict["amount"] = donation.amount
                paypal_dict["invoice"] = donation.trxn_id
                paypal_btn = PayPalPaymentsForm(initial=paypal_dict)
                button_enable = True
                messages.success(
                    request, "Please find the PayPal button below to complete the Donation!"
                )
                donation.save()
                return render(
                    request,
                    "sponsor.html",
                    {
                        "paypal_btn": paypal_btn,
                        "form": form_data,
                        "button_enable": button_enable,
                    },
                )

            else:
                messages.error(
                    request, "There was an error with your donation. Please try again!"
                )

    # Pre-populate user info if user is authenticated
    if request.user.is_authenticated:
        donate = Donation()
        donate.campaign_id = 0
        donate.user_id = request.user.startyoungukuser.user_id
        donate.name = request.user.first_name + " " + request.user.last_name
        donate.email = request.user.startyoungukuser.email
        donate.address = request.user.startyoungukuser.address
        donate.mobile_number = request.user.startyoungukuser.phone_number
        form = DonationForm(instance=donate)
    else:
        form = DonationForm()

    return render(request, "sponsor.html", {"form": form, "GSHEETS_DONATE_IN_KIND": settings.GSHEETS_DONATE_IN_KIND})


class PaypalReturnView(TemplateView):
    template_name = "paypal_success.html"


class PaypalCancelView(TemplateView):
    template_name = "paypal_cancel.html"
