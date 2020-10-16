from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from mailinglist.models import MailingList
from mailinglist.forms import MailingListForm


class MailinglistListView(LoginRequiredMixin, ListView):
    model = MailingList

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)


class MailinglistDetailView(LoginRequiredMixin, DetailView):
    model = MailingList

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)


class MailingListCreateView(LoginRequiredMixin, CreateView):
    model = MailingList
    form_class = MailingListForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add'
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailinglistUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingList
    form_class = MailingListForm

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit'
        return context


class MailinglistDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingList
    success_url = reverse_lazy('mailinglist:mailinglist-list')

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)
