from django.contrib import admin
from .models import TeamMember, GalleryImage

# Register your models here.
@admin.register(TeamMember)
class TeamMember(admin.ModelAdmin):
    list_display = ("member_id", "member_name", "member_title", "member_description")
    list_filter = ("member_id", "member_name", )
    search_fields = ("member_name__startswith",)

@admin.register(GalleryImage)
class GalleryImage(admin.ModelAdmin):
    list_display = ("image_id", "image_title", )
    list_filter = ("image_id", "image_title", )
    search_fields = ("image_title__startswith",)