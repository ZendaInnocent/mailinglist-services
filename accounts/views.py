from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, TemplateView

from accounts import forms

from .tokens import account_activation_token

User = get_user_model()


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = forms.UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:pending-registration')
    success_message = (
        'A confirmation email has been sent to your email'
        '. Please confirm to finish registration.'
    )

    def form_valid(self, form):
        form.save()
        user = User.objects.get(email=form.instance)
        # send confirmation email
        token = account_activation_token.make_token(user)
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        url = 'http://localhost:8000' + reverse(
            'accounts:confirm-email', kwargs={'user_id': user_id, 'token': token}
        )
        message = get_template('registration/account_activation_email.html').render(
            {'confirm_url': url}
        )
        mail = EmailMessage(
            'Account Confirmation',
            message,
            to=[form.instance],
            from_email='noreply@domain.com',
        )
        mail.content_subtype = 'html'
        mail.send()
        return super().form_valid(form)


class PendingRegistration(TemplateView):
    template_name = 'registration/registration_pending.html'


def confirm_registration_view(request, user_id, token):
    """View for user to confirm registration."""
    user_id = force_str(urlsafe_base64_decode(user_id))
    user = User.objects.get(pk=user_id)

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
    return redirect('accounts:login')
