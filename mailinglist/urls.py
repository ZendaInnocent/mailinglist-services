from django.urls import path

from . import views


app_name = 'mailinglist'

urlpatterns = [
    path('', views.MailinglistListView.as_view(), name='mailinglist-list'),
    path('add/', views.MailingListCreateView.as_view(),
         name='mailinglist-create'),
    path('<pk>/', views.MailinglistDetailView.as_view(),
         name='mailinglist-detail'),
    path('<pk>/update/', views.MailinglistUpdateView.as_view(),
         name='mailinglist-update'),
]
