from celery import shared_task

from . import utils
from .models import User


@shared_task
def send_registration_confirmation_mail(user_id):
    user = User.objects.get(pk=user_id)
    utils.send_registration_confirmation_mail(user.email)
