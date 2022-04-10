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
from rest.functions.season import season_latest_get, season_get
from rest.functions.helper import logger_setup, uts_now, uts_to_date_utc
from rest.functions.team import team_list_get
from rest.functions.teamstatdel import teamstatdel_add
from delapphelper import DelAppHelper

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='teampstat_load.py - update teamstats in database')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-l', '--league', help='leage id (1 - regular season, 3 - playoff)', required=True)
    args = parser.parse_args()

    # default settings
    season = 0
    # args
    debug = args.debug
    league = args.league

    return(debug, league)

if __name__ == '__main__':

    (DEBUG, LEAGUE_ID) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # unix timestamp
    UTS = uts_now()
    DATE = uts_to_date_utc(UTS)

    # get lasted seasonid and database
    SEASON_ID = season_latest_get(LOGGER)
    DELSEASON_NAME = season_get(LOGGER, 'id', SEASON_ID, ['delname'])
    TEAM_ID_LIST = team_list_get(LOGGER, None, None, ['team_id'])

    with DelAppHelper('0101030405', DEBUG) as del_app_helper:

        if SEASON_ID and DELSEASON_NAME and TEAM_ID_LIST:
            for team_id in TEAM_ID_LIST:
                try:
                    stats_dic = del_app_helper.teamstatssummary_get(DELSEASON_NAME, LEAGUE_ID, team_id)
                except BaseException:
                    stats_dic = {}
                if stats_dic:
                    result = teamstatdel_add(LOGGER, SEASON_ID, team_id, {'leagueallteamstats': stats_dic, 'stats_updated': DATE})
