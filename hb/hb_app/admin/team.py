from django.contrib import admin

from hb_app.models import Team, TeamMember


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    inlines = [TeamMemberInline]


__all__ = (
    'TeamAdmin',
)
