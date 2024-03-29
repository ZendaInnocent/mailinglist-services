from django.urls import path

from . import views

app_name = 'mailinglist'

urlpatterns = [
    path('', views.mailinglist_list, name='mailinglist-list'),
    path('add/', views.mailinglist_add, name='mailinglist-add'),
    path('<uuid:pk>/', views.mailinglist_detail, name='mailinglist-detail'),
    path('<uuid:pk>/update/', views.mailinglist_update, name='mailinglist-update'),
    path('<uuid:pk>/delete/', views.mailinglist_delete, name='mailinglist-delete'),
    path(
        '<uuid:pk>/subscribe/',
        views.SubscribeToMailingListView.as_view(),
        name='subscribe',
    ),
    path(
        '<uuid:pk>/thank-you/',
        views.ThankYouForSubscribingView.as_view(),
        name='subscriber-thank-you',
    ),
    path(
        'subscribe/confirmation/<uuid:pk>/',
        views.ConfirmSubscriptionView.as_view(),
        name='confirm-subscription',
    ),
    path('unsubscribe/<uuid:pk>/', views.UnsubscribeView.as_view(), name='unsubscribe'),
    path(
        '<uuid:pk>/message/new/',
        views.MessageCreateView.as_view(),
        name='message-create',
    ),
    path(
        'message/<uuid:pk>/', views.MessageDetailView.as_view(), name='message-detail'
    ),
]
