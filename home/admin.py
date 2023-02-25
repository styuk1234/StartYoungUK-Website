from django.contrib import admin
from .models import Campaign, Affiliation,Opportunity

# Register your models here.

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("campaign_id", "campaign_title", "collection_target", "campaign_deadline")
    list_filter = ("campaign_id", "campaign_title", )
    search_fields = ("campaign_title__startswith",)

admin.site.register(Affiliation)
# class CampaignAdmin(admin.ModelAdmin):
#     list_display = ("campaign_id", "campaign_title", "collection_target", "campaign_deadline")
#     list_filter = ("campaign_id", "campaign_title", )
#     search_fields = ("campaign_title__startswith",)python3 manage.py migrate
    
@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "form_url")
    list_filter = ("id", "title", )
    search_fields = ("title__startswith",)
