from django.contrib import admin
from .models import TeamMember, GalleryItem, CharityDetail

# Register your models here.
@admin.register(TeamMember)
class TeamMember(admin.ModelAdmin):
    list_display = ("member_id", "member_name", "member_title", "member_description")
    list_filter = ("member_id", "member_name", )
    search_fields = ("member_name__startswith", "member_title__startswith")

@admin.register(GalleryItem)
class GalleryItem(admin.ModelAdmin):
    list_display = ("item_id", "item_title", )
    list_filter = ("item_id", "item_title", )
    search_fields = ("item_title__startswith",)

@admin.register(CharityDetail)
class CharityDetail(admin.ModelAdmin):
    list_display = ("id", "email", "address", "phone_number", "charity_number" )
