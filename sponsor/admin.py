from django.contrib import admin
from .models import Donation
# Register your models here.

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("trxn_id", "is_successful", "name", "email", "amount", "user_id", 'date_donation')
    list_filter = ("user_id", "email", "is_successful")
    search_fields = ("name__startswith", "email__startswith", "trxn_id__startswith", "amount__startswith",)

    def has_change_permission(self, request, obj = None) -> bool:
        return False
    
    def has_delete_permission(self, request, obj = None) -> bool:
        return False
    
    def has_add_permission(self, request, obj = None) -> bool:
        return False