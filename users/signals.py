from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.contrib.auth.models import User


# This will prevent recursion when updating the user profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update the profile for the user."""
    # Avoid infinite loop by checking if the user is already related to a profile
    if created:
        User.objects.create(user=instance)
    # This ensures that the profile is saved when the user is updated
    if not hasattr(instance, "profile"):
        instance.profile.save()
