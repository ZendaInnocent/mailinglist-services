from django.urls import path

from . import views


app_name = 'mailinglist'

urlpatterns = [
    path('', views.MailinglistListView.as_view(), name='mailinglist-list'),
]
