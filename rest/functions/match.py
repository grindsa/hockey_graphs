# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Match

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
