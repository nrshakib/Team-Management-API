from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from teams.models import Team, TeamMembership
from teams.serializers import TeamMembershipSerializer, TeamSerializer
from utils.utils import api_response

# Create your views here.
class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    # it will query for whether the user is in the created by list or memberships.user list
    def get_queryset(self):
        return Team.objects.filter(
            Q(created_by = self.request.user) |
            Q(membership__user = self.request.user)
        )

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception = True)
    
            self.perform_create(serializer)
    
            return api_response(
                message="Team created successfully.",
                data=serializer.data,
                status_text="Success",
                http_status=status.HTTP_201_CREATED
            )
    # get all
    def list(self, request, *args, **kwargs):
         queryset = self.filter_queryset(self.get_queryset())
         serializer = self.get_serializer(queryset, many = True)

         return api_response(
            message="Teams retrieved successfully.",
            data=serializer.data,
            status_text="Success",
            http_status=status.HTTP_200_OK
         )

     # RETRIEVE
    def retrieve(self, request, *args, **kwargs):
        team = self.get_object()
        serializer = self.get_serializer(team)

        return api_response(
            message="Team details retrieved successfully.",
            data=serializer.data,
            status_text="Success",
            http_status=status.HTTP_200_OK
        )

    # UPDATE
    def update(self, request, *args, **kwargs):
        partial = kwargs.get("partial", False)

        team = self.get_object()

        serializer = self.get_serializer(
            team,
            data=request.data,
            partial=partial
        )
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return api_response(
            message='Team updated successfully',
            data=serializer.data,
            status_text="Success",
            http_status=status.HTTP_200_OK
        )

    # DELETE
    def destroy(self, request, *args, **kwargs):
        team = self.get_object()
        team_id = team.id

        self.perform_destroy(team)

        return api_response(
            message="Team deleted successfully.",
            data={"id": team_id},
            status_text="Success",
            http_status=status.HTTP_200_OK
        )

    # create team and set user role
    @transaction.atomic
    def perform_create(self, serializer):
        team = serializer.save(created_by = self.request.user)

        TeamMembership.objects.create(
            team = team,
            user = self.request.user,
            role = TeamMembership.MemberRoles.OWNER
        )

    
class TeamMembershipViewSet(ReadOnlyModelViewSet):
    serializer_class = TeamMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamMembership.objects.filter(
            Q(team__created_by = self.request.user) |
            Q(team__membership__user = self.request.user)
        ).distinct()

    # get all
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many = True)
    
        return api_response(
            message="Team members retrieved successfully.",
            data=serializer.data,
            status_text="Success",
            http_status=status.HTTP_200_OK
        )
    
    # RETRIEVE
    def retrieve(self, request, *args, **kwargs):
        members = self.get_object()
        serializer = self.get_serializer(members)
    
        return api_response(
            message="Team member details retrieved successfully.",
            data=serializer.data,
            status_text="Success",
            http_status=status.HTTP_200_OK
        )