from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.views import generic

from mailinglist.forms import MailingListForm, MessageForm, SubscriberForm
from mailinglist.mixins import MailingListMixin
from mailinglist.models import MailingList, Message, Subscriber


class MailinglistListView(
    LoginRequiredMixin,
    MailingListMixin,
    generic.ListView,
):
    model = MailingList


mailinglist_list = MailinglistListView.as_view()


class MailinglistDetailView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DetailView,
):
    model = MailingList

    def test_func(self):
        return self.get_object().owner == self.request.user


mailinglist_detail = MailinglistDetailView.as_view()


class MailingListCreateView(LoginRequiredMixin, generic.CreateView):
    model = MailingList
    form_class = MailingListForm
    extra_context = {'page_title': 'Add'}

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


mailinglist_add = MailingListCreateView.as_view()


class MailinglistUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView,
):
    model = MailingList
    form_class = MailingListForm
    extra_context = {'page_title': 'Edit'}

    def test_func(self):
        return self.get_object().owner == self.request.user


mailinglist_update = MailinglistUpdateView.as_view()


class MailinglistDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView,
):
    model = MailingList
    success_url = reverse_lazy('mailinglist:mailinglist-list')

    def test_func(self):
        return self.get_object().owner == self.request.user


mailinglist_delete = MailinglistDeleteView.as_view()


class SubscribeToMailingListView(generic.CreateView):
    model = Subscriber
    form_class = SubscriberForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.mailing_list = MailingList.objects.get(pk=self.kwargs['pk'])
        context['mailinglist'] = self.mailing_list
        return context

    def form_valid(self, form):
        mailing_list = self.mailing_list
        form.instance.mailing_list = mailing_list
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'mailinglist:subscriber-thank-you',
            kwargs={
                'pk': self.mailing_list.pk,
            },
        )


class ThankYouForSubscribingView(generic.DetailView):
    model = MailingList
    template_name = 'mailinglist/subscription_thank_you.html'


class ConfirmSubscriptionView(generic.DetailView):
    model = Subscriber
    template_name = 'mailinglist/confirm_subscription.html'

    def get_object(self):
        subscriber = super().get_object()
        subscriber.confirmed = True
        subscriber.save()
        return subscriber


class UnsubscribeView(generic.DeleteView):
    model = Subscriber
    template_name = 'mailinglist/unsubscribe.html'

    def get_success_url(self):
        return reverse_lazy(
            'mailinglist:subscribe',
            kwargs={'pk': self.get_object().mailing_list.id},
        )


class MessageCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView,
):
    SAVE_ACTION = 'save'
    PREVIEW_ACTION = 'preview'

    model = Message
    form_class = MessageForm

    def test_func(self):
        mailinglist = get_object_or_404(MailingList, pk=self.kwargs['pk'])
        return mailinglist.owner == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.mailing_list = get_object_or_404(
            MailingList,
            pk=self.kwargs['pk'],
        )

        context['mailinglist'] = self.mailing_list
        context['SAVE_ACTION'] = self.SAVE_ACTION
        context['PREVIEW_ACTION'] = self.PREVIEW_ACTION
        return context

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == self.PREVIEW_ACTION:
            context = self.get_context_data(form=form, preview=form.instance)
            return self.render_to_response(context=context)
        elif action == self.SAVE_ACTION:
            form.instance.mailing_list = self.mailing_list
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'mailinglist:mailinglist-detail',
            kwargs={'pk': self.mailing_list.pk},
        )


class MessageDetailView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DetailView,
):
    model = Message

    def test_func(self):
        message = self.get_object()
        return message.mailing_list.owner == self.request.user
