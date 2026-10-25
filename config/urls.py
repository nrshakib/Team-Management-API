#URL configuration for config project.


from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),

    #JWT Auth tokens
    path('api/v1/login/', CustomLoginView.as_view(), name = 'user-login'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name = 'token-refresh'),
]
