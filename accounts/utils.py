from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User
from .tokens import account_activation_token


def send_registration_confirmation_mail(email):
    user = User.objects.get(email=email)
    token = account_activation_token.make_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user.id))
    url = 'http://localhost:8000' + reverse_lazy(
        'accounts:confirm-email', kwargs={'user_id': user_id, 'token': token}
    )
    message = get_template('registration/account_activation_email.html').render(
        {'confirm_url': url}
    )
    mail = EmailMessage(
        'Account Confirmation',
        message,
        to=[user.email],
        from_email='noreply@domain.com',
    )
    mail.content_subtype = 'html'
    mail.send()
