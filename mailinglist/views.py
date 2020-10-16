from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from mailinglist.forms import MailingListForm

from mailinglist.models import MailingList


class MailinglistListView(ListView):
    model = MailingList


class MailinglistDetailView(DetailView):
    model = MailingList


class MailingListCreateView(CreateView):
    model = MailingList
    form_class = MailingListForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add'
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailinglistUpdateView(UpdateView):
    model = MailingList
    form_class = MailingListForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit'
        return context
