from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
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
