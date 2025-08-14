from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import tasks

User = get_user_model()


@receiver(post_save, sender=User)
def send_registration_confirmation_mail(sender, instance, created, **kwargs):
    if created:
        tasks.send_registration_confirmation_mail.delay(instance.id)
