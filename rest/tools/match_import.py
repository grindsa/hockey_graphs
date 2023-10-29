#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
import argparse
from rest.functions.helper import logger_setup, list2dic, uts_to_date_utc, uts_now, json_store, json_load, date_to_uts_utc
from rest.functions.match import match_add
from rest.functions.season import season_latest_get, season_get
from rest.functions.team import team_list_get
from delapphelper import DelAppHelper

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='match_import.py - update matches in database')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    tsg = parser.add_mutually_exclusive_group()
    tsg.add_argument('-s', '--season', help='hockeygraphs season id', default=None)
    tsg.add_argument('-t', '--tournament', help='del season id', default=None)
    args = parser.parse_args()

    debug = args.debug
    season = args.season
    tournament = args.tournament

    if not tournament and not season:
        print('specify either "-t" or "-s"')
        sys.exit(0)

    return(debug, season, tournament)

if __name__ == '__main__':

    # create pseudo-device for REST-API calls against mobile api
    DEVICE_ID = '00155d8aecc66666'
    LEAGUE_ID = 1

    # get commandline arguments
    (DEBUG, SEASON_ID, TOURNAMENT_ID) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    UTS_NOW = uts_now()

    if not SEASON_ID:
        # get season_id
        SEASON_ID = season_latest_get(LOGGER)

    if not TOURNAMENT_ID:
        # get tournamentid based on season_id
        TOURNAMENT_ID = season_get(LOGGER, 'id', SEASON_ID, ['tournament'])

    YEAR, _YEAR = season_get(LOGGER, 'id', SEASON_ID, ['name']).split('/', 1)


    # get team_list
    TEAM_DIC = list2dic(LOGGER, list(team_list_get(LOGGER, None, None, ['team_id', 'shortcut'])), 'shortcut')


    SEASON_GAMES_DIC = {}

    with DelAppHelper(DEBUG, cfg_file=os.path.dirname(__file__) + '/' + 'delapphelper.cfg') as del_app_helper:

        for team, team_info in TEAM_DIC.items():
            try:
                game_dic = del_app_helper.gameschedule_get(YEAR, LEAGUE_ID, team_info['team_id'])

                for match in game_dic['matches']:
                    # uts = date_to_uts_utc(match['start_date'], '%Y-%m-%d %H:%M:%S') - 7200
                    uts = date_to_uts_utc(match['start_date'], '%Y-%m-%d %H:%M:%S') - 3600
                    data_dic = {
                        'season_id': SEASON_ID,
                        'match_id': match['id'],
                        'home_team_id': match['home']['id'],
                        'visitor_team_id': match['guest']['id'],
                        'date_uts': uts,
                        'date': uts_to_date_utc(uts, '%Y-%m-%d'),
                    }

                    # if match['id'] not in SEASON_GAMES_DIC:
                    SEASON_GAMES_DIC[match['id']] = data_dic
                    #else:
                    #     print('game: {0} exists in dictionary. Ignoring...'.format(match['id']))

            except Exception:
                LOGGER.error('No schedule for team: {0}'.format(team))

    for id, match_data in SEASON_GAMES_DIC.items():

        if UTS_NOW <= match_data['date_uts']:
            (match_id, created) = match_add(LOGGER, 'match_id', id, match_data)
            if created:
                LOGGER.debug('match_created({0})'.format(match_id))
            else:
                LOGGER.debug('match_updated({0})'.format(match_id))

