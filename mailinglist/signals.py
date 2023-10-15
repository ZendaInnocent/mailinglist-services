from django.db.models.signals import post_save
from django.dispatch import receiver

from . import emails
from .models import Subscriber


@receiver(post_save, sender=Subscriber)
def send_confirmation_mail(sender, created, instance, **kwargs):
    if created:
        emails.send_confirmation_email(instance.id)
