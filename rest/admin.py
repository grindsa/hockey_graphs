# -*- coding: utf-8 -*-
""" admin class """
from django.contrib import admin

# Register your models here.
from rest.models import Gameheader, Match, Periodevent, Player, Playerstat, Roster, Season, Shift, Shot, Team, Teamstat

class MatchAdmin(admin.ModelAdmin):
    """ match admin """
    fields = ['season', 'match_id', 'date', 'date_uts', 'home_team', 'visitor_team', 'result', 'finish']
    list_display = ['season', 'match_id', 'date', 'date_uts', 'home_team', 'visitor_team', 'result', 'finish']
    ordering = ['match_id']

class PeriodeventAdmin(admin.ModelAdmin):
    """ shots admin """
    fields = ['match', 'period_event']
    list_display = ['match']
    ordering = ['match_id']

class PlayerAdmin(admin.ModelAdmin):
    """ player admin """
    fields = ['player_id', 'first_name', 'last_name', 'jersey']
    list_display = ['player_id', 'first_name', 'last_name', 'jersey']
    ordering = ['player_id']

class PlayerstatAdmin(admin.ModelAdmin):
    """ shots admin """
    fields = ['match', 'home', 'visitor']
    list_display = ['match']
    ordering = ['match_id']

class GameheaderAdmin(admin.ModelAdmin):
    """ gameheader admin """
    fields = ['match', 'gameheader']
    list_display = ['match', 'gameheader']
    ordering = ['match_id']

class RosterAdmin(admin.ModelAdmin):
    """ Roster admin """
    fields = ['match', 'roster']
    list_display = ['match']
    ordering = ['match_id']

class SeasonAdmin(admin.ModelAdmin):
    """ season admin """
    fields = ['name', 'shortcut']
    list_display = ['name', 'shortcut']
    ordering = ['name']

class ShiftAdmin(admin.ModelAdmin):
    """ shots admin """
    fields = ['match', 'shift']
    list_display = ['match']
    ordering = ['match_id']

class ShotAdmin(admin.ModelAdmin):
    """ shots admin """
    fields = [field.name for field in Shot._meta.get_fields()]
    list_display = [field.name for field in Shot._meta.get_fields()]
    ordering = ['shot_id']

class TeamAdmin(admin.ModelAdmin):
    """ teamadmin"""
    fields = ['team_id', 'team_name', 'shortcut', 'logo']
    list_display = ['team_id', 'team_name', 'shortcut', 'logo']
    ordering = ['team_id']

class TeamstatAdmin(admin.ModelAdmin):
    """ shots admin """
    fields = ['match', 'home', 'visitor']
    list_display = ['match', 'home', 'visitor']
    ordering = ['match_id']

admin.site.register(Match, MatchAdmin)
admin.site.register(Periodevent, PeriodeventAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Playerstat, PlayerstatAdmin)
admin.site.register(Roster, RosterAdmin)
admin.site.register(Gameheader, GameheaderAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Shot, ShotAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Teamstat, TeamstatAdmin)
