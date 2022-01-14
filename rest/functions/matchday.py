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

def _seasonid_get(logger, request):
    logger.debug('_seasonid_get()')
    # no filter has been passed, lets use season_id
    if 'season' in request.GET:
        try:
            fkey = 'season_id'
            fvalue = int(request.GET['season'])
        except BaseException:
            fkey = 'season_id'
            fvalue = season_latest_get(logger)
    else:
        fkey = 'season_id'
        fvalue = season_latest_get(logger)
    logger.debug('_seasonid_get() ended with: {0}'.format(fvalue))
    return (fkey, fvalue)

def matchdays_get(logger, request, fkey=None, fvalue=None, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team__shortcut', 'home_team__team_name', 'home_team__logo', 'visitor_team__team_name', 'visitor_team__shortcut', 'visitor_team__logo', 'result', 'finish')):
    """ matches grouped by days """
    logger.debug('matchdays_get({0}:{1})'.format(fkey, fvalue))

    if not fkey:
        (fkey, fvalue) = _seasonid_get(logger, request)

    # reuse of an existing function from match
    match_list = match_list_get(logger, fkey, fvalue, vlist)

    matchday_dic = {}
    matchday_uts_dic = {}
    lastmday_uts = 0
    firstmday_uts = 0
    firstmday_uts = 9999999999
    lastmday_human = ''
    firstmday_human = ''
    nextmday_human = ''

    # we need the url to be added to the logo URL
    if request and request.META:
        base_url = url_build(request.META)
    else:
        base_url = ''


    uts = uts_now()

    # we need to group the list by matchdays
    for match in sorted(match_list, key=lambda i: i['date_uts'], reverse=False):
    # for match in match_list:
        dateobj = datestr_to_date(match['date'], '%Y-%m-%d')
        match_day = date_to_datestr(dateobj, '%d.%m.%Y')
        match_uts = date_to_uts_utc(match['date'], '%Y-%m-%d')

        # we need the completed matchday to set the display key to true
        if match['date_uts'] > lastmday_uts:
            if uts >  match['date_uts']:
                lastmday_uts =  match['date_uts']
                lastmday_human = match['date']
            elif uts > (match['date_uts'] - 12 * 3600):
                # if matches are supposed to start within next 12 hours show the mathday
                nextmday_uts = match['date_uts']
                nextmday_human = match['date']
        # we need the first machday for cornercase handling (begin of season with no matches yet)
        if match['date_uts'] <= firstmday_uts:
            firstmday_uts =  match['date_uts']
            firstmday_human = match['date']

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

    if matchday_dic and nextmday_human:
        matchday_dic[nextmday_human]['displayday'] = True
    elif matchday_dic and lastmday_human:
        # set displayflag to last matchday (during season this should be the case)
        matchday_dic[lastmday_human]['displayday'] = True
    elif matchday_dic and firstmday_human:
        # set displayflag to first matchday (no matches in season yet)
        matchday_dic[firstmday_human]['displayday'] = True

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
