from django.contrib import admin
from .models import Campaign, Affiliation,Opportunity,EmailContent

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("campaign_id", "is_active", "campaign_title", "collection_target", "campaign_deadline")
    list_filter = ("is_active", "campaign_id", "campaign_title", )
    search_fields = ("campaign_title__startswith",)
    prepopulated_fields = {"slug": ("campaign_title",)}

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

@admin.register(EmailContent)
class EmailContentAdmin(admin.ModelAdmin):
    list_display = ("id", "email_type")
    list_filter =  ("id", "email_type")
    # TODO: once the email types are added in the production database uncomment the line below so user can not adapt email type
    # readonly_fields = ("email_type",)