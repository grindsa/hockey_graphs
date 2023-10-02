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
        playerstat_dic[str(match_id)] = player_dic[player_id]

        # _result = playerstatistics_single_add(logger, season_id, player_id, {'faceoff': playerstat_dic})
        output_dic[player_id] = {'faceoff': playerstat_dic}

    return output_dic

def _update_shot_data(logger, season_id, match_id, matchinfo_dic, periodevent_list, roster_list, shift_list, shot_list):
    """ update shoot data in playerstatistics """
    logger.debug('_update_shot_data: {0}'.format(match_id))

    shot_dic = {}
    player_shot_dic = gameplayercorsi_get(logger, shot_list, shift_list, periodevent_list, matchinfo_dic, roster_list, five_filter=False)
    player_shot5v5_dic = gameplayercorsi_get(logger, shot_list, shift_list, periodevent_list, matchinfo_dic, roster_list, five_filter=True)

    shot_dic = {}

    # create hash
    for team, player_dic in player_shot_dic.items():
        for player, summary in player_dic.items():
            if not summary['player_id'] in shot_dic:
                shot_dic[summary['player_id']] = {'shot_list': []}
            shot_dic[summary['player_id']]['shots_for'] = summary['shots']
            shot_dic[summary['player_id']]['shots_against'] = summary['shots_against']
            if 'assist' in summary:
                shot_dic[summary['player_id']]['assist'] = summary['assist']
            if 'goal' in summary:
                shot_dic[summary['player_id']]['goal'] = summary['goal']

            if team in player_shot5v5_dic and player in player_shot5v5_dic[team]:
                shot_dic[summary['player_id']]['shots_for_5v5'] = player_shot5v5_dic[team][player]['shots']
                shot_dic[summary['player_id']]['shots_against_5v5'] = player_shot5v5_dic[team][player]['shots_against']

    return shot_dic


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
    #toipppk_dic = toipppk_get(logger, matchinfo_dic, playerstat_dic, 'id')
    #for team in toipppk_dic:
    #    for player_id in toipppk_dic[team]:
    #        toi_dic[player_id]['toi_pk'] = toipppk_dic[team][player_id]['pk']
    #        toi_dic[player_id]['toi_pp'] = toipppk_dic[team][player_id]['pp']


    return toi_dic


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
        shot_list = shot_list_get(LOGGER, 'match', match_id, ['timestamp', 'match_shot_resutl_id', 'team_id', 'player', 'zone', 'coordinate_x', 'coordinate_y'])
        faceoff_list = faceoff_get(LOGGER, 'match', match_id, ['faceoff'])

        toi_dic = {}
        shot_dic = {}
        if shift_list:
            # update toi
            toi_dic = _update_toi_data(LOGGER, SEASON_ID, match_id, matchinfo_dic, shift_list, playerstat_dic)

        if shot_list:
            shot_dic =  _update_shot_data(LOGGER, SEASON_ID, match_id, matchinfo_dic, periodevent_list, roster_list, shift_list, shot_list)

        for team in ['home', 'visitor']:
            # print(matchinfo_dic)
            for period, player_list in playerstat_dic[team].items():
                for player in player_list:
                    if not player['position'] == 'GK':
                        data_dic = {
                            'match_id': match_id,
                            'player_id': player['id'],
                            'team_id': matchinfo_dic[f'{team}_team_id'],
                            'season_id': SEASON_ID,
                            'assists':  player['statistics']['assists']['away'] + player['statistics']['assists']['home'],
                            'faceoffswon':  player['statistics']['faceoffsWin'],
                            'faceofflost':  player['statistics']['faceoffsLosses'],
                            'games':  player['statistics']['games'],
                            'goals':  player['statistics']['goals']['away'] + player['statistics']['goals']['home'],
                            'penaltyminutes':  player['statistics']['penaltyMinutes'],
                            'shifts': player['statistics']['shifts'],
                            'shots_ongoal':  player['statistics']['shotsOnGoal']['away'] + player['statistics']['shotsOnGoal']['home'],
                            'shots': player['statistics']['shotsAttempts'],
                            'toi': player['statistics']['timeOnIce'],
                            'toi_pp': player['statistics']['timeOnIcePP'],
                            'toi_sh': player['statistics']['timeOnIceSH'],
                        }
                        if player['id'] in shot_dic:
                            data_dic['shots_for'] = shot_dic[player['id']]['shots_for']
                            data_dic['shots_for_5v5'] = shot_dic[player['id']]['shots_for_5v5']
                            data_dic['shots_against'] = shot_dic[player['id']]['shots_against']
                            data_dic['shots_against_5v5'] = shot_dic[player['id']]['shots_against_5v5']

                        if player['id'] in toi_dic and 'toi' in toi_dic[player['id']]:
                            data_dic['toi_per_period'] = toi_dic[player['id']]['toi']
                        playerstatistics_single_add(LOGGER, SEASON_ID, player['id'], data_dic=data_dic)


        #    # update shots
        #shot_dic =  _update_shot_data(LOGGER, SEASON_ID, match_id, matchinfo_dic, periodevent_list, roster_list, shift_list, shot_list)
        # pprint(shot_dic)


       # if faceoff_list:
       #     faceoff_dic = _update_faceoff_data(LOGGER, SEASON_ID, match_id, faceoff_list)


        #for player_id in toi_dic:
        #    if player_id in faceoff_dic:
        #        toi_dic[player_id].update(faceoff_dic[player_id])
        #    if player_id in shot_dic:
        #        toi_dic[player_id].update(shot_dic[player_id])


        # update database
        #for player_id, data_dic in toi_dic.items():
        #