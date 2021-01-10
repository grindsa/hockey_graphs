#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" script for initial teamsmatchstat load """
import sys
import os
import argparse
import django
# we need this to load the django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
django.setup()
# pylint: disable=E0401, C0413
# import project settings
from rest.functions.helper import logger_setup, uts_now, json_load
from rest.functions.match import openmatch_list_get, pastmatch_list_get, sincematch_list_get
from rest.functions.season import season_latest_get
from rest.functions.teamstat import teamstat_get
from rest.functions.teammatchstat import teammatchstat_add

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='teampstat_load.py - update teamstats in database')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('--shifts', help='debug mode', action="store_true", default=False)
    parser.add_argument('--xgdata', help='file containing the xg model data', default=[])
    parser.add_argument('--xgweights', help='file containing the xg weights', default=[])
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
    addshifts = args.shifts
    allmatches = args.allmatches
    xg_data = args.xgdata
    xg_weights = args.xgweights
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

    if not matchlist and not allmatches and not openmatches and not pastmatches and not interval:
        print('either -a -i -o -p or --matchlist parameter must be specified')
        sys.exit(0)

    return(debug, season, match_list, addshifts, openmatches, pastmatches, interval, allmatches, xg_data, xg_weights)

if __name__ == '__main__':

    # get variables
    (DEBUG, SEASON_ID, MATCH_LIST, ADDSHIFTS, OPENMATCHES, PASTMATCHES, INTERVAL, ALLMATCHES,  XG_DATA, XG_WEIGHTS) = arg_parse()

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

    # get list of matches
    if MATCH_LIST:
        # selective update for certain matches only
        stat_list = teamstat_get(LOGGER, 'match_id', MATCH_LIST)
    else:
        # update all statistics
        stat_list = teamstat_get(LOGGER)

    XG_DATA_DIC = {}
    XG_WEIGHTS_DIC = {}
    if XG_DATA and XG_WEIGHTS:
        XG_DATA_DIC = json_load(XG_DATA)
        XG_WEIGHTS_DIC  = json_load(XG_WEIGHTS)

    for stat in stat_list:
        # get matchid and add data add function
        teammatchstat_add(LOGGER, stat, XG_DATA_DIC, XG_WEIGHTS_DIC)
