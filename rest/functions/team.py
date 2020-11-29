# -*- coding: utf-8 -*-
""" list of functions for teams """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.models import Team
from rest.functions.helper import list2dic, url_build

def team_dic_get(logger, request):
    """ query team(s) from database based with optional filtering """
    logger.debug('teams_dic_get()')

    team_list = team_list_get(logger, None, None, ['team_id', 'team_name', 'shortcut', 'logo'])
    team_dic = list2dic(logger, team_list, 'team_id')

    if request:
        url = url_build(request)
        for team_id in team_dic:
            team_dic[team_id]['team_logo'] = '{0}{1}{2}'.format(url, settings.STATIC_URL, team_dic[team_id]['logo'])

    return team_dic

def team_list_get(logger, fkey=None, fvalue=None, vlist=('team_id', 'team_name', 'shortcut')):
    """ query team(s) from database based with optional filtering """
    logger.debug('team_list_get({0}:{1})'.format(fkey, fvalue))
    try:
        if fkey:
            if len(vlist) == 1:
                team_list = Team.objects.filter(**{fkey: fvalue}).order_by('team_id').values_list(vlist[0], flat=True)
            else:
                team_list = Team.objects.filter(**{fkey: fvalue}).order_by('team_id').values(*vlist)
        else:
            if len(vlist) == 1:
                team_list = Team.objects.all().order_by('team_id').values_list(vlist[0], flat=True)
            else:
                team_list = Team.objects.all().order_by('team_id').values(*vlist)
    except BaseException as err_:
        logger.critical('error in team_list_get(): {0}'.format(err_))
        team_list = []
    logger.debug('team_list_get({0}:{1}) ended with {2}'.format(fkey, fvalue, bool(team_list)))
    return list(team_list)

def team_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('team_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add authorization
        obj, _created = Team.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.team_id
    except BaseException as err_:
        logger.critical('error in team_add(): {0}'.format(err_))
        result = None
    logger.debug('team_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result
