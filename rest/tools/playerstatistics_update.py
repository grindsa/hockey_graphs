#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import os
import sys
import pathlib
import argparse
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from rest.functions.corsi import gameplayercorsi_get
from rest.functions.faceoff import faceoff_get, faceoff_per_player_sort
from rest.functions.playerstatistics import playerstatistics_single_get, playerstatistics_single_add
from rest.functions.helper import logger_setup, uts_now
from rest.functions.match import openmatch_list_get, pastmatch_list_get, sincematch_list_get, match_list_get, match_info_get
from rest.functions.periodevent import periodevent_get
from rest.functions.playerstat import playerstat_get, playerstatistics_add, toipppk_get
from rest.functions.roster import roster_get
from rest.functions.season import season_latest_get
from rest.functions.shift import shift_get, toifromshifts_get, shiftsperplayer_get
from rest.functions.shot import shot_list_get

def _update_faceoff_data(logger, season_id, match_id, faceoff_list, ):
    """ update faceoff data"""

    output_dic = {}
    # build dictionary container faceoff results per player(id)
    player_dic = faceoff_per_player_sort(logger, faceoff_list)

    for player_id in player_dic:
        playerstat_dic = playerstatistics_single_get(logger, season_id, player_id, ['faceoff'])
        playerstat_dic[match_id] = player_dic[player_id]

        # _result = playerstatistics_single_add(logger, season_id, player_id, {'faceoff': playerstat_dic})
        output_dic[player_id] = {'faceoff': playerstat_dic}

    return output_dic

def _update_shot_data(logger, match_id, matchinfo_dic, periodevent_list, roster_list, shift_list, shot_list):
    """ update shoot data in playerstatistics """
    logger.debug('_update_shot_data: {0}'.format(match_id))

    shot_dic = {}
    player_shot_dic = gameplayercorsi_get(logger, shot_list, shift_list, periodevent_list, matchinfo_dic, roster_list, five_filter=False)
    player_shot5v5_dic = gameplayercorsi_get(logger, shot_list, shift_list, periodevent_list, matchinfo_dic, roster_list, five_filter=True)

    _avg_dic = {}

    output_dic = {}
    for team in player_shot_dic:

        if team == 'home_team':
            team_id = matchinfo_dic['home_team_id']
            oteam_id = matchinfo_dic['visitor_team_id']
        else:
            oteam_id = matchinfo_dic['home_team_id']
            team_id = matchinfo_dic['visitor_team_id']

        if team not in _avg_dic:
            _avg_dic[team] = {'shots_for': 0, 'shots_against': 0, 'shots_for_5v5': 0, 'shots_against_5v5': 0, 'cnt': 0}

        for player in player_shot_dic[team]:
            if player_shot_dic[team][player]['player_id'] not in shot_dic:
                shot_dic[player_shot_dic[team][player]['player_id']] = {'team_id': team_id, 'oteam_id': oteam_id}

            shot_dic[player_shot_dic[team][player]['player_id']]['shots_for'] =  player_shot_dic[team][player]['shots']
            shot_dic[player_shot_dic[team][player]['player_id']]['shots_against'] = player_shot_dic[team][player]['shots_against']
            shot_dic[player_shot_dic[team][player]['player_id']]['shots_for_5v5'] = player_shot5v5_dic[team][player]['shots']
            shot_dic[player_shot_dic[team][player]['player_id']]['shots_against_5v5'] = player_shot5v5_dic[team][player]['shots_against']

            # count sums
            _avg_dic[team]['cnt'] += 1
            _avg_dic[team]['shots_for'] += player_shot_dic[team][player]['shots']
            _avg_dic[team]['shots_against'] += player_shot_dic[team][player]['shots_against']
            _avg_dic[team]['shots_for_5v5'] += player_shot5v5_dic[team][player]['shots']
            _avg_dic[team]['shots_against_5v5'] += player_shot5v5_dic[team][player]['shots_against']

    for team in player_shot_dic:
        for player in player_shot_dic[team]:
            shot_dic[player_shot_dic[team][player]['player_id']]['shots_for_avg'] = round(_avg_dic[team]['shots_for']/_avg_dic[team]['cnt'], 2)
            shot_dic[player_shot_dic[team][player]['player_id']]['shots_against_avg'] = round(_avg_dic[team]['shots_against']/_avg_dic[team]['cnt'], 2)
            shot_dic[player_shot_dic[team][player]['player_id']]['shots_for_5v5_avg'] = round(_avg_dic[team]['shots_for_5v5']/_avg_dic[team]['cnt'], 2)
            shot_dic[player_shot_dic[team][player]['player_id']]['shots_against_5v5_avg'] = round(_avg_dic[team]['shots_against_5v5']/_avg_dic[team]['cnt'], 2)

    for player_id in shot_dic:
        playerstatistics_add(logger, match_id, player_id, shot_dic[player_id])

