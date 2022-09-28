from django.contrib import admin
from .models import Campaign

# Register your models here.

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("campaign_id", "campaign_title", "collection_target", "campaign_deadline")
    list_filter = ("campaign_id", "campaign_title", )
    search_fields = ("campaign_title__startswith",)