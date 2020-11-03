# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Playerstat
from rest.functions.timeline import skatersonice_get, penalties_include
from rest.functions.lineup import lineup_sort

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

    for team in playerstat_dic:
        print(team)
        if team == 'home':
            team_name = 'home_team'
        else:
            team_name = 'visitor_team'

        # build dictionary based on playerstats (this is live - hopefully)
        for period in sorted(playerstat_dic[team]):
            for player in playerstat_dic[team][period]:
                # store values in a temporary dic as playerstats contains aggregated values only
                if player['name'] not in tmp_toi_sum_dic:
                    tmp_toi_sum_dic[team_name][player['name']] = 0
                if player['statistics']['timeOnIce'] > 0:
                    toi_dic[team_name]['ebb'][int(period)][player['name']] = player['statistics']['timeOnIce'] - tmp_toi_sum_dic[team_name][player['name']]
                    tmp_toi_sum_dic[team_name][player['name']] = player['statistics']['timeOnIce']

    return toi_dic

def matchupmatrix_get(logger, matchinfo_dic, shift_list, roster_list, five_filter=True):
    """ get player matchup - time players spend on ice together """
    logger.debug('matchupmatrix_get()')

    # soi = seconds on ice
    (soi_dic, toi_dic) = skatersonice_get(logger, shift_list, matchinfo_dic)

    # get lineup in a sorted way
    lineup_dic = lineup_sort(logger, roster_list)

    # get playerstat dic
    # playerstat_dic = playerstat_get(logger, 'match_id', )
