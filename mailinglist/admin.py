from django.contrib import admin

from .models import MailingList, Subscriber


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass
