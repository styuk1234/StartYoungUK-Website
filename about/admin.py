from django.contrib import admin
from .models import TeamMember

# Register your models here.
@admin.register(TeamMember)
class TeamMember(admin.ModelAdmin):
    list_display = ("member_id", "member_name", "member_title", "member_description")
    list_filter = ("member_id", "member_name", )
    search_fields = ("member_name__startswith",)
