from django.contrib import admin

from .models import MailingList, Message, Subscriber


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    pass
