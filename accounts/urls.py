from django.urls import path

from accounts import views


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name = "user-registration")
]