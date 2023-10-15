from django.db.models.signals import post_save
from django.dispatch import receiver

from . import tasks
from .models import Message, Subscriber, SubscriberMessage


@receiver(post_save, sender=Subscriber)
def send_confirmation_mail(sender, created, instance, **kwargs):
    if created:
        tasks.send_confirmation_email_to_subscriber.delay(instance.id)


@receiver(post_save, sender=Message)
def build_subscriber_messages_for_message(sender, created, instance, **kwargs):
    if created:
        tasks.build_subscriber_messages_for_message.delay(instance.id)


@receiver(post_save, sender=SubscriberMessage)
def send_message_to_subscribers(sender, created, instance, **kwargs):
    if created:
        tasks.send_subscriber_message.delay(instance.id)
