from django.contrib import admin
from django.http.request import HttpRequest
from .models import Donation
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.admin import PayPalIPNAdmin
from import_export.admin import ExportActionMixin

# Register your models here.

admin.site.unregister(PayPalIPN)

@admin.register(PayPalIPN)
class PayPalIPNAdmin(PayPalIPNAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Donation)
class DonationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "trxn_id",
        "is_successful",
        "user_id",
        "name",
        "email",
        "amount",
        "date_donation",
    )
    list_filter = ("is_successful",)
    search_fields = (
        "name__startswith",
        "email__startswith",
        "trxn_id__startswith",
        "amount__startswith",
    )

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return False
