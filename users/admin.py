from django.contrib import admin
from .models import StartYoungUKUser, Buddy, Child


# Register your models here.

@admin.register(StartYoungUKUser)
class StartYoungUKUserAdmin(admin.ModelAdmin):
    admin.site.site_header = 'StartYoung UK Administration'
    admin.site.site_title = 'StartYoung UK Admin Site '
    admin.site.index_title = 'StartYoung UK Management'

    list_display = ("email", "display_name", "user_type", "is_verified", "phone_number")
    list_filter = ("is_verified", "user_type", )
    search_fields = ("display_name__startswith", "email__startswith", )

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    pass

@admin.register(Buddy)
class BuddyAdmin(admin.ModelAdmin):
    list_display = ("id", "user",  "status")
    list_filter = ("status", )
    # search_fields = ("display_name__startswith", "email__startswith", )
