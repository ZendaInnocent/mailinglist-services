from django.conf import settings
from django.template import engines, Context
from django.urls import reverse
from django.core.mail import send_mail


CONFIRM_SUBSCRIPTION_TEXT = 'mailinglist/email_templates/confirmation.txt'
CONFIRM_SUBSCRIPTION_HTML = 'mailinglist/email_templates/confirmation.html'


class EmailTemplateContext(Context):

    def __init__(self, subscriber, dict_=None, **kwargs):
        if dict_ is None:
            dict_ = {}
        email_context = self.common_context(subscriber)
        email_context.update(dict_)
        super().__init__(email_context, **kwargs)

    def common_context(self, subscriber):
        subscriber_pk_kwargs = {'pk': subscriber.id}
        unsubscribe_path = reverse(
            'mailinglist:unsubscribe', kwargs=subscriber_pk_kwargs)
        return {
            'subscriber': subscriber,
            'mailinglist': subscriber.mailing_list,
            'unsubscription_link': self.make_link(unsubscribe_path)
        }

    @staticmethod
    def make_link(path):
        return settings.MAILING_LIST_LINK_DOMAIN + path


def send_confirmation_email(subscriber):
    mailinglist = subscriber.mailing_list
    confirmation_link = EmailTemplateContext.make_link(
        reverse('mailinglist:confirm-subscription', kwargs={
            'pk': subscriber.id
        })
    )
    context = EmailTemplateContext(subscriber,
                                   {'confirmation_link': confirmation_link})
    subject = f'Confirming subscription to {mailinglist.name}'

    dt_engine = engines['django'].engine

    text_body_template = dt_engine.get_template(CONFIRM_SUBSCRIPTION_TEXT)
    text_body = text_body_template.render(context)

    html_body_template = dt_engine.get_template(CONFIRM_SUBSCRIPTION_HTML)
    html_body = html_body_template.render(context)

    send_mail(
        subject=subject,
        message=text_body,
        from_email=settings.MAILING_LIST_FROM_EMAIL,
        recipient_list=[subscriber.email, ],
        html_message=html_body
    )
