import logging

from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from accounts.forms import UserCreationForm
from accounts.models import User

logger = logging.getLogger(__name__)


def test_user_registration_view_works(client):
    response = client.get(reverse('accounts:signup'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'registration/signup.html')
    assert isinstance(response.context['form'], UserCreationForm)


def test_user_registration_view_submission_works(client):
    data = {
        'email': 'someone@domain.com',
        'name': 'Someone There',
        'password1': 'ofsdoadsfoisadfh9',
        'password2': 'ofsdoadsfoisadfh9',
    }

    response = client.post(reverse('accounts:signup'), data)

    assert response.status_code == 302
    assertRedirects(response, '/accounts/pending-registration/')
    assert User.objects.filter(email='someone@domain.com').exists()
