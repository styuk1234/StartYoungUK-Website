from django.contrib import admin
from .models import Campaign, Affiliation, Opportunity, EmailContent
from import_export.admin import ExportActionMixin

@admin.register(Campaign)
class CampaignAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "campaign_id",
        "is_active",
        "campaign_title",
        "collection_target",
        "campaign_deadline",
    )
    list_filter = (
        "is_active",
        "campaign_id",
        "campaign_title",
    )
    search_fields = ("campaign_title__startswith",)
    prepopulated_fields = {"slug": ("campaign_title",)}


@admin.register(Affiliation)
class AffiliationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("affiliation_id", "affiliation_name", "affiliation_join_date")
    list_filter = (
        "affiliation_id",
        "affiliation_name",
    )
    search_fields = ("affiliation_name__startswith",)


@admin.register(Opportunity)
class OpportunityAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("id", "title", "description", "form_url")
    list_filter = (
        "id",
        "title",
    )
    search_fields = ("title__startswith",)


@admin.register(EmailContent)
class EmailContentAdmin(admin.ModelAdmin):
    list_display = ("id", "email_type")
    list_filter = ("id", "email_type")
    readonly_fields = ("email_type",)
    
    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return False
