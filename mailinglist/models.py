import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from mailinglist import tasks

User = get_user_model()


class MailingList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
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

    class Meta:
        unique_together = ['email', 'mailing_list']

    def send_confirmation_email(self):
        return tasks.send_confirmation_email_to_subscriber.delay(self.id)

    def save(self, *args, **kwargs):
        # send confirmation email to new Subscriber
        if self._state.adding:
            self.send_confirmation_email()
        return super().save(*args, **kwargs)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    subject = models.CharField(max_length=140)
    body = models.TextField()
    started = models.DateTimeField(default=None, null=True)
    finished = models.DateTimeField(default=None, null=True)

    def get_absolute_url(self):
        return reverse('mailinglist:message-detail', kwargs={'pk': self.id})
