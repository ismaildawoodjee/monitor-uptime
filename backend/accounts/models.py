from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    """
    User is Django's default model, UserProfile has a 1-to-1 mapping to it.
    Each User has one UserProfile.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # other custom fields for user - subscription plan and subscription ID
    # `default` is the default value for the field
    # if `blank`, the field is allowed to have an empty string
    plan = models.CharField(max_length=255, default="free", blank=True)
    subscription_id = models.CharField(max_length=255, blank=True)


# post_save signals are sent after a User object calls the `save()` method, i.e.
# when a User is created and saved into the database, the methods below are called
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates `UserProfile` for new users."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Updates `UserProfile`"""
    instance.profile.save()
