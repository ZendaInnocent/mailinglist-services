from django.urls import path, include

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserRegistrationView.as_view(), name='signup'),
    path('confirm-email/<str:user_id>/<str:token>/',
         views.confirm_registration_view, name='confirm-email'),
    path('pending-registration/', views.PendingRegistration.as_view(),
         name='pending-registration'),
    path('', include('django.contrib.auth.urls')),
]
