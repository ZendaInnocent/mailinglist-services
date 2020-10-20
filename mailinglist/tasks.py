from celery import shared_task

from mailinglist import emails


@shared_task
def send_confirmation_email_to_subscriber(subscriber_id):
    from mailinglist.models import Subscriber
    subscriber = Subscriber.objects.get(id=subscriber_id)
    emails.send_confirmation_email(subscriber)
