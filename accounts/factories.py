import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    name = factory.Faker('name')
    email = factory.LazyAttribute(lambda o: '%s@gmail.com' % o.name)
