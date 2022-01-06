# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Teamstatdel

def teamstatdel_add(logger, season_id=None, team_id=None, data_dic=None):
    """ add team to database """
    logger.debug('teamstatdel_add({0}:{1})'.format(season_id, team_id))
    try:
        # add teamstatdel
        obj, _created = Teamstatdel.objects.update_or_create(season_id=season_id, team_id=team_id, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in teamstatdel_add(): {0}'.format(err_))
        result = None
    logger.debug('teamstatdel_add({0}:{1}) ended with {2}'.format(season_id, team_id, result))
    return result

def teamstatdel_get(logger, fkey=None, fvalue=None, vlist=('seaon', 'team', 'leagueallteamstats')):
    """ get info for a specifc match_id """
    logger.debug('teamstatdel_get({0}:{1})'.format(fkey, fvalue))
    try:
        if fkey:
            if len(vlist) == 1:
                teamstatdel_dic = list(Teamstatdel.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))
            else:
                teamstatdel_dic = list(Teamstatdel.objects.filter(**{fkey: fvalue}).values(*vlist))
        else:
            if len(vlist) == 1:
                teamstatdel_dic = Teamstatdel.objects.all().order_by('team_id').values_list(vlist[0], flat=True)
            else:
                teamstatdel_dic = Teamstatdel.objects.all().order_by('team_id').values(*vlist)
    except BaseException as err_:
        logger.debug('Error in teamstatdel_get(): {0}'.format(err_))
        teamstatdel_dic = []

    return teamstatdel_dic
