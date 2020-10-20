from django.contrib import admin

from .models import MailingList, Message, Subscriber


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'mailing_list', 'confirmed', )


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'mailing_list', )
