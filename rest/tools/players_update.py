#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" update player information in database """
# pylint: disable=E0401, C0413
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from rest.functions.helper import logger_setup
from rest.functions.team import team_dic_get
from rest.functions.player import player_add
from delapphelper import DelAppHelper

if __name__ == '__main__':

    DEBUG = False

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # season to scan
    # SEASON_YEAR_LIST = [2019, 2020]
    SEASON_YEAR_LIST = [2020]

    # league (1-regular, 3-playoff)
    # 1 - for DEL Regular season
    # 3 - for DEL Playoffs
    # 4 - for Magenta Cup
    # LEAGUE_LIST = [1, 3]
    LEAGUE_LIST = [1]

    # get list of teams
    TEAM_DIC = team_dic_get(LOGGER, None)

    with DelAppHelper(None, DEBUG) as del_app_helper:
        for season_year in SEASON_YEAR_LIST:
            for league in LEAGUE_LIST:
                for team_id in TEAM_DIC:
                    try:
                        playerinfo_dic = del_app_helper.teamplayers_get(season_year, team_id, league)
                        for player in playerinfo_dic:
                            LOGGER.debug('{1}: {2}: {3}: update: {0}'.format(player['name'], season_year, league, team_id))
                            data_dic = {
                                'player_id': player['id'],
                                'first_name': player['firstname'],
                                'last_name': player['surname'],
                                'jersey': player['jersey'],
                                'stick': player['stick'],
                                'weight': player['weight'],
                                'height': player['height']
                            }
                            pid = player_add(LOGGER, 'player_id', player['id'], data_dic)
                    except BaseException:
                        LOGGER.debug('ERROR: {0}: {1}: {2}'.format(season_year, league, team_id))
