from django.db import models

from config import settings

# Create your models here.
class TeamModel(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=150, blank=True, default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="created_teams",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TeamMembershipModel(models.Model):
    class MemberRoles(models.TextChoices):
        OWNER = 'owner', 'Owner'
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'

    team = models.ForeignKey(
        TeamModel,
        on_delete=models.CASCADE,
        related_name='membership'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_membership"
    )
    role = models.CharField(max_length=15, choices=MemberRoles.choices, default=MemberRoles.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields= ['team', 'user'],
                name = 'unique_team_user_membership'
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.team}"