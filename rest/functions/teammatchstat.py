# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Teammatchstat
from rest.functions.match import match_info_get

def teammatchstat_add(logger, match_dic):
    """ add team to database """
    logger.debug('teammatchstat_add()')

    match_id = match_dic['match_id']

    match_info_dic = match_info_get(logger, match_id, None)

    result_list = []
    for team in ['home', 'visitor']:

        if team == 'home':
            o_team = 'visitor'
            team_id = match_info_dic['home_team_id']
        else:
            o_team = 'home'
            team_id = match_info_dic['visitor_team_id']

        data_dic = {
            'match_id': match_id,
            'team_id': team_id,
            'goals_for': match_dic[team]['goals'],
            'goals_against': match_dic[o_team]['goals'],
            'goals_pp': match_dic[team]['ppGoals'],
            'goals_sh': match_dic[team]['shGoals'],
            'shots_for': match_dic[team]['shotsAttempts'],
            'shots_against': match_dic[o_team]['shotsAttempts'],
            'shots_ongoal_for': match_dic[team]['shotsOnGoal'],
            'shots_ongoal_against': match_dic[o_team]['shotsOnGoal'],
            'shots_ongoal_pctg': match_dic[o_team]['shotEfficiency'],
            'saves': match_dic[o_team]['saves'],
            'saves_pctg': match_dic[o_team]['savesPercent'],
            'faceoffswon': match_dic[team]['faceOffsWon'],
            'faceoffswon_pctg': match_dic[team]['faceOffsWonPercent'],
            'penaltyminutes': match_dic[team]['penaltyMinutes'],
            'powerplayseconds': match_dic[team]['powerPlaySeconds'],
        }

        try:
            # add teammatchstat
            obj, _created = Teammatchstat.objects.update_or_create(match_id=match_id, team_id=team_id, defaults=data_dic)
            obj.save()
            result_list.append(obj.id)
        except BaseException as err_:
            logger.critical('error in teammatchstat_add(): {0}'.format(err_))
            result_list.append(None)

    logger.debug('teammatchstat_add() ended with: {0}'.format(result_list))
    return result_list

def teammatchstat_get(_logger, fkey=None, fvalue=None, vlist=('match_id', 'home', 'visitor')):
    """ get info for a specifc match_id """
    # logger.debug('teammatchstat_get({0}:{1})'.format(fkey, fvalue))
    try:
        if fkey:
            if len(vlist) == 1:
                teammatchstat_dic = list(Teammatchstat.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
            else:
                teammatchstat_dic = Teammatchstat.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
        else:
            if len(vlist) == 1:
                teammatchstat_dic = Teammatchstat.objects.all().order_by('match_id').values_list(vlist[0], flat=True)
            else:
                teammatchstat_dic = Teammatchstat.objects.all().order_by('match_id').values(*vlist)
    except BaseException:
        teammatchstat_dic = {}

    return teammatchstat_dic
