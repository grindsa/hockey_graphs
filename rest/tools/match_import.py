#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../../')
from rest.functions.helper import logger_setup, list2dic, uts_to_date_utc
from rest.functions.match import match_add
from rest.functions.season import season_latest_get
from rest.functions.team import team_list_get
from delapphelper import DelAppHelper

if __name__ == '__main__':

    DEBUG = True
    DEVICE_ID = '00155d8aecc66666'

    # 62 - Mangenta SportCup 2020
    TOURNAMENT_ID = 62

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # get season_id
    SEASON_ID = season_latest_get(LOGGER)

    # get team_list
    TEAM_DIC = list2dic(LOGGER, list(team_list_get(LOGGER, None, None, ['team_id', 'shortcut'])), 'shortcut')


    with DelAppHelper(DEVICE_ID, DEBUG) as del_app_helper:
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
