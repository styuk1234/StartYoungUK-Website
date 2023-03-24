from django.shortcuts import render, redirect
from sponsor.models import Donation
from .models import Campaign, Affiliation
from users.models import Buddy, Child
from django.core.serializers import serialize
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from .signals import sendBuddyApprovalEmail


# from django.views.generic import ListView
# from django.forms.widgets import CheckboxSelectMultiple
# from django.http import QueryDict

def home(request):
    affiliations = Affiliation.objects.all()
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
    cnt_buddy = len(Buddy.objects.all())
    cnt_child = len(Child.objects.all())
    

    return render(request, 'home.html', {'affiliations':affiliations,'top_donations':serial_donation, 'cnt_usr': cnt_usr, 'campaigns_zip': campaigns_zip, 'cnt_buddy': cnt_buddy, 'cnt_child': cnt_child})

def buddy_system(request):
    return render(request, 'buddy.html')

@login_required
@user_passes_test(lambda u: u.startyoungukuser.is_coordinator)
def approve_buddies(request):
    buddies = Buddy.objects.all().order_by('date_status_modified')
    current_user = request.user
    if request.method == 'POST':
        filter_status = request.POST.get('filter-status')
        if filter_status is None or filter_status == "all":
            buddies = Buddy.objects.all().order_by('date_status_modified')
        else:
            buddies = Buddy.objects.filter(status=filter_status).order_by('date_status_modified')
        Buddy_status = request.POST.get('Buddy-status')
        checked_buddies = request.POST.getlist('chosen-buddies')
        filter_status = request.POST.get('filter-status')
        for Buddy_id in checked_buddies:
            updated_buddies = Buddy.objects.filter(pk=int(Buddy_id))
            updated_buddies.update(status=Buddy_status,approver=current_user.email)
            # TODO: send email update to buddy once they're accepted/rejected as Buddy. The current email settings need to be changed for below code to work.
            # for updated_Buddy in updated_buddies:
            #     sendBuddyApprovalEmail(updated_Buddy.user.email, Buddy_status)
        return render(request, 'buddy_approvals.html',{'buddies':buddies, 'filter_status':filter_status})
    return render(request, 'buddy_approvals.html',{'buddies':buddies})

    