from django.apps import AppConfig


class MailinglistConfig(AppConfig):
    name = 'mailinglist'

    def ready(self):
        from . import signals  # noqa: F401
