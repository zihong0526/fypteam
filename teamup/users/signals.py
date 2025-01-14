from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.db import IntegrityError

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            profile = Profile.objects.create(user=instance)
        except IntegrityError:
            # Profile for this user already exists
            pass

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # If the profile doesn't exist, create it
        Profile.objects.create(user=instance)