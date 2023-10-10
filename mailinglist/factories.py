import factory

from accounts.factories import UserFactory

from .models import MailingList


class MailinglistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MailingList

    name = factory.Sequence(lambda n: "Mailinglist %03d" % n)
    owner = factory.SubFactory(UserFactory)
