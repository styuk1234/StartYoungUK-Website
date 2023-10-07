from django.contrib import admin
from .models import TeamMember, GalleryItem, CharityDetail


# Register your models here.
@admin.register(TeamMember)
class TeamMember(admin.ModelAdmin):
    list_display = ("member_id", "member_name", "member_title")
    list_filter = (
        "member_id",
        "member_name",
    )
    search_fields = ("member_name__startswith", "member_title__startswith")


@admin.register(GalleryItem)
class GalleryItem(admin.ModelAdmin):
    list_display = (
        "item_id",
        "item_title",
    )
    list_filter = (
        "item_id",
        "item_title",
    )
    search_fields = ("item_title__startswith",)


@admin.register(CharityDetail)
class CharityDetail(admin.ModelAdmin):
    list_display = ("id", "email", "address", "phone_number", "charity_number","number_children_helped", "buddies_onboarded","number_of_sponsors"," campaigns_so_far")
    
    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return False