def _update_toi_data(logger, season_id, match_id, matchinfo_dic, shift_list, playerstat_dic):
    """ update toi data in playerstatistics """
    logger.debug('_update_toi_data: {0}'.format(match_id))

    toi_dic = {}
    output_dic = {}
    # get toi
    period_toi_dic = toifromshifts_get(logger, matchinfo_dic, shift_list, 'id')

    # aggregate tois per player
    for team in period_toi_dic:
        if team == 'home_team':
            team_id = matchinfo_dic['home_team_id']
            oteam_id = matchinfo_dic['visitor_team_id']
        else:
            oteam_id = matchinfo_dic['home_team_id']
            team_id = matchinfo_dic['visitor_team_id']#

        for period in period_toi_dic[team]:
            for player_id in period_toi_dic[team][period]:
                if player_id not in toi_dic:
                    toi_dic[player_id] = {'team_id': team_id, 'oteam_id': oteam_id, 'toi': {}, 'toi_pp': 0, 'toi_pk': 0}
                toi_dic[player_id]['toi'][period] = period_toi_dic[team][period][player_id]


    # add toi_pp and toi_sh
    toipppk_dic = toipppk_get(logger, matchinfo_dic, playerstat_dic, 'id')
    for team in toipppk_dic:
        for player_id in toipppk_dic[team]:
            toi_dic[player_id]['toi_pk'] = toipppk_dic[team][player_id]['pk']
            toi_dic[player_id]['toi_pp'] = toipppk_dic[team][player_id]['pp']

    for player_id in toi_dic:
        playerstat_dic = playerstatistics_single_get(logger, season_id, player_id, ['toi'])
        playerstat_dic[match_id] = toi_dic[player_id]

        output_dic[player_id] = {'toi': playerstat_dic}

    return output_dic


def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='teampstat_load.py - update teamstats in database')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    mlist = parser.add_mutually_exclusive_group()
    mlist.add_argument('-s', '--season', help='season id', default=None)
    mlist.add_argument('--matchlist', help='list of del matchids', default=[])
    mlist.add_argument('-a', '--allmatches', help='open matches from latest season', action="store_true", default=False)
    mlist.add_argument('-o', '--openmatches', help='open matches from latest season', action="store_true", default=False)
    mlist.add_argument('-p', '--pastmatches', help='previous matches from latest season', action="store_true", default=False)
    mlist.add_argument('-i', '--interval', help='previous matches during last x hours', default=0)
    args = parser.parse_args()

    # default settings
    season = 0
    matchlist = None

    debug = args.debug
    allmatches = args.allmatches
    openmatches = args.openmatches
    pastmatches = args.pastmatches
    season = args.season
    matchlist = args.matchlist
    interval = int(args.interval)

    # process matchlist
    try:
        _tmp_list = matchlist.split(',')
    except BaseException:
        _tmp_list = []
    match_list = []
    for match in _tmp_list:
        match_list.append(int(match))

    if not matchlist and not allmatches and not openmatches and not pastmatches and not interval and not season:
        print('either -a -i -o -p or --matchlist parameter must be specified')
        sys.exit(0)

    return(debug, season, match_list, openmatches, pastmatches, interval, allmatches)

if __name__ == '__main__':

    (DEBUG, SEASON_ID, MATCH_LIST, OPENMATCHES, PASTMATCHES, INTERVAL, ALLMATCHES) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # unix timestamp
    UTS = uts_now()

    if not SEASON_ID:
        # get season_id
        SEASON_ID = season_latest_get(LOGGER)

    if not MATCH_LIST:
        if ALLMATCHES:
            MATCH_LIST = []
        elif OPENMATCHES:
            # Get list of matches to be updated (selection current season, status finish_false, date lt_uts)
            MATCH_LIST = openmatch_list_get(LOGGER, SEASON_ID, UTS, ['match_id'])
        elif PASTMATCHES:
            MATCH_LIST = pastmatch_list_get(LOGGER, SEASON_ID, UTS, ['match_id'])
        elif INTERVAL:
            MATCH_LIST = sincematch_list_get(LOGGER, SEASON_ID, UTS, INTERVAL*3600, ['match_id'], )
        else:
            MATCH_LIST = match_list_get(LOGGER, 'season', SEASON_ID, ['match_id'])

    for match_id in MATCH_LIST:
        LOGGER.debug('processing match: {0}'.format(match_id))

        # we need some match_information
        matchinfo_dic = match_info_get(LOGGER, match_id, None)
        playerstat_dic = playerstat_get(LOGGER, 'match', match_id, ['home', 'visitor'])
        periodevent_list = periodevent_get(LOGGER, 'match', match_id, ['period_event'])
        roster_list = roster_get(LOGGER, 'match', match_id, ['roster'])
        shift_list = shift_get(LOGGER, 'match', match_id, ['shift'])
        shot_list = shot_list_get(LOGGER, 'match', match_id, ['timestamp', 'match_shot_resutl_id', 'real_date', 'team_id', 'player__first_name', 'player__last_name', 'zone', 'coordinate_x', 'coordinate_y', 'player__jersey'])
        faceoff_list = faceoff_get(LOGGER, 'match', match_id, ['faceoff'])

        if shift_list:
            # update toi
            toi_dic = _update_toi_data(LOGGER, SEASON_ID, match_id, matchinfo_dic, shift_list, playerstat_dic)
            # update shots
            # _update_shot_data(LOGGER, match_id, matchinfo_dic, periodevent_list, roster_list, shift_list, shot_list)

        if faceoff_list:
            faceoff_dic = _update_faceoff_data(LOGGER, SEASON_ID, match_id, faceoff_list)


        final_dic = {**toi_dic, **faceoff_dic}
        from pprint import pprint
        pprint(final_dic)