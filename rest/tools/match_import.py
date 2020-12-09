#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
import argparse
from rest.functions.helper import logger_setup, list2dic, uts_to_date_utc
from rest.functions.match import match_add
from rest.functions.season import season_latest_get
from rest.functions.team import team_list_get
from delapphelper import DelAppHelper

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='match_import.py - update matches in database')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true")
    tsg = parser.add_mutually_exclusive_group()
    tsg.add_argument('-s', '--season', help='hockeygraphs season id')
    tsg.add_argument('-t', '--tournament', help='del season id')
    args = parser.parse_args()
    # default settings
    debug = False
    season = 0
    tournament = 0
    if args.debug:
        debug = args.debug
    if args.season:
        season = args.season
    if args.tournament:
        tournament = args.tournament

    if not tournament and not season:
        print('specify either "-t" or "-s"')
        sys.exit(0)

    return(debug, season, tournament)


if __name__ == '__main__':

    # create pseudo-device for REST-API calls against mobile api
    DEVICE_ID = '00155d8aecc66666'

    # get commandline arguments
    (DEBUG, SEASON_ID, TOURNAMENT_ID) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    if not SEASON_ID:
        # get season_id
        SEASON_ID = season_latest_get(LOGGER)

    # get team_list
    TEAM_DIC = list2dic(LOGGER, list(team_list_get(LOGGER, None, None, ['team_id', 'shortcut'])), 'shortcut')

    with DelAppHelper(DEVICE_ID, DEBUG) as del_app_helper:
        # get matches for a season
        game_dic = del_app_helper.games_get(TOURNAMENT_ID)
        for match in game_dic:
            if match['homeTeam'] in TEAM_DIC and match['guestTeam'] in TEAM_DIC:
                data_dic = {
                    'home_team_id': TEAM_DIC[match['homeTeam']]['team_id'],
                    'visitor_team_id': TEAM_DIC[match['guestTeam']]['team_id'],
                    'date_uts': match['dateTime'],
                    'date': uts_to_date_utc(match['dateTime'], '%Y-%m-%d'),
                    'season_id': SEASON_ID,
                    'match_id': match['gameNumber']
                }
                (match_id, created) = match_add(LOGGER, 'match_id', match['gameNumber'], data_dic)
                if created:
                    LOGGER.debug('match_created({0})'.format(match_id))
                else:
                    LOGGER.debug('match_updated({0})'.format(match_id))
