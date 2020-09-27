from django.contrib import admin

# Register your models here.
from rest.models import Match, Player, Season, Shot, Team

class MatchAdmin(admin.ModelAdmin):
    fields = [field.name for field in Match._meta.get_fields()]
    list_display = [field.name for field in Match._meta.get_fields()]
    ordering = ['match_id']

class PlayerAdmin(admin.ModelAdmin):
    fields = ['id', 'player_id', 'date', 'first_name', 'last_name', 'jersey']
    list_display = ['id', 'player_id', 'date', 'first_name', 'last_name', 'jersey']
    ordering = ['player_id']

class SeasonAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']
    ordering = ['name']

class ShotAdmin(admin.ModelAdmin):
    fields = [field.name for field in Season._meta.get_fields()]
    list_display = [field.name for field in Shot._meta.get_fields()]
    ordering = ['id']

class TeamAdmin(admin.ModelAdmin):
    """ teamadmin"""
    fields = ['home_team', 'visitor_team', 'team_id', 'team_name', 'short_name']
    list_display = ['team_id', 'home_team', 'visitor_team', 'id', 'team_name', 'short_name']
    ordering = ['team_id']

admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Shot, ShotAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Team, TeamAdmin)
