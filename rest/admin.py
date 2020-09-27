# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from rest.models import Match, Player, Season, Shot, Team

class MatchAdmin(admin.ModelAdmin):
    fields = ['season', 'match_id', 'date', 'date_uts', 'home_team', 'visitor_team']
    list_display = ['season', 'match_id', 'date', 'date_uts', 'home_team', 'visitor_team']
    ordering = ['match_id']

class PlayerAdmin(admin.ModelAdmin):
    fields = ['player_id', 'first_name', 'last_name', 'jersey']
    list_display = ['player_id', 'first_name', 'last_name', 'jersey']
    ordering = ['player_id']

class SeasonAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']
    ordering = ['name']

class ShotAdmin(admin.ModelAdmin):
    fields = [field.name for field in Season._meta.get_fields()]
    list_display = [field.name for field in Shot._meta.get_fields()]
    ordering = ['shot_id']

class TeamAdmin(admin.ModelAdmin):
    """ teamadmin"""
    fields = ['team_id', 'team_name', 'shortcut']
    list_display = ['team_id', 'team_name', 'shortcut']
    ordering = ['team_id']

admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Shot, ShotAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Team, TeamAdmin)
