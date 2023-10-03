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
from rest.functions.player import u23_player_list_get

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

def playerstatistics_get(logger, fkey=None, fvalue=None, vlist=('season_id', 'match_id', 'player_id', 'player__first_name', 'player__last_name', 'player__team__shortcut', 'shots', 'goals', 'toi', 'toi_per_period', 'toi_pp', 'toi_sh', 'line')):
    """ query player(s) from database based with optional filtering """
    logger.debug('playerstatistics_get({0})'.format(fkey))
    try:
        if fkey:
            if len(vlist) == 1:
                player_list = Playerstatistics.objects.filter(**{fkey: fvalue}).order_by('player_id').values_list(vlist[0], flat=True)
            else:
                player_list = Playerstatistics.objects.filter(**{fkey: fvalue}).order_by('player_id').values(*vlist)
        else:
            if len(vlist) == 1:
                player_list = Playerstatistics.objects.all().order_by('player_id').values_list(vlist[0], flat=True)
            else:
                player_list = Playerstatistics.objects.all().order_by('player_id').values(*vlist)
    except BaseException as err_:
        logger.critical('playerstatistics_get in player_list_get(): {0}'.format(err_))
        player_list = []
    return list(player_list)

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

def u23_toi_get(logger, season_id, teams_dic):
    """get u23 to data """
    logger.debug('u23_toi_get()')

    u23_player_dic = u23_player_list_get(logger, season_id=season_id)
    u23_player_list = list(u23_player_dic.keys())
    player_match_list = playerstatistics_get(logger, 'player__in', u23_player_list, vlist=('season_id', 'match_id', 'player_id', 'player__first_name', 'player__last_name', 'player__nationality', 'player__team_id', 'player__team__shortcut', 'player__jersey', 'shifts', 'toi', 'toi_per_period', 'toi_pp', 'toi_sh', 'line'))

    # aggregate data
    playerstat_dic = {}
    for pmatch in player_match_list:
        # if pmatch['toi_per_period']:
        if pmatch['toi'] and pmatch['player__nationality'] == 'GER':
            # fix inconsitenceies
            #if pmatch['toi'] == 0:
            #    for period, value in pmatch['toi_per_period'].items():
            #        pmatch['toi'] += value

            if pmatch['player_id'] not in playerstat_dic:
                playerstat_dic[pmatch['player_id']] = {'player_id': pmatch['player_id'], 'first_name': pmatch['player__first_name'], 'games': 0, 'last_name': pmatch['player__last_name'], 'shifts': 0, 'toi': 0, 'toi_pp': 0, 'toi_sh': 0, 'toi_per_period': {'1': 0, '2': 0, '3': 0, '4': 0}, 'line': []}
            playerstat_dic[pmatch['player_id']]['team_shortcut'] = pmatch['player__team__shortcut']
            playerstat_dic[pmatch['player_id']]['team_logo'] = teams_dic[pmatch['player__team_id']]['team_logo']
            playerstat_dic[pmatch['player_id']]['team_id'] = pmatch['player__team_id']
            playerstat_dic[pmatch['player_id']]['jersey'] = pmatch['player__jersey']
            playerstat_dic[pmatch['player_id']]['games'] += 1
            playerstat_dic[pmatch['player_id']]['shifts'] += pmatch['shifts']
            playerstat_dic[pmatch['player_id']]['toi'] += pmatch['toi']
            playerstat_dic[pmatch['player_id']]['toi_pp'] += pmatch['toi_pp']
            playerstat_dic[pmatch['player_id']]['toi_sh'] += pmatch['toi_sh']
            playerstat_dic[pmatch['player_id']]['line'].append(pmatch['line'])
            for period, value in pmatch['toi_per_period'].items():
                playerstat_dic[pmatch['player_id']]['toi_per_period'][period] += value

    # calulate *per games*
    for player_id in playerstat_dic:
        playerstat_dic[player_id]['shifts_pg'] = round(playerstat_dic[player_id]['shifts']/playerstat_dic[player_id]['games'], 0)
        playerstat_dic[player_id]['toi_pg'] = round(playerstat_dic[player_id]['toi']/playerstat_dic[player_id]['games'], 0)
        playerstat_dic[player_id]['toi_pp_pg'] = round(playerstat_dic[player_id]['toi_pp']/playerstat_dic[player_id]['games'], 0)
        playerstat_dic[player_id]['toi_sh_pg'] = round(playerstat_dic[player_id]['toi_sh']/playerstat_dic[player_id]['games'], 0)
        playerstat_dic[player_id]['toi_per_period_pg'] = {}
        for period, value in playerstat_dic[player_id]['toi_per_period'].items():
            playerstat_dic[player_id]['toi_per_period_pg'][period] = round(value/playerstat_dic[player_id]['games'], 0)

    return playerstat_dic
