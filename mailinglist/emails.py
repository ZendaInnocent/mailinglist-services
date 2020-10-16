from django.conf import settings
from django.template import Context
from django.urls import reverse


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
        return settings.MAIL_LIST_LINK_DOMAIN + path
