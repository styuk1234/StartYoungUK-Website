from django.shortcuts import render, redirect
from sponsor.models import Donation
from .models import Campaign
from users.models import Mentor, Child
from django.core.serializers import serialize
from django.contrib.auth.models import User
import json

def home(request):
    top_donation = Donation.objects.all().order_by('-amount')[:4]
    serial_donation = json.loads(serialize('json', top_donation))
    # print(serial_donation[1]['fields']['name'])
    campaigns = Campaign.objects.all().order_by('campaign_deadline')[:]
    collection_by_campaign = []
    percent_raised = []
    for campaign in campaigns:
        try:
            donation_object = Donation.objects.filter(campaign_id=campaign.campaign_id)
            total_amount = sum([donation['amount'] for donation in donation_object.values()])
            collection_by_campaign.append(total_amount)
            percent = int(total_amount/campaign.collection_target * 100)
            percent_raised.append(percent)
        except:
            default_amount = 0
            collection_by_campaign.append(default_amount)
            percent = int(default_amount/campaign.collection_target * 100)
            percent_raised.append(percent)
            
    campaigns_zip = zip(campaigns, collection_by_campaign, percent_raised)
    cnt_usr = len(User.objects.all())
    cnt_buddy = len(Mentor.objects.all())
    cnt_child = len(Child.objects.all())

    return render(request, 'home.html', {'top_donations':serial_donation, 'cnt_usr': cnt_usr, 'campaigns_zip': campaigns_zip, 'cnt_buddy': cnt_buddy, 'cnt_child': cnt_child})

def buddysystem(request):
    return render (request, 'buddy.html')