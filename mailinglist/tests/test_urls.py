import uuid

from django.urls import resolve, reverse_lazy

from mailinglist import views


def test_mailinglist_list_url_resolves() -> None:
    url = reverse_lazy('mailinglist:mailinglist-list')

    assert resolve(url).func == views.mailinglist_list


def test_mailinglist_add_url_resolves() -> None:
    url = reverse_lazy('mailinglist:mailinglist-add')

    assert resolve(url).func == views.mailinglist_add


def test_mailinglist_detail_url_resolves() -> None:
    url = reverse_lazy('mailinglist:mailinglist-detail', kwargs={'pk': uuid.uuid4()})

    assert resolve(url).func == views.mailinglist_detail


def test_mailinglist_update_url_resolves() -> None:
    url = reverse_lazy('mailinglist:mailinglist-update', kwargs={'pk': uuid.uuid4()})

    assert resolve(url).func == views.mailinglist_update


def test_mailinglist_delete_url_resolves() -> None:
    url = reverse_lazy('mailinglist:mailinglist-delete', kwargs={'pk': uuid.uuid4()})

    assert resolve(url).func == views.mailinglist_delete
