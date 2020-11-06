from django.contrib import admin

from .models import MailingList, Message, Subscriber, SubscriberMessage

admin.site.site_title = 'MailApe Admin'
admin.site.site_header = 'MailApe Admin'


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'mailing_list', 'confirmed', )


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'mailing_list', )


@admin.register(SubscriberMessage)
class SubscriberMessageAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'message', 'created',
                    'last_attempt', 'sent', )
