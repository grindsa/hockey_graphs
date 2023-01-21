# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.models import Playerstat, Playerstatistics
from rest.functions.helper import list2dic, url_build
from rest.functions.lineup import lineup_sort
from rest.functions.shot import shotpersecondlist_get
from rest.functions.timeline import skatersonice_get, penalties_include

def _matchupmatrix_initialize(logger, lineup_dic):
    """ add team to database """
    logger.debug('_matchupmatrix_initialize()')
    matchup_matrix = {}
    for hplayer in lineup_dic['home_team']:
        matchup_matrix[hplayer] = {}
        for vplayer in lineup_dic['visitor_team']:
            matchup_matrix[hplayer][vplayer] = {'seconds': 0, 'home_shots': 0, 'visitor_shots': 0}
    return matchup_matrix

def _five_filter(five_filter, hteam, vteam):
    """ check if there is no penalty """
    process_it = False
    if five_filter:
        if 'penalty' not in hteam and vteam:
            process_it = True
    else:
        process_it = True

    return process_it

def _matchupmatrix_gen(logger, shotpersec_list, soi_dic, lineup_dic, player_dic, five_filter=False):
    """ create matrix of players and ice_times """

    # generate empty matrix to collect data
    matchup_matrix = _matchupmatrix_initialize(logger, lineup_dic)

    for sec in soi_dic['home_team']:
        # 5v5 check
        if sec in soi_dic['home_team'] and sec in soi_dic['visitor_team']:
            process_sec = _five_filter(five_filter, soi_dic['home_team'][sec], soi_dic['visitor_team'][sec])
        else:
            process_sec = False

        if process_sec:
            if 'player_list' in soi_dic['home_team'][sec] and 'player_list' in  soi_dic['visitor_team'][sec]:
                for hplayer_id in soi_dic['home_team'][sec]['player_list']:
                    for vplayer_id in soi_dic['visitor_team'][sec]['player_list']:
                        if hplayer_id in player_dic and vplayer_id in player_dic:
                            matchup_matrix[player_dic[hplayer_id]][player_dic[vplayer_id]]['seconds'] += 1
                            # print(shotpersec_list['home_team'].count(sec), shotpersec_list['visitor_team'].count(sec))
                            if shotpersec_list['home_team'].count(sec) > 0:
                                matchup_matrix[player_dic[hplayer_id]][player_dic[vplayer_id]]['home_shots'] += shotpersec_list['home_team'].count(sec)
                            if shotpersec_list['visitor_team'].count(sec) > 0:
                                matchup_matrix[player_dic[hplayer_id]][player_dic[vplayer_id]]['visitor_shots'] += shotpersec_list['visitor_team'].count(sec)
    return matchup_matrix

