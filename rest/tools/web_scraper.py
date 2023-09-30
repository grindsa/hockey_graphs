#!/usr/bin/python3
""" webstat scrper and parser """
# -*- coding: utf-8 -*-
import os
import sys
import argparse
from delstats import DelStats
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
# import project settings
# pylint: disable=C0413
# from django.conf import settings
# pylint: disable=E0401, C0413
from rest.functions.helper import logger_setup, uts_now, uts_to_date_utc, list2dic, json_store # , json_load  # nopep8
from rest.functions.match import match_info_get, sincematch_list_get  # nopep8
from rest.functions.season import season_latest_get  # nopep8
from rest.functions.team import team_list_get  # nopep8
from rest.functions.teamstatdel import teamstatdel_add, teamstatdel_get  # nopep8
from rest.functions.teammatchstat import teammatchstatistics_add  # nopep8


def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='web_scraper.py - webstat scrper and parser')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-f', '--force', help='force mode', action="store_true", default=False)
    parser.add_argument('-s', '--season', help='season id', default=None)
    mlist = parser.add_mutually_exclusive_group()
    mlist.add_argument('--matchlist', help='list of del matchids', default=[])
    mlist.add_argument('-i', '--interval', help='previous matches during last x hours', default=0)
    parser.add_argument('--save', help='store json report', default=None)
    args = parser.parse_args()

    # default settings
    season = 0
    matchlist = None

    debug = args.debug
    season = args.season
    matchlist = args.matchlist
    interval = int(args.interval)
    force = args.force
    save_path = args.save

    # process matchlist
    try:
        _tmp_list = matchlist.split(',')
    except BaseException:
        _tmp_list = []
    match_list = []
    for match in _tmp_list:
        match_list.append(int(match))

    if not interval and not match_list:
        print('either -i or --matchlist parameter must be specified')
        sys.exit(0)

    return debug, season, match_list, interval, force, save_path


def delsite_scrap(debug, logger, team_dic):
    """ scrap del website and format output """
    logger.debug('delsite_scrap()')

    stat_dic = {}
    with DelStats(debug=debug) as delstats:
        teamstats = delstats.teamstats()
        # _stat_dic = json_load('c://temp//teamstats-2023-09-18.json')
        _stat_dic = teamstats.all()
        for team_name, team_stats in _stat_dic.items():
            if team_name:
                stat_dic[team_dic[team_name]['team_id']] = team_stats
                stat_dic[team_dic[team_name]['team_id']]['team_name'] = team_name
    return stat_dic


def value_modify(logger, category, field, value):
    """ modify value """

    if category == 'puckbesitz' and field == 'Dauer':
        logger.debug(f'value_modify({category}/{field})/{value}')
        hour, min_, sec = value.split(':', 2)
        result = int(hour) * 3600 + int(min_) * 60 + int(sec)
    else:
        result = value

    return result


def _fieldvalue_get(logger, category, field, db_dic, web_dic):
    logger.debug(f'fieldvalue_get({category}, {field}')

    if category in db_dic and field in db_dic[category]:
        logger.debug(f'fieldvalue_get({category}, {field} exists')
        result = value_modify(logger, category, field, web_dic[category][field]['value']) - value_modify(logger, category, field, db_dic[category][field]['value'])
    else:
        result = value_modify(logger, category, field, web_dic[category][field]['value'])

    return result


def check_newmatch(logger, db_dic, web_dic):
    """ check if we ever saw these stats """
    logger.debug('check_newmatch()')

    new_match = False

    if db_dic:
        if 'zuschauer' in web_dic and 'Spiele' in web_dic['zuschauer'] and 'zuschauer' in db_dic and 'Spiele' in db_dic['zuschauer']:
            if web_dic['zuschauer']['Spiele']['value'] != db_dic['zuschauer']['Spiele']['value']:
                new_match = True
        else:
            new_match = True
    else:
        # emtpy db new match
        new_match = True

    logger.debug(f'check_newmatch() ended with: {new_match}')
    return new_match


def matchstats_get(logger, force, db_dic, web_dic):
    """ get stats per match """
    logger.debug('matchstats_get()')

    fielsofinterest_dic = {
        'paesse': {'Erfolgreich': 'passes_successful', 'Gesamt': 'passes_total'},
        'defensive': {'PCW': 'pcw', 'PCL': 'pcl'},
        'puckbesitz': {'Dauer': 'puck_possession', 'DIST': 'dist', 'Control DIST': 'control_dist', 'Control DIST FWD': 'control_dist_fw'}
    }

    # check if it is a new match
    if force:
        new_match = force
    else:
        new_match = check_newmatch(logger, db_dic, web_dic)

    output_dic = {}
    if new_match:
        for category, field_dic in fielsofinterest_dic.items():
            for field, field_name in field_dic.items():
                output_dic[field_name] = _fieldvalue_get(logger, category, field, db_dic, web_dic)

    return output_dic


if __name__ == '__main__':

    (DEBUG, SEASON_ID, MATCH_ID_LIST, INTERVAL, FORCE, SAVE_PATH) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    UTS_NOW = uts_now()
    DATE = uts_to_date_utc(UTS_NOW)

    if not SEASON_ID:
        # get season_id
        SEASON_ID = season_latest_get(LOGGER)

    if not MATCH_ID_LIST:
        if INTERVAL:
            MATCH_ID_LIST = sincematch_list_get(LOGGER, SEASON_ID, UTS_NOW, INTERVAL*3600, ['match_id'], )

    # get team_list
    TEAM_DIC = list2dic(LOGGER, list(team_list_get(LOGGER, None, None, ['team_id', 'team_name'])), 'team_name')

    DELWEBSTAT_DIC = delsite_scrap(DEBUG, LOGGER, TEAM_DIC)

    if SAVE_PATH:
        SAVE_DATE = uts_to_date_utc(UTS_NOW, '%Y-%m-%d')
        json_store(file_name_=f'{SAVE_PATH}\webscrap-teamstats{SAVE_DATE}.json', data_=DELWEBSTAT_DIC)

    for match_id in MATCH_ID_LIST:
        matchinfo_dic = match_info_get(LOGGER, match_id, None, ['result_suffix', 'result', 'home_team_id', 'home_team__shortcut', 'visitor_team_id', 'visitor_team__shortcut'])

        team_list = [matchinfo_dic['home_team_id'], matchinfo_dic['visitor_team_id']]

        for team_id in team_list:
            teamstat_list = teamstatdel_get(LOGGER, SEASON_ID, team_id, ['delwebstats'])
            delstat_dic = matchstats_get(LOGGER, FORCE, teamstat_list[-1], DELWEBSTAT_DIC[team_id])

            if delstat_dic:
                # add matchstats
                _id = teammatchstatistics_add(LOGGER, match_id, team_id, delstat_dic)
                # store originial values for tracking
                _id = teamstatdel_add(LOGGER, SEASON_ID, team_id, {'delwebstats': DELWEBSTAT_DIC[team_id], 'delwebstats_updated': DATE})
