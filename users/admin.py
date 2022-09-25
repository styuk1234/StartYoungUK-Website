from django.contrib import admin
from users.models import StartYoungUKUser

# Register your models here.
#admin.site.register(StartYoungUKUser)

@admin.register(StartYoungUKUser)
class StartYoungUKUserAdmin(admin.ModelAdmin):
    list_display = ("email", "display_name", "user_type", "is_verified", "phone_number")
    list_filter = ("is_verified", "user_type", )
    search_fields = ("display_name__startswith", "email__startswith", )