def playerstatistics_add(logger, match_id, player_id, data_dic):
    """ add playerstatistics to database """
    logger.debug('playerstatistics_add({0}:{1})'.format(match_id, player_id))
    try:
        # add playerstat
        obj, _created = Playerstatistics.objects.update_or_create(player_id=player_id, match_id=match_id, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in playerstatistics_add(): {0}'.format(err_))
        result = None
    logger.debug('playerstatistics_add()) ended with {0}'.format(result))
    return result

def playerstatistics_get(logger, match_list, player_id, request, vlist=('match_id', 'player_id', 'team_id', 'oteam_id', 'shots_for', 'shots_for_avg', 'shots_for_5v5', 'shots_for_5v5_avg', 'shots_against', 'shots_against_avg', 'shots_against_5v5', 'shots_against_5v5_avg', 'toi', 'toi_pp', 'toi_pk', 'team__team_name', 'team__shortcut', 'team__logo', 'team__team_name', 'oteam__shortcut', 'oteam__logo')):
    """ get info for a specifc match_id """
    logger.debug('playerstatistics_get({0})'.format(player_id))
    try:
        if len(vlist) == 1:
            playerstatistics_list = list(Playerstatistics.objects.filter(player_id=player_id, match_id__in=match_list).order_by('match_id').values_list(vlist[0], flat=True))
        else:
            playerstatistics_list = list(Playerstatistics.objects.filter(player_id=player_id, match_id__in=match_list).order_by('match_id').values(*vlist))
    except BaseException as err:
        playerstatistics_list = {}

    # change logo link
    try:
        base_url = url_build(request.META)
    except BaseException:
        base_url = None

    for match in playerstatistics_list:
        if 'oteam__logo' in match:
            match['oteam_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match['oteam__logo'])
        if 'team__logo' in match:
            match['team_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match['team__logo'])

    # convert2dict
    playerstatistics_dic = list2dic(logger, playerstatistics_list, 'match_id')

    return playerstatistics_list, playerstatistics_dic

def playerstat_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('playerstat_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add playerstat
        obj, _created = Playerstat.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in playerstat_add(): {0}'.format(err_))
        result = None
    logger.debug('playerstat_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def playerstat_get(logger, fkey, fvalue, vlist=('match_id', 'home', 'visitor')):
    """ get info for a specifc match_id """
    logger.debug('playerstat_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            playerstat_dic = list(Playerstat.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            playerstat_dic = Playerstat.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except BaseException:
        playerstat_dic = {}

    return playerstat_dic

def toifromplayerstats_get(logger, _matchinfo_dic, playerstat_dic):
    """ get info for a specifc match_id """
    logger.debug('toifromplayerstats_get()')

    # inititialize dictionaries to store the data
    toi_dic = {'home_team': {1: {}, 2: {}, 3: {}, 4: {}}, 'visitor_team': {1: {}, 2: {}, 3: {}, 4: {}}}
    tmp_toi_sum_dic = {'home_team': {}, 'visitor_team': {}}

    # filter only allowed periods
    periods_allowed = {'1': 1, '2': 2, '3': 3, 'P': 4}
    for team in playerstat_dic:
        if team == 'home':
            team_name = 'home_team'
        else:
            team_name = 'visitor_team'

        # build dictionary based on playerstats (this is live - hopefully)
        for period in periods_allowed:
            if period in playerstat_dic[team]:
                for player in playerstat_dic[team][period]:
                    # if player['name'] == 'Michael Moore':
                    # store values in a temporary dic as playerstats contains aggregated values only
                    if player['name'] not in tmp_toi_sum_dic[team_name]:
                        tmp_toi_sum_dic[team_name][player['name']] = 0
                    if player['statistics']['timeOnIce'] > 0:
                        toi_dic[team_name][periods_allowed[period]][player['name']] = player['statistics']['timeOnIce'] - tmp_toi_sum_dic[team_name][player['name']]
                        tmp_toi_sum_dic[team_name][player['name']] = player['statistics']['timeOnIce']
    return toi_dic

def toipppk_get(logger, _matchinfo_dic, playerstat_dic, key='name'):
    """ get timeonice for powerplay and penalty killing"""
    logger.debug('toipppk_get()')

    # inititialize dictionaries to store the data
    # toi_dic = {'home_team': {1: {}, 2: {}, 3: {}, 4: {}}, 'visitor_team': {1: {}, 2: {}, 3: {}, 4: {}}}
    toi_sum_dic = {'home_team': {}, 'visitor_team': {}}

    # filter only allowed periods
    periods_allowed = {'1': 1, '2': 2, '3': 3, 'P': 4}
    for team in playerstat_dic:
        if team == 'home':
            team_name = 'home_team'
        else:
            team_name = 'visitor_team'

        # build dictionary based on playerstats (this is live - hopefully)
        for period in periods_allowed:
            if period in playerstat_dic[team]:
                for player in playerstat_dic[team][period]:
                    # store values in a temporary dic as playerstats contains aggregated values only
                    if player['statistics']['timeOnIcePP'] > 0:
                        if player[key] not in toi_sum_dic[team_name]:
                            toi_sum_dic[team_name][player[key]] = {'pp': 0, 'pk': 0}
                        toi_sum_dic[team_name][player[key]]['pp'] = player['statistics']['timeOnIcePP']
                    if player['statistics']['timeOnIceSH'] > 0:
                        if player[key] not in toi_sum_dic[team_name]:
                            toi_sum_dic[team_name][player[key]] = {'pp': 0, 'pk': 0}
                        toi_sum_dic[team_name][player[key]]['pk'] = player['statistics']['timeOnIceSH']

    return toi_sum_dic

def matchupmatrix_get(logger, matchinfo_dic, shot_list, shift_list, roster_list, periodevent_list, five_filter=True):
    """ get player matchup - time players spend on ice together """
    logger.debug('matchupmatrix_get()')

    # shot list prepar
    shotpersec_list = shotpersecondlist_get(logger, matchinfo_dic, shot_list)

    # soi = seconds on ice
    (soi_dic, _toi_dic) = skatersonice_get(logger, shift_list, matchinfo_dic, True)

    # add penalties to filter 5v5
    soi_dic = penalties_include(logger, soi_dic, periodevent_list)

    # get lineup in a sorted way
    (lineup_dic, player_dic, plotline_dic) = lineup_sort(logger, roster_list)

    matchup_matrix = _matchupmatrix_gen(logger, shotpersec_list, soi_dic, lineup_dic, player_dic, five_filter=five_filter)

    return(lineup_dic, matchup_matrix, plotline_dic)
