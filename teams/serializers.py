from rest_framework import serializers

from accounts.models import User
from teams.models import Team, TeamMembership

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class TeamSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class TeamMembershipSerializer(serializers.ModelSerializer):
    team = TeamSummarySerializer(read_only=True)
    user = UserSummarySerializer(read_only=True)
    
    class Meta:
        model = TeamMembership
        fields = ['id', 'team', 'user', 'role', 'joined_at']
        read_only_fields = ['id', 'joined_at']