# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Teamstat

def teamstat_add(logger, fkey=None, fvalue=None, data_dic=None):
    """ add team to database """
    logger.debug('teamstat_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add teamstat
        obj, _created = Teamstat.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in teamstat_add(): {0}'.format(err_))
        result = None
    logger.debug('teamstat_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def teamstat_get(logger, fkey=None, fvalue=None, vlist=('match_id', 'home', 'visitor')):
    """ get info for a specifc match_id """
    logger.debug('teamstat_get({0}:{1})'.format(fkey, fvalue))

    try:
        if fkey:
            if fkey == 'match_id' and isinstance(fvalue, list):
                if len(vlist) == 1:
                    teamstat_dic = list(Teamstat.objects.filter(match__in=fvalue).values_list(vlist[0], flat=True))
                else:
                    teamstat_dic = list(Teamstat.objects.filter(match__in=fvalue).values(*vlist))
            else:
                if len(vlist) == 1:
                    teamstat_dic = list(Teamstat.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))
                else:
                    teamstat_dic = list(Teamstat.objects.filter(**{fkey: fvalue}).values(*vlist))
        else:
            if len(vlist) == 1:
                teamstat_dic = Teamstat.objects.all().order_by('match_id').values_list(vlist[0], flat=True)
            else:
                teamstat_dic = Teamstat.objects.all().order_by('match_id').values(*vlist)
    except BaseException as err_:
        logger.debug('Error in teamstat_get(): {0}'.format(err_))
        teamstat_dic = []

    logger.debug('teamstat_get() ended.')
    return teamstat_dic

def teamstat_dic_get(logger, matchstat_list):
    logger.debug('teamstat_dic_get()')

    teamstat_dic = {}
    for stat in matchstat_list:
        if stat['team_id'] not in teamstat_dic:
            teamstat_dic[stat['team_id']] = []

        teamstat_dic[stat['team_id']].append(stat)

    return teamstat_dic
