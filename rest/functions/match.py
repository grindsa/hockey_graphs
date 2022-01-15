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
from rest.functions.helper import url_build, pctg_get, min2sec
from rest.functions.teamstat import teamstat_get

def match_info_get(logger, match_id, request, vlist=('date', 'date_uts', 'result', 'result_suffix', 'home_team_id', 'home_team__team_name', 'home_team__shortcut', 'home_team__logo', 'home_team__color_primary', 'home_team__color_secondary', 'home_team__color_tertiary', 'home_team__color_quaternary', 'home_team__color_penalty_primary', 'home_team__color_penalty_secondary', 'visitor_team_id', 'visitor_team__team_name', 'visitor_team__shortcut', 'visitor_team__logo', 'visitor_team__color_primary', 'visitor_team__color_secondary',  'visitor_team__color_tertiary', 'visitor_team__color_quaternary', 'visitor_team__color_penalty_primary', 'visitor_team__color_penalty_secondary', 'home_team__twitter_name', 'visitor_team__twitter_name', 'home_team__facebook_groups', 'visitor_team__facebook_groups', 'home_team__bg_images', 'visitor_team__bg_images', 'season_id')):
    """ get info for a specifc match_id """
    logger.debug('match_info_get()')
    try:
        match_dic = Match.objects.filter(match_id=match_id).values(*vlist)[0]
    except BaseException as err:
        logger.error(err)
        match_dic = {}

    # change logo link
    try:
        base_url = url_build(request)
    except BaseException as err:
        base_url = None
    match_dic['base_url'] = base_url

    if 'home_team__logo' in match_dic:
        match_dic['home_team_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match_dic['home_team__logo'])
    if 'visitor_team__logo' in match_dic:
        match_dic['visitor_team_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match_dic['visitor_team__logo'])

    return match_dic

def match_list_get(logger, fkey=None, fvalue=None, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team')):
    """ query team(s) from database based with optional filtering """
    logger.debug('match_list_get({0}:{1})'.format(fkey, fvalue))
    try:
        if fkey:
            if len(vlist) == 1:
                match_list = Match.objects.filter(**{fkey: fvalue}).order_by('match_id').exclude(disable=True).values_list(vlist[0], flat=True)
            else:
                match_list = Match.objects.filter(**{fkey: fvalue}).order_by('match_id').exclude(disable=True).values(*vlist)
        else:
            if len(vlist) == 1:
                match_list = Match.objects.all().order_by('match_id').exclude(disable=True).values_list(vlist[0], flat=True)
            else:
                match_list = Match.objects.all().order_by('match_id').exclude(disable=True).values(*vlist)
    except BaseException as err_:
        logger.critical('error in match_list_get(): {0}'.format(err_))
        match_list = []
    logger.debug('match_list_get({0}:{1}) ended with {2}'.format(fkey, fvalue, bool(match_list)))
    return list(match_list)

def matchinfo_list_get(logger, matchid_list, request, vlist=('date', 'date_uts', 'match_id', 'result', 'result_suffix', 'home_team_id', 'home_team__shortcut', 'home_team__logo', 'visitor_team_id', 'visitor_team__shortcut', 'visitor_team__logo')):
    """ query match_information for a list of matchids """
    logger.debug('matchinfo_list_get({0})'.format(len(matchid_list)))
    matchinfo_dic = {}
    for match_id in matchid_list:
        _matchinfo_dic = match_info_get(logger, match_id, request, vlist)
        if _matchinfo_dic:
            matchinfo_dic[match_id] = _matchinfo_dic
    logger.debug('matchinfo_list_get() ended with {0} entries'.format(len(matchinfo_dic.keys())))

    return matchinfo_dic

def match_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('match_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add match
        obj, created = Match.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.match_id
    except BaseException as err_:
        logger.critical('error in match_add(): {0}'.format(err_))
        result = None
    logger.debug('match_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return (result, created)

def matchstats_get(logger, match_id):
    """ get matchstatistics """
    # pylint: disable=E0602
    try:
        matchstat_dic = teamstat_get(logger, 'match', match_id)[0]
    except BaseException:
        matchstat_dic = {}

    if matchstat_dic:
        stat_dic = {
            'shotsOnGoal': _('Shots on Goal'),
            'saves': _('Saves'),
            'penaltyMinutes': _('Penalties in Minutes'),
            'ppGoals': _('Powerplay Goals'),
            'shGoals': _('Shorthanded Goals'),
            'faceOffsWon': _('Faceoff Win'),
            'puckpossession': _('Puck Possession'),
            'powerplaymin': _('Time in Powerplay'),
            'home_team': {
                'shotsOnGoal': matchstat_dic['home']['shotsOnGoal'],
                'shotsOnGoal_pctg': pctg_get(matchstat_dic['home']['shotsOnGoal'], (matchstat_dic['home']['shotsOnGoal'] + matchstat_dic['visitor']['shotsOnGoal'])),
                'saves': matchstat_dic['home']['saves'],
                'saves_pctg': pctg_get(matchstat_dic['home']['saves'], (matchstat_dic['home']['saves'] + matchstat_dic['visitor']['saves'])),
                'faceOffsWon': matchstat_dic['home']['faceOffsWon'],
                'faceOffsWon_pctg': pctg_get(matchstat_dic['home']['faceOffsWon'], (matchstat_dic['home']['faceOffsWon'] + matchstat_dic['visitor']['faceOffsWon'])),
                'penaltyMinutes': matchstat_dic['home']['penaltyMinutes'],
                'penaltyMinutes_pctg': pctg_get(matchstat_dic['home']['penaltyMinutes'], (matchstat_dic['home']['penaltyMinutes'] + matchstat_dic['visitor']['penaltyMinutes'])),
                'powerplaymin': min2sec(matchstat_dic['home']['powerPlaySeconds']),
                'powerplaymin_pctg': pctg_get(matchstat_dic['home']['powerPlaySeconds'], (matchstat_dic['home']['powerPlaySeconds'] + matchstat_dic['visitor']['powerPlaySeconds'])),
                'ppGoals': matchstat_dic['home']['ppGoals'],
                'ppGoals_pctg': pctg_get(matchstat_dic['home']['ppGoals'], (matchstat_dic['home']['ppGoals'] + matchstat_dic['visitor']['ppGoals'])),
                'shGoals': matchstat_dic['home']['shGoals'],
                'shGoals_pctg': pctg_get(matchstat_dic['home']['shGoals'], (matchstat_dic['home']['shGoals'] + matchstat_dic['visitor']['shGoals'])),
                'puckpossession': pctg_get(matchstat_dic['home']['shotsAttempts'], (matchstat_dic['home']['shotsAttempts'] + matchstat_dic['visitor']['shotsAttempts'])),
                'puckpossession_pctg': pctg_get(matchstat_dic['home']['shotsAttempts'], (matchstat_dic['home']['shotsAttempts'] + matchstat_dic['visitor']['shotsAttempts']))
            },
            'visitor_team': {
                'shotsOnGoal': matchstat_dic['visitor']['shotsOnGoal'],
                'shotsOnGoal_pctg': pctg_get(matchstat_dic['visitor']['shotsOnGoal'], (matchstat_dic['home']['shotsOnGoal'] + matchstat_dic['visitor']['shotsOnGoal'])),
                'saves': matchstat_dic['visitor']['saves'],
                'saves_pctg': pctg_get(matchstat_dic['visitor']['saves'], (matchstat_dic['home']['saves'] + matchstat_dic['visitor']['saves'])),
                'faceOffsWon': matchstat_dic['visitor']['faceOffsWon'],
                'faceOffsWon_pctg': pctg_get(matchstat_dic['visitor']['faceOffsWon'], (matchstat_dic['home']['faceOffsWon'] + matchstat_dic['visitor']['faceOffsWon'])),
                'penaltyMinutes': matchstat_dic['visitor']['penaltyMinutes'],
                'penaltyMinutes_pctg': pctg_get(matchstat_dic['visitor']['penaltyMinutes'], (matchstat_dic['home']['penaltyMinutes'] + matchstat_dic['visitor']['penaltyMinutes'])),
                'powerplaymin': min2sec(matchstat_dic['visitor']['powerPlaySeconds']),
                'powerplaymin_pctg': pctg_get(matchstat_dic['visitor']['powerPlaySeconds'], (matchstat_dic['home']['powerPlaySeconds'] + matchstat_dic['visitor']['powerPlaySeconds'])),
                'ppGoals': matchstat_dic['visitor']['ppGoals'],
                'ppGoals_pctg': pctg_get(matchstat_dic['visitor']['ppGoals'], (matchstat_dic['home']['ppGoals'] + matchstat_dic['visitor']['ppGoals'])),
                'shGoals': matchstat_dic['visitor']['shGoals'],
                'shGoals_pctg': pctg_get(matchstat_dic['visitor']['shGoals'], (matchstat_dic['home']['shGoals'] + matchstat_dic['visitor']['shGoals'])),
                'puckpossession': pctg_get(matchstat_dic['visitor']['shotsAttempts'], (matchstat_dic['home']['shotsAttempts'] + matchstat_dic['visitor']['shotsAttempts'])),
                'puckpossession_pctg': pctg_get(matchstat_dic['visitor']['shotsAttempts'], (matchstat_dic['home']['shotsAttempts'] + matchstat_dic['visitor']['shotsAttempts']))
            }
        }

        stat_entry = {
            'title': _('Overview'),
            'chart': stat_dic,
            'tabs': False
        }

    else:
        stat_entry = {}

    return stat_entry

def last_match_get(logger, season_id, uts):
    """ get information of past match """
    logger.debug('next_match_get({0}:{1})'.format(season_id, uts))
    match_list = match_list_get(logger, 'season_id', season_id, ('match_id', 'date_uts', 'date', 'result', 'home_team_id', 'home_team__team_name', 'home_team__shortcut', 'home_team__logo', 'visitor_team_id', 'visitor_team__team_name', 'visitor_team__shortcut', 'visitor_team__logo'))
    match_info_dic = {}
    match_id = None
    for match in match_list:
        if match['date_uts'] <= uts:
            match_info_dic = match
            match_id = match['match_id']

    logger.debug('next_match_get() ended with: {0}'.format(match_id))
    return(match_id, match_info_dic)

def next_match_get(logger, season_id, uts):
    """ get information of upcoming match """
    logger.debug('next_match_get({0}:{1})'.format(season_id, uts))
    match_list = match_list_get(logger, 'season_id', season_id, ('match_id', 'date_uts', 'date', 'result', 'home_team_id', 'home_team__team_name', 'home_team__shortcut', 'home_team__logo', 'visitor_team_id', 'visitor_team__team_name', 'visitor_team__shortcut', 'visitor_team__logo'))

    match_info_dic = {}
    match_id = None
    for match in match_list:
        if uts <= match['date_uts']:
            match_info_dic = match
            match_id = match['match_id']
            break
    logger.debug('next_match_get() ended with: {0}'.format(match_id))
    return(match_id, match_info_dic)

def openmatch_list_get(logger, season_id, uts=0, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team')):
    """ get a list of non finished matches from past """
    logger.debug('match_list_get({0}:{1})'.format(season_id, uts))
    try:
        if len(vlist) == 1:
            match_list = Match.objects.filter(season_id=season_id, finish=False, date_uts__lt=uts).order_by('match_id').exclude(disable=True).values_list(vlist[0], flat=True)
        else:
            match_list = Match.objects.filter(season_id=season_id, finish=False, date_uts__lt=uts).order_by('match_id').exclude(disable=True).values(*vlist)
    except BaseException as err_:
        logger.critical('error in match_list_get(): {0}'.format(err_))
        match_list = []
    logger.debug('match_list_get() ended with {0}'.format(bool(match_list)))
    return list(match_list)

def pastmatch_list_get(logger, season_id, uts=0, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team')):
    """ get a list of non finished matches from past """
    logger.debug('pastmatch_list_get({0}:{1})'.format(season_id, uts))
    try:
        if len(vlist) == 1:
            match_list = Match.objects.filter(season_id=season_id, date_uts__lt=uts).order_by('match_id').exclude(disable=True).values_list(vlist[0], flat=True)
        else:
            match_list = Match.objects.filter(season_id=season_id, date_uts__lt=uts).order_by('match_id').exclude(disable=True).values(*vlist)
    except BaseException as err_:
        logger.critical('error in match_list_get(): {0}'.format(err_))
        match_list = []
    logger.debug('pastmatch_list_get() ended with {0}'.format(bool(match_list)))
    return list(match_list)

def sincematch_list_get(logger, season_id, uts=0, treshold=0, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team')):
    """ get a list of non finished matches from past """
    logger.debug('sincematch_list_get({0}:{1})'.format(season_id, uts))
    try:
        if len(vlist) == 1:
            match_list = Match.objects.filter(season_id=season_id, date_uts__lt=uts, date_uts__gt=uts-treshold).order_by('match_id').exclude(disable=True).values_list(vlist[0], flat=True)
        else:
            match_list = Match.objects.filter(season_id=season_id, date_uts__lt=uts, date_uts__gt=uts-treshold).order_by('match_id').exclude(disable=True).values(*vlist)
    except BaseException as err_:
        logger.critical('error in sincematch_list_get(): {0}'.format(err_))
        match_list = []
    logger.debug('sincematch_list_get() ended with {0}'.format(bool(match_list)))
    return list(match_list)

def futurematch_list_get(logger, season_id, uts=0, treshold=0, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team')):
    """ get a list of non finished matches from past """
    logger.debug('sincematch_list_get({0}:{1})'.format(season_id, uts))
    try:
        if len(vlist) == 1:
            match_list = Match.objects.filter(season_id=season_id, date_uts__gt=uts, date_uts__lt=uts+treshold).order_by('match_id').exclude(disable=True).values_list(vlist[0], flat=True)
        else:
            match_list = Match.objects.filter(season_id=season_id, date_uts__gt=uts, date_uts__lt=uts+treshold).order_by('match_id').exclude(disable=True).values(*vlist)
    except BaseException as err_:
        logger.critical('error in sincematch_list_get(): {0}'.format(err_))
        match_list = []
    logger.debug('sincematch_list_get() ended with {0}'.format(bool(match_list)))
    return list(match_list)


def untweetedmatch_list_get(logger, season_id, uts=0, treshold=0, vlist=('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team')):
    """ get a list of non finished matches from past """
    logger.debug('untweetedmatch_list_get({0}:{1})'.format(season_id, uts))
    try:
        if len(vlist) == 1:
            match_list = Match.objects.filter(season_id=season_id, date_uts__lt=uts, date_uts__gt=uts-treshold, finish=True, tweet=False).order_by('match_id').exclude(disable=True).values_list(vlist[0], flat=True)
        else:
            match_list = Match.objects.filter(season_id=season_id, date_uts__lt=uts, date_uts__gt=uts-treshold).order_by('match_id').exclude(disable=True).values(*vlist)
    except BaseException as err_:
        logger.critical('error in sincematch_list_get(): {0}'.format(err_))
        match_list = []
    logger.debug('sincematch_list_get() ended with {0}'.format(bool(match_list)))
    return list(match_list)
