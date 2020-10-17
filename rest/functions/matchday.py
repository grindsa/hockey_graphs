# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.functions.match import match_list_get
from rest.functions.helper import date_to_datestr, datestr_to_date, date_to_uts_utc

def matchdays_get(logger, fkey=None, fvalue=None, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team__shortcut', 'visitor_team__shortcut', 'result')):
    """ matches grouped by days """
    logger.debug('match_list_get({0}:{1})'.format(fkey, fvalue))

    # reuse of an existing function from match
    match_list = match_list_get(logger, fkey, fvalue, vlist)
    matchday_dic = {}
    lastmday_uts = 0
    lastmday_human = ''

    # we need to group the list by matchdays
    for match in match_list:
        dateobj = datestr_to_date(match['date'], '%Y-%m-%d')
        match_day = date_to_datestr(dateobj, '%d.%m')
        match_uts = date_to_uts_utc(match['date'], '%Y-%m-%d')
        # we need the last matchday to set the display key to true
        if match_uts > lastmday_uts:
            lastmday_uts = match_uts
            lastmday_human = match['date']

        if match['date'] not in matchday_dic:
            matchday_dic[match['date']] = {
                'date': match_day,
                'uts': match_uts,
                'matches': [],
                'displayday': False
            }
        # rename a few keys to make the output better understandable
        match['home_team'] = match.pop('home_team__shortcut')
        match['visitor_team'] = match.pop('visitor_team__shortcut')

        matchday_dic[match['date']]['matches'].append(match)

    # set displayflag to last matchday
    matchday_dic[lastmday_human]['displayday'] = True

    logger.debug('match_list_get({0}:{1}) ended with {2}'.format(fkey, fvalue, bool(match_list)))
    return matchday_dic
