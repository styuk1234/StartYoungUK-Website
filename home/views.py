from django.shortcuts import render, redirect
from sponsor.models import Donation
from .models import Campaign, Affiliation
from users.models import Mentor, Child
from django.core.serializers import serialize
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from .signals import sendMentorApprovalEmail


from django.views.generic import ListView
from django.forms.widgets import CheckboxSelectMultiple
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
    cnt_buddy = len(Mentor.objects.all())
    cnt_child = len(Child.objects.all())
    

    return render(request, 'home.html', {'affiliations':affiliations,'top_donations':serial_donation, 'cnt_usr': cnt_usr, 'campaigns_zip': campaigns_zip, 'cnt_buddy': cnt_buddy, 'cnt_child': cnt_child})

def buddysystem(request):
    return render(request, 'buddy.html')

@login_required
@user_passes_test(lambda u: u.startyoungukuser.is_coordinator)
def approve_mentors(request):
    mentors = Mentor.objects.all()
    current_user = request.user
    if request.method == 'POST':
        mentor_status = request.POST.get('mentor-status')
        checked_mentors = request.POST.getlist('chosen-mentors')
        for mentor_id in checked_mentors:
            updated_mentors = Mentor.objects.filter(pk=int(mentor_id))
            updated_mentors.update(status=mentor_status,approver=current_user.email)
            # TODO: send email update to buddy once they're accepted/rejected as mentor. The current email settings need to be changed for below code to work.
            # for updated_mentor in updated_mentors:
            #     sendMentorApprovalEmail(updated_mentor.user.email, mentor_status)
        return render(request, 'mentor_approvals.html',{'mentors':mentors})
    return render(request, 'mentor_approvals.html',{'mentors':mentors})

    