import pytest
from django.http import HttpResponse
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from accounts.factories import UserFactory
from mailinglist.factories import MailinglistFactory


@pytest.fixture
def testuser() -> UserFactory:
    return UserFactory(is_active=True)


@pytest.fixture
def db_with_three_mailinglists(testuser):
    return [MailinglistFactory(owner=testuser) for i in range(3)]


@pytest.fixture
def mailinglist(testuser):
    return MailinglistFactory(owner=testuser)


def test_mailinglist_list_view_unauthenticated(client) -> None:
    response: HttpResponse = client.get(reverse('mailinglist:mailinglist-list'))

    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/mailinglist/'


def test_mailinglist_list_view_authenticated(
    client, testuser: UserFactory, db_with_three_mailinglists: list[MailinglistFactory]
) -> None:
    client.force_login(testuser)
    response: HttpResponse = client.get(reverse('mailinglist:mailinglist-list'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'mailinglist/mailinglist_list.html')
    assert list(response.context['object_list']) == db_with_three_mailinglists


def test_mailinglist_detail_view_unauthenticated(client, testuser, mailinglist) -> None:
    response: HttpResponse = client.get(
        reverse('mailinglist:mailinglist-detail', kwargs={'pk': mailinglist.pk})
    )

    assert response.status_code == 302
    assert response.url == f'/accounts/login/?next=/mailinglist/{mailinglist.pk}/'


def test_mailinglist_detail_view_authenticated(
    client, testuser: UserFactory, mailinglist
) -> None:
    client.force_login(testuser)
    response: HttpResponse = client.get(
        reverse('mailinglist:mailinglist-detail', kwargs={'pk': mailinglist.pk})
    )

    assert response.status_code == 200
    assertTemplateUsed(response, 'mailinglist/mailinglist_detail.html')
    assert response.context['object'] == mailinglist
