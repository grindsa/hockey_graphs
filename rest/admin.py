# -*- coding: utf-8 -*-
""" admin class """
from django.contrib import admin

# Register your models here.
from rest.models import Comment, Gameheader, Match, Periodevent, Player, Playerstat, Roster, Season, Shift, Shot, Socialnetworkevent, Team, Teamstat, Teammatchstat, Xg

class MatchAdmin(admin.ModelAdmin):
    """ match admin """
    fields = ['season', 'match_id', 'date', 'date_uts', 'home_team', 'visitor_team', 'result', 'finish', 'disable']
    list_display = ['season', 'match_id', 'date', 'date_uts', 'home_team', 'visitor_team', 'result', 'finish', 'disable']
    ordering = ['match_id']

class PeriodeventAdmin(admin.ModelAdmin):
    """ shots admin """
    fields = ['match', 'period_event']
    list_display = ['match']
    ordering = ['match_id']

class PlayerAdmin(admin.ModelAdmin):
    """ player admin """
    fields = ['player_id', 'first_name', 'last_name', 'jersey', 'stick', 'height', 'weight']
    list_display = ['player_id', 'first_name', 'last_name', 'jersey', 'stick', 'height', 'weight']
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

class CommentAdmin(admin.ModelAdmin):
    """ Roster admin """
    fields = ['name', 'de', 'en']
    list_display = ['name', 'de', 'en']
    ordering = ['name', 'de', 'en']

class RosterAdmin(admin.ModelAdmin):
    """ Roster admin """
    fields = ['match', 'roster']
    list_display = ['match']
    ordering = ['match_id']

class SeasonAdmin(admin.ModelAdmin):
    """ season admin """
    fields = ['name', 'shortcut', 'tournament']
    list_display = ['name', 'shortcut', 'tournament']
    ordering = ['tournament']

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

class SocialnetworkeventAdmin(admin.ModelAdmin):
    fields = ['match', 'source', 'created_at', 'created_uts', 'identifier', 'name', 'name_alternate', 'text_cleaned', 'text_raw', 'tag']
    list_display = ['match', 'source', 'created_at', 'created_uts', 'identifier', 'name', 'name_alternate', 'text_cleaned', 'text_raw', 'tag']
    ordering = ['match_id', 'created_uts']

class TeamAdmin(admin.ModelAdmin):
    """ teamadmin"""
    fields = ['team_id', 'team_name', 'shortcut', 'logo', 'color_primary', 'color_secondary', 'color_penalty_primary', 'color_penalty_secondary', 'twitter_name']
    list_display = ['team_id', 'team_name', 'shortcut', 'logo', 'color_primary', 'color_secondary', 'color_penalty_primary', 'color_penalty_secondary', 'twitter_name']
    ordering = ['team_id']

class TeamstatAdmin(admin.ModelAdmin):
    """ shots admin """
    fields = ['match', 'home', 'visitor']
    list_display = ['match', 'home', 'visitor']
    ordering = ['match_id']

class TeammatchstatAdmin(admin.ModelAdmin):
    """ admin class for teammatchstat """
    fields = ['match', 'team', 'goals_for', 'goals_against', 'goals_pp', 'goals_pp_against', 'goals_sh', 'xgoals_for', 'xgoals_against', 'shots_for', 'shots_for_5v5', 'shots_ongoal_for', 'shots_ongoal_for_5v5', 'shots_ongoal_pctg', 'shots_against', 'shots_against_5v5', 'shots_ongoal_against', 'shots_ongoal_against_5v5', 'saves', 'saves_pctg', 'faceoffswon', 'faceoffslost', 'faceoffswon_pctg', 'penaltyminutes_drawn', 'penaltyminutes_taken', 'powerplayseconds', 'rebounds_for', 'rebounds_against', 'goals_rebound_for', 'goals_rebound_against', 'breaks_for', 'breaks_against', 'goals_break_for', 'goals_break_against', 'ppcount', 'shcount', 'points']
    list_display = ['match', 'team', 'goals_for', 'goals_against', 'goals_pp', 'goals_pp_against', 'goals_sh', 'shots_for', 'shots_for_5v5', 'shots_ongoal_for', 'shots_ongoal_for_5v5', 'shots_ongoal_pctg', 'shots_against', 'shots_against_5v5', 'shots_ongoal_against', 'shots_ongoal_against_5v5', 'saves', 'saves_pctg', 'faceoffswon', 'faceoffslost', 'faceoffswon_pctg', 'penaltyminutes_drawn', 'penaltyminutes_taken', 'powerplayseconds', 'rebounds_for', 'rebounds_against', 'goals_rebound_for', 'goals_rebound_against', 'breaks_for', 'breaks_against', 'goals_break_for', 'goals_break_against', 'ppcount', 'shcount', 'points']
    ordering = ['match_id', 'team_id']

#class XgAdmin(admin.ModelAdmin):
#     """ admin class for xg model """
#    # fields = ['xg_data']
#    # list_display = ['xg_data']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Periodevent, PeriodeventAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Playerstat, PlayerstatAdmin)
admin.site.register(Roster, RosterAdmin)
admin.site.register(Gameheader, GameheaderAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Shot, ShotAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Socialnetworkevent, SocialnetworkeventAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Teamstat, TeamstatAdmin)
admin.site.register(Teammatchstat, TeammatchstatAdmin)
#admin.site.register(Xg, XgAdmin)
