from django import forms
from datetime import datetime
from home.models import Campaign


class CampaignForm(forms.ModelForm):
    campaign_title = forms.CharField(required=True)
    campaign_description = forms.TextField(required=True)
    collection_target = forms.IntegerField(required=True)
    campaign_deadline = forms.DateField(required=True, default=datetime.date.today)
    campaign_image = forms.ImageField(required=True)
    
    class Meta:
        model = Campaign
        fields = ['campaign_title', 'campaign_description','campaign_description','collection_target', 'campaign_deadline', 'campaign_image']