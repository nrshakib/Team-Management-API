from django.contrib import admin

from teams.models import TeamMembership, Team

# Register your models here.
@admin.register(Team)
class TeamModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    search_fields = ['name', 'created_by__email']
    list_filter = ['created_by', 'created_at']

@admin.register(TeamMembership)
class MembershipModelAdmin(admin.ModelAdmin):
    list_display = ['team', 'user', 'role', 'joined_at']
    search_fields = ['team__name', 'user__email']
    list_filter = ['role', 'joined_at']