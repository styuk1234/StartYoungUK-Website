from django import forms
from home.models import Campaigns


class CampaignsForm(forms.ModelForm):
    campaign_title = forms.CharField(required=True)
    campaign_description = forms.TextField(required=True)
    collection_target = forms.IntegerField(required=True)
    campaign_image = forms.ImageField(required=True)
    
    class Meta:
        model = Campaigns
        fields = ['campaign_title', 'campaign_description','campaign_description','collection_target', 'campaign_image']