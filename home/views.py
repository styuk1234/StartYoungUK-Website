from django.shortcuts import render, redirect
import StartYoungUK
from sponsor.models import Donation
from sponsor.forms import DonationForm
from django.urls import reverse
from dotenv import load_dotenv
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Campaign, Affiliation, EmailContent
from users.models import Buddy, StartYoungUKUser
from django.core.serializers import serialize
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from .signals import sendEmail
import os

load_dotenv()
# from django.views.generic import ListView
# from django.forms.widgets import CheckboxSelectMultiple
# from django.http import QueryDict


def home(request):
    affiliations = Affiliation.objects.all()
    top_donation = Donation.objects.filter(is_successful=True).order_by("-amount")[:4]
    serial_donation = json.loads(serialize("json", top_donation))
    donor_images = []
    for donation in top_donation:
        try:
            donor_images.append(
                StartYoungUKUser.objects.get(id=donation.user_id).image.url
            )
        except StartYoungUKUser.DoesNotExist:
            donor_images.append("Unauthenticated donation")

    campaigns = Campaign.objects.all().order_by("campaign_deadline")[:]
    collection_by_campaign = []
    percent_raised = []
    for campaign in campaigns:
        try:
            donation_object = Donation.objects.filter(campaign_id=campaign.campaign_id)
            total_amount = sum(
                [
                    donation["amount"]
                    for donation in donation_object.values()
                    if donation["is_successful"]
                ]
            )
            collection_by_campaign.append(total_amount)
            percent = int(total_amount / campaign.collection_target * 100)
            percent_raised.append(percent)
        except:
            default_amount = 0
            collection_by_campaign.append(default_amount)
            percent = int(default_amount / campaign.collection_target * 100)
            percent_raised.append(percent)

    campaigns_zip = zip(campaigns, collection_by_campaign, percent_raised)
    cnt_usr = len(User.objects.all())
    cnt_buddy = len(Buddy.objects.all())
    cnt_campaigns = len(campaigns)
    donations_zip = zip(serial_donation, donor_images)

    return render(
        request,
        "home.html",
        {
            "affiliations": affiliations,
            "top_donations": donations_zip,
            "cnt_usr": cnt_usr,
            "campaigns_zip": campaigns_zip,
            "cnt_buddy": cnt_buddy,
            "cnt_campaigns": cnt_campaigns,
        },
    )


def buddy_system(request):
    return render(request, "buddy.html")


@login_required
@user_passes_test(lambda u: u.startyoungukuser.is_coordinator)
def approve_buddies(request):
    buddies = Buddy.objects.all().order_by("date_status_modified")
    current_user = request.user
    if request.method == "POST":
        buddy_status = request.POST.get("buddy-status")
        checked_buddies = request.POST.getlist("chosen-buddies")

        for buddy_id in checked_buddies:
            buddy = Buddy.objects.get(id=buddy_id)
            if buddy.status != buddy_status:
                buddy.status = buddy_status
                buddy.approver = current_user.email
                buddy.save()
                buddy_user = StartYoungUKUser.objects.get(user=buddy.user)
                if buddy.status == "approved":
                    buddy_user.is_buddy = True
                    buddy_user.save()
                else:
                    buddy_user.is_buddy = False
                    buddy_user.save()
                if (
                    buddy.user.startyoungukuser.sdp_frequency != "N"
                    and buddy_status == "approved"
                ):
                    sendEmail(buddy.user.email, "final")
                else:
                    sendEmail(buddy.user.email, buddy_status)
        return render(
            request,
            "buddy_approvals.html",
            {
                "buddies": buddies,
            },
        )
    return render(request, "buddy_approvals.html", {"buddies": buddies})


@login_required
@user_passes_test(lambda u: u.startyoungukuser.is_coordinator)
def letter_tracker(request):
    buddies = (
        Buddy.objects.filter(status="approved")
        .select_related("user__startyoungukuser")
        .exclude(user__startyoungukuser__sdp_frequency__exact="N")
        .order_by("letter_received")
    )

    if request.method == "POST":
        # three bottom buttons functions
        checked_buddies = request.POST.getlist("chosen-buddies")
        if "send-email" in request.POST:
            for buddy_id in checked_buddies:
                buddy = Buddy.objects.get(id=buddy_id)
                # only send letter to buddy with false letter received
                if buddy.letter_received == False:
                    sendEmail(buddy.user.email, "Letter")
            return redirect("letter_tracker")
        # update letter received to true
        elif "letter-received-true" in request.POST:
            for buddy_id in checked_buddies:
                buddy = Buddy.objects.get(id=buddy_id)
                buddy.letter_received = True
                buddy.save()
            return redirect("letter_tracker")
        # update letter received to false
        elif "letter-received-false" in request.POST:
            for buddy_id in checked_buddies:
                buddy = Buddy.objects.get(id=buddy_id)
                buddy.letter_received = False
                buddy.save()
            return redirect("letter_tracker")

        return render(
            request,
            "letter_tracker.html",
            {"buddies": buddies},
        )

    return render(request, "letter_tracker.html", {"buddies": buddies})


def campaign_donate(request, slug):
    campaign_name = get_object_or_404(
        Campaign, slug=slug, is_active=True
    ).campaign_title
    campaign_id: int = get_object_or_404(
        Campaign, slug=slug, is_active=True
    ).campaign_id

    if request.method == "POST":
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
            messages.error(request, 'Please submit a Captcha before you click "Donate"')

        elif form.is_valid():
            data = form.save()
            form_data = DonationForm(instance=data)

            # Update the donation object with current campaign's id
            donation = Donation.objects.get(trxn_id=data.trxn_id)
            donation.campaign_id = campaign_id
            donation.user_id = request.user.id if request.user.is_authenticated else 0
            donation.save()

            # Update PayPal data with donation amount and invoce number
            paypal_dict["amount"] = data.amount
            paypal_dict["invoice"] = data.trxn_id
            paypal_btn = PayPalPaymentsForm(initial=paypal_dict)
            messages.success(
                request, "Please find the Paypal button below to complete the Donation!"
            )

            return render(
                request,
                "campaign_donate.html",
                {
                    "paypal_btn": paypal_btn,
                    "form": form_data,
                    "button_enable": True,
                    "campaign_name": campaign_name,
                },
            )

        else:
            messages.error(
                request, "There was an error with your donation. Please try again!"
            )

    # Pre-populate user info if user is authenticated
    if request.user.is_authenticated:
        donate = Donation()
        donate.user_id = request.user.startyoungukuser.user_id
        donate.name = request.user.first_name + " " + request.user.last_name
        donate.email = request.user.startyoungukuser.email
        donate.mobile_number = request.user.startyoungukuser.phone_number
        form = DonationForm(instance=donate)
    else:
        form = DonationForm()

    return render(
        request, "campaign_donate.html", {"form": form, "campaign_name": campaign_name}
    )
