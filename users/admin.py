from django.contrib import admin
from .models import StartYoungUKUser, Buddy
from verify_email.models import LinkCounter
import verify_email.admin
from import_export.admin import ExportActionMixin



# Register your models here.

admin.site.unregister(LinkCounter)

@admin.register(LinkCounter)
class LinkCounterAdmin(ExportActionMixin, admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None) -> bool:
        return True

    def has_add_permission(self, request, obj=None) -> bool:
        return False

@admin.register(StartYoungUKUser)
class StartYoungUKUserAdmin(ExportActionMixin, admin.ModelAdmin):
    admin.site.site_header = "Start Young UK Administration"
    admin.site.site_title = "Start Young UK Admin Site"
    admin.site.index_title = "Start Young UK Management"

    list_display = ("email", "name", "user_type", "is_verified", "phone_number")
    list_filter = (
        "is_verified",
        "user_type",
    )
    search_fields = (
        "user__first_name__startswith",
        "user__last_name__startswith",
        "email__startswith",
    )
    readonly_fields = [
        "sdp_amount",
        "sdp_frequency",
        "is_buddy",
        "image",
        "is_verified",
        "user_type",
        "crn_no",
        "phone_number",
        "address",
        "user",
        "email",
    ]

    def has_delete_permission(self, request, obj=None) -> bool:
        return True

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name


# @admin.register(Child)
# class ChildAdmin(admin.ModelAdmin):
#     pass


@admin.register(Buddy)
class BuddyAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("id", "user", "status")
    list_filter = ("status",)
    # search_fields = ("display_name__startswith", "email__startswith", )
