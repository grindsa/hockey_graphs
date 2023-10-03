# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413, R0914
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.models import Playerstatistics
from rest.functions.heatmap import gameheatmapdata_get
from rest.functions.helper import url_build, mobile_check
from rest.functions.match import match_list_get, matchinfo_list_get
from rest.functions.playerstat import playerstatistics_get
from rest.functions.shot import shot_list_perplayer_get, shot_dic_convert
from rest.functions.shotcharts import shotmapchart_create

def playerstatistics_fetch(logger, request, season_id=None, player_id=None):
    """ matchstatistics grouped by days """
    logger.debug('matchstatistics_get({0}:{1})'.format(season_id, player_id))

    # check if access comes via mobile
    ismobile = mobile_check(logger, request)

    # we protect the REST and will not return anything without specifiying season_id and player_id
    if season_id and player_id:

        result = []

        # collect matches per season
        match_list = match_list_get(logger, 'season', season_id, ['match_id'])
        match_info_dic = matchinfo_list_get(logger, match_list, request)

        # collect shots per player per season as both list and dictionary of matches
        shot_list = shot_list_perplayer_get(logger, player_id, match_list, ['shot_id', 'player_id', 'player__first_name', 'player__last_name', 'player__jersey', 'timestamp', 'match_shot_resutl_id', 'team_id', 'match_id', 'coordinate_x', 'coordinate_y', 'match__home_team__shortcut'])
        shot_dic = _shots_per_match_get(logger, shot_list)
        # shotlist and shot dic with converted coordinates
        (converted_shot_list, converted_shot_dic) =  shot_dic_convert(logger, shot_dic, match_info_dic)

        # fake_matchinfo_dic = {'home_team__shortcut': 'foofofoshortcut', 'visitor_team__shortcut': 'foofoovistiorshortcut', 'home_team_logo': 'foohometeamlogo', 'visitor_team_logo': 'visitor_team_logo'}
        # disabled as it looks ugly
        # result.append(_playershotmap_get(logger, 'title', 'subtitle', ismobile, fake_matchinfo_dic, shot_list))
        #result.append(_playerheatmap_get(logger, _('Shot attempts'), 'subtitle', ismobile, fake_matchinfo_dic, shot_list))

        (playerstatistics_list, playerstatistics_dic) = playerstatistics_get(logger, match_list, player_id, request)
        #from pprint import pprint
        #pprint(playerstatistics_list)
        # get matchstatistics
        #result.append(banana_chart1_create(logger, 'title1'))
        #result.append(banana_chart2_create(logger, 'title2'))


        #pass
    else:
        result = {'error': 'Please specify a season and player'}

    return result

def _playershotmap_get(logger, title, subtitle, ismobile, matchinfo_dic, shot_list):
    """ get playershotmap """
    logger.debug('_gameshotmap_get()')

    shot_table = {}
    stat_entry = {}

    if shot_list:
        # get shots and goals per min
        shot_chart = shotmapchart_create(logger, '{0} {1}'.format(title, matchinfo_dic['home_team__shortcut']), subtitle, ismobile, shot_list, player_chart=True)

        stat_entry = {
            'title': title,
            'chart': shot_chart,
            'table': shot_table,
        }

    return stat_entry

def _playerheatmap_get(logger, title, subtitle, ismobile, matchinfo_dic, shot_list):
    """ get playerheatmap """
    logger.debug('_gameshotmap_get()')

    shot_table = None
    shotmap_dic = {}

    if shot_list:
        # get shots and goals per min
        shotmap_dic = gameheatmapdata_get(logger, title, subtitle, ismobile, matchinfo_dic, shot_list)

        stat_entry = {
            'title': title,
            'chart': shotmap_dic,
            'table': shot_table,
        }

    return stat_entry

def _shots_per_match_get(logger, shot_list):
    """ split shot_list in shots per match """
    logger.debug('_shots_per_match_get()')
    shot_dic = {}
    for shot in shot_list:
        if shot['match_id'] not in shot_dic:
            shot_dic[shot['match_id']] = []
        shot_dic[shot['match_id']].append(shot)

    logger.debug('_shots_per_match_get() ended with {0} match_entries'.format(len(shot_dic.keys())))
    return shot_dic

def playerstatistics_single_get(logger, season_id=None, player_id=None,  vlist=('season_id', 'player_id', 'faceoff', 'toi')):
    """ get playerstatistics for a player per season"""
    logger.debug('playerstatistics_single_get()')
    try:
        if len(vlist) == 1:
            playerstat_dic = list(Playerstatistics.objects.filter(season_id=season_id, player_id=player_id).values_list(vlist[0], flat=True))[0]
        else:
            playerstat_dic = Playerstatistics.objects.filter(season_id=season_id, player_id=player_id).values(*vlist)[0]
    except BaseException:
        playerstat_dic = {}

    return playerstat_dic

def playerstatistics_single_add(logger, season_id=None, player_id=None, match_id=None, data_dic={}):
    """ add playerstat to database """
    logger.debug('playerstatistics_single_add({0}:{1})'.format(season_id, player_id, data_dic))

    try:
        # add playerstatistics
        obj, _created = Playerstatistics.objects.update_or_create(season_id=season_id, player_id=player_id, match_id=match_id, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in playerstatistics_single_add(): {0}'.format(err_))
        result = None
    logger.debug('playerstatistics_single_add({0}:{1}) ended with {2}'.format(season_id, player_id, result))
    return result

