from django.contrib import admin

from .models import MailingList


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    pass
