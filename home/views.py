from django.shortcuts import render, redirect
from sponsor.models import Donation
from .models import Campaign
from django.core.serializers import serialize
from django.contrib.auth.models import User
import json

def home(request):
    top_donation = Donation.objects.all().order_by('-amount')[:4]
    #serial_donation = json.loads(serialize('json', top_donation))
    # print(serial_donation[1]['fields']['name'])
    campaigns = Campaign.objects.all().order_by('campaign_deadline')[:]
    collection_by_campaign = []
    percent_raised = []
    for campaign in campaigns:
        try:
            donation_object = Donation.objects.filter(campaign_id=campaign.campaign_id)
            collection_by_campaign.append(sum(donation_object.amount))
            percent_raised.append(int(collection_by_campaign//campaign.collection_target) * 100)
        except:
            collection_by_campaign.append(100)
            percent_raised.append(int(100*100//campaign.collection_target))

    campaigns_zip = zip(campaigns, collection_by_campaign, percent_raised)
    cnt_usr = len(User.objects.all())
    print(percent_raised)
    return render(request, 'home.html', {'top_donations':top_donation, 'cnt_usr': cnt_usr, 'campaigns_zip': campaigns_zip})

def buddysystem(request):
    return render (request, 'buddy.html')