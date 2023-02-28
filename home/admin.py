from django.contrib import admin
from .models import Campaign, Affiliation,Opportunity

# Register your models here.

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("campaign_id", "campaign_title", "collection_target", "campaign_deadline")
    list_filter = ("campaign_id", "campaign_title", )
    search_fields = ("campaign_title__startswith",)

@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = ("affiliation_id", "affiliation_name", "affiliation_join_date")
    list_filter = ("affiliation_id", "affiliation_name", )
    search_fields = ("affiliation_name__startswith",)
    
@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "form_url")
    list_filter = ("id", "title", )
    search_fields = ("title__startswith",)
