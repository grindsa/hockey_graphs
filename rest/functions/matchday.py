# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.functions.match import match_list_get
from rest.functions.helper import date_to_datestr, datestr_to_date, date_to_uts_utc, url_build, uts_now
from rest.functions.season import season_latest_get

def matchdays_get(logger, request, fkey=None, fvalue=None, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team__shortcut', 'home_team__team_name', 'home_team__logo', 'visitor_team__team_name', 'visitor_team__shortcut', 'visitor_team__logo', 'result')):
    """ matches grouped by days """
    logger.debug('match_list_get({0}:{1})'.format(fkey, fvalue))

    uts = uts_now()

    if not fkey:
        # no filter has been passed, lets use season_id
        if 'season_id' in request.GET:
            try:
                fkey = 'season_id'
                fvalue = int(request.GET['season_id'])
            except:
                fkey = 'season_id'
                fvalue = season_latest_get(logger)
        else:
            fkey = 'season_id'
            fvalue = season_latest_get(logger)
    
    # reuse of an existing function from match
    match_list = match_list_get(logger, fkey, fvalue, vlist)
    matchday_dic = {}
    matchday_uts_dic = {}
    lastmday_uts = 0
    lastmday_human = ''

    # we need the url to be added to the logo URL
    if request.META:
        base_url = url_build(request.META)
    else:
        base_url = ''

    # we need to group the list by matchdays
    for match in match_list:
        dateobj = datestr_to_date(match['date'], '%Y-%m-%d')
        match_day = date_to_datestr(dateobj, '%d.%m.%Y')
        match_uts = date_to_uts_utc(match['date'], '%Y-%m-%d')

        # we need the completed matchday to set the display key to true
        if match_uts-86400 > lastmday_uts:
            if uts > match_uts:
                lastmday_uts = match_uts
                lastmday_human = match['date']

        if match['date'] not in matchday_dic:
            matchday_dic[match['date']] = {
                'date': match_day,
                'uts': match_uts,
                'matches': [],
                'displayday': False
            }
            # we need this dictionary to lookup the previous and next matchdate
            matchday_uts_dic[match_uts] = match['date']

        # rename a few keys to make the output better understandable
        match['home_team_shortcut'] = match.pop('home_team__shortcut')
        match['home_team_name'] = match.pop('home_team__team_name')
        match['home_team_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match.pop('home_team__logo'))
        match['visitor_team_shortcut'] = match.pop('visitor_team__shortcut')
        match['visitor_team_name'] = match.pop('visitor_team__team_name')
        match['visitor_team_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match.pop('visitor_team__logo'))

        matchday_dic[match['date']]['matches'].append(match)

    # set displayflag to last matchday
    matchday_dic[lastmday_human]['displayday'] = True

    # add references to previous and next matchdate
    matchday_dic = matchdays_previous_next_add(logger, matchday_dic, matchday_uts_dic)

    logger.debug('match_list_get({0}:{1}) ended with {2}'.format(fkey, fvalue, bool(match_list)))
    return matchday_dic

def matchdays_previous_next_add(logger, matchday_dic, matchday_uts_dic):
    """ add links for next and previous matches """
    logger.debug('matchdays_previous_next_add()')

    # create list of uts for faster lookup
    matchday_uts_list = sorted(matchday_uts_dic.keys())

    for matchday in matchday_dic:
        matchday_index = matchday_uts_list.index(matchday_dic[matchday]['uts'])

        if matchday_index > 0:
            # get prevevious match by looking up previous elemnet before in match_uts_list
            matchday_dic[matchday]['previous'] = matchday_uts_dic[matchday_uts_list[matchday_index-1]]

        if matchday_index < len(matchday_uts_list)-1:
            # get next match by lookup up next element in match_uts_list
            matchday_dic[matchday]['next'] = matchday_uts_dic[matchday_uts_list[matchday_index+1]]

    logger.debug('matchdays_previous_next_add() ended')
    return matchday_dic
