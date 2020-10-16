from django.urls import path

from . import views


app_name = 'mailinglist'

urlpatterns = [
    path('', views.MailinglistListView.as_view(), name='mailinglist-list'),
    path('<pk>/', views.MailinglistDetailView.as_view(),
         name='mailinglist-detail'),
]
