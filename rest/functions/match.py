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
from rest.models import Match
from rest.functions.helper import url_build
from rest.functions.teamstat import teamstat_get

def match_info_get(logger, match_id, request, vlist=('date', 'result', 'home_team_id', 'home_team__team_name', 'home_team__shortcut', 'home_team__logo', 'visitor_team_id', 'visitor_team__team_name', 'visitor_team__shortcut', 'visitor_team__logo')):
    """ get info for a specifc match_id """
    logger.debug('match_info_get()')
    try:
        match_dic = Match.objects.filter(match_id=match_id).values(*vlist)[0]
    except BaseException:
        match_dic = {}

    # change logo link
    base_url = url_build(request)
    match_dic['home_team_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match_dic['home_team__logo'])
    match_dic['visitor_team_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match_dic['visitor_team__logo'])

    return match_dic

def match_list_get(logger, fkey=None, fvalue=None, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team')):
    """ query team(s) from database based with optional filtering """
    logger.debug('match_list_get({0}:{1})'.format(fkey, fvalue))
    try:
        if fkey:
            if len(vlist) == 1:
                match_list = Match.objects.filter(**{fkey: fvalue}).order_by('match_id').values_list(vlist[0], flat=True)
            else:
                match_list = Match.objects.filter(**{fkey: fvalue}).order_by('match_id').values(*vlist)
        else:
            if len(vlist) == 1:
                match_list = Match.objects.all().order_by('match_id').values_list(vlist[0], flat=True)
            else:
                match_list = Match.objects.all().order_by('match_id').values(*vlist)
    except BaseException as err_:
        logger.critical('error in match_list_get(): {0}'.format(err_))
        match_list = []
    logger.debug('match_list_get({0}:{1}) ended with {2}'.format(fkey, fvalue, bool(match_list)))
    return list(match_list)

def match_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('match_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add match
        obj, _created = Match.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.match_id
    except BaseException as err_:
        logger.critical('error in match_add(): {0}'.format(err_))
        result = None
    logger.debug('match_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def matchstats_get(logger, match_id):
    """ get matchstatistics """

    matchstat_dic = teamstat_get(logger, 'match', match_id)

    stat_dic = {
        'home_team': {
            'shotsOnGoal': matchstat_dic['home']['shotsOnGoal'],
            'saves': matchstat_dic['home']['saves'],
            'faceOffsWon': matchstat_dic['home']['faceOffsWon'],
            'penaltyMinutes': matchstat_dic['home']['penaltyMinutes'],
            'powerPlaySeconds': matchstat_dic['home']['powerPlaySeconds'],
            'ppGoals': matchstat_dic['home']['ppGoals'],
            'shGoals': matchstat_dic['home']['shGoals'],
            'puckpossession': int(matchstat_dic['home']['shotsAttempts'] * 100 / (matchstat_dic['home']['shotsAttempts'] + matchstat_dic['home']['shotsAttempts']))
        },
        'visitor_team': {
            'shotsOnGoal': matchstat_dic['visitor']['shotsOnGoal'],
            'saves': matchstat_dic['visitor']['saves'],
            'faceOffsWon': matchstat_dic['visitor']['faceOffsWon'],
            'penaltyMinutes': matchstat_dic['visitor']['penaltyMinutes'],
            'powerPlaySeconds': matchstat_dic['visitor']['powerPlaySeconds'],
            'ppGoals': matchstat_dic['visitor']['ppGoals'],
            'shGoals': matchstat_dic['visitor']['shGoals'],
            'puckpossession': int(matchstat_dic['visitor']['shotsAttempts'] * 100 / (matchstat_dic['home']['shotsAttempts'] + matchstat_dic['home']['shotsAttempts']))
        }
    }

    stat_entry = {
        'title': 'foo',
        'chart': stat_dic,
        'tabs': False
    }

    return stat_entry
