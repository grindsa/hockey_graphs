#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import os
import sys
import time
from datetime import datetime
from pytz import timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from rest.functions.helper import logger_setup, uts_now
from rest.functions.matchday import matchdays_get
from rest.functions.season import season_latest_get
from rest.functions.shift import shift_add
from delapphelper import DelAppHelper

# from wa_hack_cli import simple_send
TIMEZONE = timezone('Europe/Berlin')

def value_from_list_filter(logger, in_list, value):
    """ filter a certain value from list """
    logger.debug('value_from_list_filter({0})'.format(value))
    out_list = []
    for ele in in_list:
        out_list.append(ele[value])

    return out_list

if __name__ == '__main__':

    DEBUG = True

    # initialize logger
    LOGGER = logger_setup(DEBUG)
    # get season_id
    SEASON_ID = season_latest_get(LOGGER)
    # unix timestamp
    UTS = uts_now()

    # unix timestamp
    uts_now = int(time.time())

    # get matches of the day
    # print('today manipuliert')
    # TODAY = '2020-11-15'
    TODAY = datetime.fromtimestamp(uts_now, tz=TIMEZONE).strftime("%Y-%m-%d")

    # Get list of matches to be updated and compile a list of corresponding match_ids as this is input for the update loop
    matchday_list = matchdays_get(LOGGER, None, 'date', TODAY)
    matchid_list = []
    if matchday_list:
        if TODAY in matchday_list and 'matches' in matchday_list[TODAY]:
            matchid_list = value_from_list_filter(LOGGER, matchday_list[TODAY]['matches'], 'match_id')

    with DelAppHelper(None, DEBUG) as del_app_helper:
        for match_id in matchid_list:
            # get shifts and update db
            shift_dic = del_app_helper.shifts_get(match_id)
            shift_add(LOGGER, 'match_id', match_id, {'match_id': match_id, 'shift': shift_dic})
