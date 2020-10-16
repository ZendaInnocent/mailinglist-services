from django import forms

from .models import MailingList, Subscriber


class SubscriberForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        fields = ['mailing_list', 'email', ]
