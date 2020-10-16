from django.shortcuts import render
from django.views.generic import ListView

from mailinglist.models import MailingList


class MailinglistListView(ListView):
    model = MailingList
