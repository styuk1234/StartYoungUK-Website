from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import StartYoungUKUser


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.is_superuser:

        syuk_user = StartYoungUKUser()
        if not StartYoungUKUser.objects.filter(email=instance.email).exists():
            syuk_user.user = User.objects.get(email=instance.email)
            syuk_user.display_name = instance.username
            syuk_user.phone_number = "+447946369885"
            syuk_user.email = instance.email
            syuk_user.address = "Newham, UK"
            syuk_user.user_type = "I"
            # syuk_user.crn_no = instance.crn_no
            syuk_user.is_verified=True
            syuk_user.save()