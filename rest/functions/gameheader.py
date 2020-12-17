# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()

from rest.models import Gameheader

def gameheader_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('gameheader_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add event
        obj, _created = Gameheader.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in gameheader_add(): {0}'.format(err_))
        result = None
    logger.debug('gameheader_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def gameheader_get(logger, fkey, fvalue, vlist=('match_id', 'period_event')):
    """ get info for a specifc match_id """
    logger.debug('gameheader_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            event_dic = list(Gameheader.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            event_dic = Gameheader.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except BaseException:
        event_dic = {}
    return event_dic

def points_get(logger, team, game_header):
    """ get points """
    logger.debug('teammatchstat_add()')

    extra_time = game_header['results']['extra_time']
    score_home = game_header['results']['score']['final']['score_home']
    score_guest = game_header['results']['score']['final']['score_guest']
    points = 0

    if extra_time:
        if team == 'home':
            if score_home > score_guest:
                # home team wins OT
                points = 2
            else:
                # home team lost OT
                points = 1
        else:
            # home team wins OT
            if score_home > score_guest:
                points = 1
            else:
                # home team lost OT
                points = 2
    else:
        if team == 'home':
            if score_home > score_guest:
                # home team wins regular
                points = 3
        else:
            if score_guest > score_home:
                # visitor wins regular
                points = 3

    return points
