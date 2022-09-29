from django.contrib import admin
from users.models import StartYoungUKUser, Mentor, Child

# Register your models here.

@admin.register(StartYoungUKUser)
class StartYoungUKUserAdmin(admin.ModelAdmin):
    admin.site.site_header = 'StartYoungUK Administration'
    admin.site.site_title = ' '
    admin.site.index_title = ' '

    list_display = ("email", "display_name", "user_type", "is_verified", "phone_number")
    list_filter = ("is_verified", "user_type", )
    search_fields = ("display_name__startswith", "email__startswith", )

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    pass

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    pass