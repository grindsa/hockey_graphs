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
from rest.functions.player import player_add, playerperseason_add
from delapphelper import DelAppHelper
from rest.functions.season import season_latest_get

if __name__ == '__main__':

    DEBUG = True

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # season to scan
    # SEASON_YEAR_LIST = [2019, 2020]
    SEASON_YEAR_LIST = [2023]

    # league (1-regular, 3-playoff)
    # 1 - for DEL Regular season
    # 3 - for DEL Playoffs
    # 4 - for Magenta Cup
    # LEAGUE_LIST = [1, 3]
    LEAGUE_LIST = [1]

    # get list of teams
    TEAM_DIC = team_dic_get(LOGGER, None)
    SEASON_ID = season_latest_get(LOGGER)

    with DelAppHelper(DEBUG, cfg_file=os.path.dirname(__file__) + '/' + 'delapphelper.cfg') as del_app_helper:
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
                                'height': player['height'],
                                'birthdate': player['dateOfBirth'],
                                'position': player['position'],
                                'nationality': player['nationalityShort'],
                                'team_id': team_id
                            }
                            pid = player_add(LOGGER, 'player_id', player['id'], data_dic)

                            data_dic = {'player_id': player['id'], 'season_id': SEASON_ID}
                            pid = playerperseason_add(LOGGER, player['id'], SEASON_ID, data_dic)
                    except BaseException:
                        LOGGER.debug('ERROR: {0}: {1}: {2}'.format(season_year, league, team_id))
