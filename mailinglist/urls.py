from django.urls import path

from . import views


app_name = 'mailinglist'

urlpatterns = [
    path('', views.MailinglistListView.as_view(), name='mailinglist-list'),
    path('add/', views.MailingListCreateView.as_view(),
         name='mailinglist-create'),
    path('<uuid:pk>/', views.MailinglistDetailView.as_view(),
         name='mailinglist-detail'),
    path('<uuid:pk>/update/', views.MailinglistUpdateView.as_view(),
         name='mailinglist-update'),
    path('<uuid:pk>/delete/', views.MailinglistDeleteView.as_view(),
         name='mailinglist-delete'),
    path('<uuid:pk>/subscribe/', views.SubscribeToMailingListView.as_view(),
         name='subscribe'),
    path('<uuid:pk>/thank-you/', views.ThankYouForSubscribingView.as_view(),
         name='subscriber-thank-you'),
    path('subscribe/confirmation/<uuid:pk>/',
         views.ConfirmSubscriptionView.as_view(), name='confirm-subscription'),
    path('unsubscribe/<uuid:pk>/', views.UnsubscribeView.as_view(),
         name='unsubscribe'),
    path('<uuid:pk>/message/new/', views.MessageCreateView.as_view(),
         name='message-create'),
]
