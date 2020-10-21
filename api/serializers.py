from django.contrib.auth import get_user_model
from rest_framework import serializers

from mailinglist.models import MailingList, Subscriber

User = get_user_model()


class MailingListSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = MailingList
        fields = ('url', 'id', 'name', 'subscriber_set', )
        read_only_fields = ('subscriber_set', )
        extra_kwargs = {
            'url': {'view_name': 'api:api-mailinglist-detail'},
            'subscriber_set': {'view_name': 'api:api-subscriber-detail'},
        }


class SubscriberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subscriber
        fields = ('url', 'id', 'email', 'confirmed', 'mailing_list', )
        extra_kwargs = {
            'url': {'view_name': 'api:api-subscriber-detail'},
            'mailing_list': {'view_name': 'api:api-mailinglist-detail'},
        }


class ReadOnlySubscriberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subscriber
        fields = ('url', 'id', 'email', 'confirmed', 'mailing_list', )
        read_only_fields = ('email', 'mailing_list', )
        extra_kwargs = {
            'url': {'view_name': 'api:api-subscriber-detail'},
            'mailing_list': {'view_name': 'api:api-mailinglist-detail'},
        }
