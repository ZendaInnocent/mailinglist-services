from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from mailinglist.models import MailingList


class MailinglistListView(ListView):
    model = MailingList


class MailinglistDetailView(DetailView):
    model = MailingList
