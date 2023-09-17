#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import os
import sys
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from delapphelper import DelAppHelper
from rest.functions.season import season_get, season_latest_get
from rest.functions.helper import logger_setup, uts_now, uts_to_date_utc, age_calculate, datestr_to_date, deviation_avg_get, position_get, region_get
from rest.functions.team import team_list_get
from rest.functions.teamstatdel import teamstatdel_add, teamstatdel_get


def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='teampstat_load.py - update teamstats in database')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-l', '--league', help='leage id (1 - regular season, 3 - playoff)', required=True)
    args = parser.parse_args()

    # args
    debug = args.debug
    league = args.league

    return (debug, league)


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

    TEAM_ID_LIST = teamstatdel_get(LOGGER, SEASON_ID, None, vlist=['team'])
    # Fall back for first meach in season
    if not TEAM_ID_LIST:
        LOGGER.debug('no team list in teamstat_del table query all teams we have...')
        TEAM_ID_LIST = team_list_get(LOGGER, None, None, ['team_id'])

    with DelAppHelper('0101030405', DEBUG) as del_app_helper:

        if SEASON_ID and DELSEASON_NAME and TEAM_ID_LIST:
            for team_id in TEAM_ID_LIST:
                try:
                    playerinfo_dic = del_app_helper.teamplayers_get(DELSEASON_NAME, team_id, LEAGUE_ID)
                except Exception as err_:
                    LOGGER.error('del_app_helper.teamplayers_get(): {0}'.format(err_))
                age_dic = {'ALL': []}
                region_dic = {}
                for player in playerinfo_dic:
                    age = age_calculate(datestr_to_date(player['dateOfBirth'], tformat='%Y-%m-%d'))
                    position = position_get(LOGGER, player['position'])
                    region = region_get(LOGGER, player['nationalityShort'])
                    if region not in region_dic:
                        region_dic[region] = {}
                    if age not in region_dic[region]:
                        region_dic[region][age] = 1
                    else:
                        region_dic[region][age] += 1

                    if position not in age_dic:
                        age_dic[position] = []

                    mydict = {
                        'age': age,
                    }
                    age_dic[position].append(mydict)
                    age_dic['ALL'].append(mydict)

                agestat_dic = {'position': {}, 'region': region_dic}
                for position, age_list in age_dic.items():
                    agestat_dic['position'][position] = deviation_avg_get(LOGGER, age_list, ['age'])
                try:
                    stats_dic = del_app_helper.teamstatssummary_get(DELSEASON_NAME, LEAGUE_ID, team_id)
                except BaseException:
                    stats_dic = {}
                if stats_dic:
                    result = teamstatdel_add(LOGGER, SEASON_ID, team_id, {'leagueallteamstats': stats_dic, 'agestats': agestat_dic, 'stats_updated': DATE})
