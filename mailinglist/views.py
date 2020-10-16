from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from mailinglist.forms import MailingListForm

from mailinglist.models import MailingList


class MailinglistListView(ListView):
    model = MailingList


class MailinglistDetailView(DetailView):
    model = MailingList


class MailingListCreateView(CreateView):
    model = MailingList
    form_class = MailingListForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
