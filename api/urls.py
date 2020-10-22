from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'api'

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api-auth-token'),
    path('mailinglist/', views.MailingListCreateListView.as_view(),
         name='api-mailinglist-list'),
    path('mailinglist/<uuid:pk>/',
         views.MailingListRetrieveUpdateDestroyView.as_view(),
         name='api-mailinglist-detail'),
    path('mailinglist/<uuid:mailinglist_pk>/subscribers/',
         views.SubscriberListCreateView.as_view(),
         name='api-subscriber-list'),
    path('subscriber/<uuid:pk>/',
         views.SubscriberRetrieveUpdateDestroyView.as_view(),
         name='api-subscriber-detail'),
]
