from django import forms

from .models import MailingList, Message, Subscriber


class MailingListForm(forms.ModelForm):

    class Meta:
        model = MailingList
        fields = ['name', ]


class SubscriberForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        fields = ['email', ]


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['subject', 'body', ]
