from django.contrib.auth import get_user_model
from rest_framework import serializers

from mailinglist.models import MailingList

User = get_user_model()


class MailingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailingList
