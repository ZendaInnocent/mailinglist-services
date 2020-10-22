from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from mailinglist.models import MailingList, Subscriber

from .serializers import (MailingListSerializer,
                          ReadOnlySubscriberSerializer, SubscriberSerializer)


class MailingListCreateListView(generics.ListCreateAPIView):
    serializer_class = MailingListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        # return the mailing lists owned by a loged in user.
        return self.request.user.mailinglist_set.all()

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data', None):
            data = kwargs.get('data', None)
            owner = {
                'owner': self.request.user.id
            }
            data.update(owner)
        return super().get_serializer(*args, **kwargs)


class MailingListRetrieveUpdateDestroyView(
        generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = MailingListSerializer

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)


class SubscriberListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = SubscriberSerializer

    def get_queryset(self):
        # return subscribers for a particular mailing list
        mailinglist_pk = self.kwargs['mailinglist_pk']
        mailinglist = get_object_or_404(MailingList, id=mailinglist_pk)
        return mailinglist.subscriber_set.all()

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data'):
            data = kwargs.get('data')
            mailinglist = {
                'mailinglist':
                    reverse('api:api-mailinglist-detail',
                            kwargs={'pk': self.kwargs['mailinglist_pk']})
            }
            data.update(mailinglist)
        return super().get_serializer(*args, **kwargs)


class SubscriberRetrieveUpdateDestroyView(
        generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = ReadOnlySubscriberSerializer

    def get_queryset(self):
        return Subscriber.objects.all()
