from django.urls.base import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from mailinglist.models import MailingList, Subscriber
from mailinglist.forms import MailingListForm, SubscriberForm


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


class SubscribeToMailingListView(CreateView):
    model = Subscriber
    form_class = SubscriberForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mailinglist'] = MailingList.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        mailinglist = MailingList.objects.get(pk=self.kwargs['pk'])
        form.instance.mailing_list = mailinglist
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailinglist:subscriber-thank-you', kwargs={
            'pk': self.kwargs['pk']
        })


class ThankYouForSubscribingView(DetailView):
    model = MailingList
    template_name = 'mailinglist/subscription_thank_you.html'


class ConfirmSubscriptionView(DetailView):
    model = Subscriber
    template_name = 'mailinglist/confirm_subscription.html'

    def get_object(self):
        subscriber = super().get_object()
        subscriber.confirmed = True
        subscriber.save()
        return subscriber
