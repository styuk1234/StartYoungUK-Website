from django import forms
from datetime import datetime
from home.models import Campaign
from PIL import Image


class CampaignForm(forms.ModelForm):
    campaign_title = forms.CharField(required=True)
    campaign_description = forms.CharField(
        widget=forms.Textarea(),
        required=True)
    collection_target = forms.IntegerField(required=True)
    campaign_deadline = forms.DateField(required=True, help_text="Enter date in YYYY-MM-DD format")
    campaign_image = forms.ImageField(required=False)
    
    class Meta:
        model = Campaign
        fields = ['campaign_title','campaign_description','collection_target', 'campaign_deadline', 'campaign_image']