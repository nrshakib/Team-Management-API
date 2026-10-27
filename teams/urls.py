from django.urls import path
from rest_framework.routers import DefaultRouter

from teams import views

router = DefaultRouter()

router.register(r'teams', views.TeamViewSet, basename = 'teams')
router.register(r'memberships', views.TeamMembershipViewSet, basename = 'memberships')

urlpatterns = router.urls