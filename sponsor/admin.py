from django.contrib import admin
from .models import Donation
# Register your models here.

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("trxn_id", "name", "email_id", "amount", "user_id")
    list_filter = ("user_id", "email_id", )
    search_fields = ("name__startswith", "email__startswith", "trxn_id__startswith", "amount__startswith",)