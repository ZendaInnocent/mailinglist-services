import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from mailinglist import tasks

User = get_user_model()


class MailingList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('mailinglist:mailinglist-detail', kwargs={'pk': self.id})


class SubscriberManager(models.Manager):
    def confirmed_subscribers_for_mailinglist(self, mailing_list):
        qs = self.get_queryset()
        return qs.filter(confirmed=True, mailing_list=mailing_list)


class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    confirmed = models.BooleanField(default=False)
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)

    objects = SubscriberManager()

    def __str__(self):
        return self.email

    class Meta:
        unique_together = ['email', 'mailing_list']


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    subject = models.CharField(max_length=140)
    body = models.TextField()
    started = models.DateTimeField(default=None, null=True)
    finished = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('mailinglist:message-detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if self._state.adding:
            tasks.build_subscriber_messages_for_message.delay(self.id)
        return super().save(*args, **kwargs)


class SubscriberMessageManager(models.Manager):
    def create_from_message(self, message):
        confirmed_subs = Subscriber.objects.confirmed_subscribers_for_mailinglist(
            message.mailing_list
        )
        return [
            self.create(message=message, subscriber=subscriber)
            for subscriber in confirmed_subs
        ]


class SubscriberMessage(models.Model):
    """A model to track whether email is successful sent
    to a `Subscriber` model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True, default=None)
    last_attempt = models.DateTimeField(null=True, default=None)

    objects = SubscriberMessageManager()

    def send(self):
        tasks.send_subscriber_message.delay(self.id)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.send()
        return super().save(*args, **kwargs)
