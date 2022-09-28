from django.shortcuts import render, redirect
from sponsor.models import Donation
from .models import Campaign
from django.core.serializers import serialize
from django.contrib.auth.models import User
import json
from django.db.models import Sum

def home(request):
    top_donation = Donation.objects.all().order_by('-amount')[:4]
    serial_donation = json.loads(serialize('json', top_donation))
    # print(serial_donation[1]['fields']['name'])
    campaigns = Campaign.objects.all().order_by('campaign_deadline')[:]
    collection_by_campaign = []
    for campaign in campaigns:
        try:
            donation_object = Donation.objects.filter(campaign_id=campaign.campaign_id)
            collection_by_campaign.append(sum(donation_object.amount))
            #print(Donation.objects.filter(campaign_id=campaign.campaign_id))
            print(collection_by_campaign)
        except:
            collection_by_campaign.append(10)
            print(collection_by_campaign)
    campaigns_zip = zip(campaigns, collection_by_campaign)
    cnt_usr = len(User.objects.all())
    return render(request, 'home.html', {'top_donations':serial_donation, 'cnt_usr': cnt_usr, 'campaigns_zip': campaigns_zip})

def buddysystem(request):
    return render (request, 'buddy.html')