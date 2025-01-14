from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Friendss

@receiver(post_save, sender=User)
def create_friendss_instance(sender, instance, created, **kwargs):
    if created:
        Friendss.objects.create(user=instance)
