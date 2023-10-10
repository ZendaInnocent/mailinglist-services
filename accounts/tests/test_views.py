import logging

from django.test import TestCase
from django.urls import reverse

from accounts.forms import UserCreationForm
from accounts.models import User

logger = logging.getLogger(__name__)


class AccountsAppViewsTest(TestCase):
    def test_user_registration_view_works(self):
        response = self.client.get(reverse('accounts:signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_user_registration_view_submission_works(self):
        data = {
            'email': 'someone@domain.com',
            'name': 'Someone There',
            'password1': 'ofsdoadsfoisadfh9',
            'password2': 'ofsdoadsfoisadfh9',
        }

        response = self.client.post(reverse('accounts:signup'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertTrue(User.objects.filter(email='someone@domain.com').exists())
