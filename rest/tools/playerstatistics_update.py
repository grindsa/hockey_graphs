#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413, R0916, R0913
import os
import sys
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from rest.functions.corsi import gameplayercorsi_get  # nopep8
from rest.functions.faceoff import faceoff_get  # nopep8
from rest.functions.playerstatistics import playerstatistics_single_add  # nopep8
from rest.functions.helper import logger_setup, uts_now  # nopep8
from rest.functions.match import openmatch_list_get, pastmatch_list_get, sincematch_list_get, match_list_get, match_info_get  # nopep8
from rest.functions.periodevent import periodevent_get  # nopep8
from rest.functions.playerstat import playerstat_get  # nopep8
from rest.functions.roster import roster_get  # nopep8
from rest.functions.season import season_latest_get  # nopep8
from rest.functions.shift import shift_get, toifromshifts_get  # nopep8
from rest.functions.shot import shot_list_get  # nopep8


def _update_shot_data(logger, match_id_, matchinfo_dic, periodevent_list_, roster_list_, shift_list_, shot_list_):
    """ update shoot data in playerstatistics """
    logger.debug(f'_update_shot_data: {match_id_}')

    shot_dic = {}
    player_shot_dic = gameplayercorsi_get(logger, shot_list_, shift_list_, periodevent_list_, matchinfo_dic, roster_list_, five_filter=False)
    player_shot5v5_dic = gameplayercorsi_get(logger, shot_list_, shift_list_, periodevent_list_, matchinfo_dic, roster_list_, five_filter=True)

    shot_dic = {}

    # create hash
    for _team, player_dic in player_shot_dic.items():
        for player_, summary in player_dic.items():
            if not summary['player_id'] in shot_dic:
                shot_dic[summary['player_id']] = {'shot_list': []}
            shot_dic[summary['player_id']]['shots_for'] = summary['shots']
            shot_dic[summary['player_id']]['shots_against'] = summary['shots_against']
            if 'assist' in summary:
                shot_dic[summary['player_id']]['assist'] = summary['assist']
            if 'goal' in summary:
                shot_dic[summary['player_id']]['goal'] = summary['goal']

            if _team in player_shot5v5_dic and player_ in player_shot5v5_dic[_team]:
                shot_dic[summary['player_id']]['shots_for_5v5'] = player_shot5v5_dic[_team][player_]['shots']
                shot_dic[summary['player_id']]['shots_against_5v5'] = player_shot5v5_dic[_team][player_]['shots_against']

    return shot_dic


def _update_toi_data(logger, _season_id, match_id_, matchinfo_dic, shift_list_, _playerstat_dic):
    """ update toi data in playerstatistics """
    logger.debug(f'_update_toi_data: {match_id_}')

    toi_dic = {}
    # get toi
    period_toi_dic = toifromshifts_get(logger, matchinfo_dic, shift_list_, 'id')

    # aggregate tois per player
    for _team in period_toi_dic:
        if _team == 'home_team':
            team_id = matchinfo_dic['home_team_id']
            oteam_id = matchinfo_dic['visitor_team_id']
        else:
            oteam_id = matchinfo_dic['home_team_id']
            team_id = matchinfo_dic['visitor_team_id']

        for period in period_toi_dic[_team]:
            for player_id in period_toi_dic[_team][period]:
                if player_id not in toi_dic:
                    toi_dic[player_id] = {'team_id': team_id, 'oteam_id': oteam_id, 'toi': {}, 'toi_pp': 0, 'toi_pk': 0}
                toi_dic[player_id]['toi'][period] = period_toi_dic[_team][period][player_id]

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

    return debug, season, match_list, openmatches, pastmatches, interval, allmatches


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
            MATCH_LIST = sincematch_list_get(LOGGER, SEASON_ID, UTS, INTERVAL * 3600, ['match_id'])
        else:
            MATCH_LIST = match_list_get(LOGGER, 'season', SEASON_ID, ['match_id'])

    for match_id in MATCH_LIST:
        LOGGER.debug(f'processing match: {match_id}')
        # we need some match_information
        matchinfo_dic_ = match_info_get(LOGGER, match_id, None)
        playerstat_dic = playerstat_get(LOGGER, 'match', match_id, ['home', 'visitor'])
        periodevent_list = periodevent_get(LOGGER, 'match', match_id, ['period_event'])
        roster_list = roster_get(LOGGER, 'match', match_id, ['roster'])
        shift_list = shift_get(LOGGER, 'match', match_id, ['shift'])
        shot_list = shot_list_get(LOGGER, 'match', match_id, ['timestamp', 'match_shot_resutl_id', 'team_id', 'player', 'zone', 'coordinate_x', 'coordinate_y'])
        faceoff_list = faceoff_get(LOGGER, 'match', match_id, ['faceoff'])

        TOI_DIC = {}
        SHOT_DIC = {}
        if shift_list:
            # update toi
            TOI_DIC = _update_toi_data(LOGGER, SEASON_ID, match_id, matchinfo_dic_, shift_list, playerstat_dic)

        if shot_list:
            SHOT_DIC = _update_shot_data(LOGGER, match_id, matchinfo_dic_, periodevent_list, roster_list, shift_list, shot_list)

        for team in ['home', 'visitor']:
            for _period, player_list in playerstat_dic[team].items():
                for player in player_list:
                    if not player['position'] == 'GK':
                        data_dic = {
                            'match_id': match_id,
                            'player_id': player['id'],
                            'team_id': matchinfo_dic_[f'{team}_team_id'],
                            'season_id': SEASON_ID,
                            'assists': player['statistics']['assists']['away'] + player['statistics']['assists']['home'],
                            'faceoffswon': player['statistics']['faceoffsWin'],
                            'faceofflost': player['statistics']['faceoffsLosses'],
                            'games': player['statistics']['games'],
                            'goals': player['statistics']['goals']['away'] + player['statistics']['goals']['home'],
                            'penaltyminutes': player['statistics']['penaltyMinutes'],
                            'shifts': player['statistics']['shifts'],
                            'shots_ongoal': player['statistics']['shotsOnGoal']['away'] + player['statistics']['shotsOnGoal']['home'],
                            'shots': player['statistics']['shotsAttempts'],
                            'toi': player['statistics']['timeOnIce'],
                            'toi_pp': player['statistics']['timeOnIcePP'],
                            'toi_sh': player['statistics']['timeOnIceSH'],
                        }
                        if player['id'] in SHOT_DIC:
                            data_dic['shots_for'] = SHOT_DIC[player['id']]['shots_for']
                            data_dic['shots_for_5v5'] = SHOT_DIC[player['id']]['shots_for_5v5']
                            data_dic['shots_against'] = SHOT_DIC[player['id']]['shots_against']
                            data_dic['shots_against_5v5'] = SHOT_DIC[player['id']]['shots_against_5v5']

                        if player['id'] in TOI_DIC and 'toi' in TOI_DIC[player['id']]:
                            data_dic['toi_per_period'] = TOI_DIC[player['id']]['toi']
                        playerstatistics_single_add(LOGGER, SEASON_ID, player['id'], match_id, data_dic=data_dic)
