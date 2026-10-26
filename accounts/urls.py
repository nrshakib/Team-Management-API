from django.urls import path

from accounts import views


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name = "user-registration"),
    path('profile/', views.UserProfileView.as_view(), name = "user-profile"),
    path('change-password/', views.ChangePasswordView.as_view(), name = "change-password"),
    path('logout/', views.LogoutView.as_view(), name = "logout"),
]