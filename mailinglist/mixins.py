from .models import MailingList


class MailingListMixin:
    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)
