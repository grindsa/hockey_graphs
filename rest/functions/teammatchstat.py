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
from rest.functions.gameheader import gameheader_get, points_get
from rest.functions.match import match_info_get
from rest.functions.corsi import gameshots5v5_get, goals5v5_get
from rest.functions.helper import pctg_float_get
from rest.functions.periodevent import periodevent_get, goaliepull_get
from rest.functions.shift import shift_get
from rest.functions.shot import shot_list_get, rebound_breaks_get
from rest.functions.xg import shotlist_process, xgf_calculate, xgscore_get

def teammatchstat_add(logger, match_dic, xg_data_dic):
    """ add team to database """
    # pylint: disable=R0914
    logger.debug('teammatchstat_add()')

    rebound_interval = 3
    break_interval = 7

    match_id = match_dic['match_id']

    match_info_dic = match_info_get(logger, match_id, None)
    shot_list = shot_list_get(logger, 'match_id', match_id, ['real_date', 'shot_id', 'match_id', 'timestamp', 'match_shot_resutl_id', 'match__home_team_id', 'team_id', 'player__first_name', 'player_id', 'player__last_name', 'player__stick', 'zone', 'coordinate_x', 'coordinate_y', 'player__jersey'])
    shift_list = shift_get(logger, 'match_id', match_id, ['shift'])
    periodevent_list = periodevent_get(logger, 'match_id', match_id, ['period_event'])

    # rebounds and breaks
    rb_dic = rebound_breaks_get(logger, shot_list, match_info_dic)

    result_list = []
    for team in ['home', 'visitor']:

        if team == 'home':
            o_team = 'visitor'
            team_id = match_info_dic['home_team_id']
        else:
            o_team = 'home'
            team_id = match_info_dic['visitor_team_id']

        # get corsi statistics
        (shots_for_5v5, shots_against_5v5, shots_ongoal_for_5v5, shots_ongoal_against_5v5, shot_list_5v5) = gameshots5v5_get(logger, match_info_dic, team, shot_list, shift_list, periodevent_list)

        # 5v5 goals from periodevents
        goals5v5_dic = goals5v5_get(logger, match_id, match_info_dic)

        # get goalipull events and goals
        goaliepull_dic = goaliepull_get(logger, team, periodevent_list)

        # xgf xga calculation
        # xf_dic = {}
        # xg_data_dic and xg_weights_dic and shot_list_5v5:
        #   # we also need the XGMODEL_DIC to check if we have the shotcoordinates in our structure
        #    (shotstat_dic, _goal_dic) = shotlist_process(logger, shot_list_5v5, xg_data_dic, rebound_interval, break_interval)
        #    # lets apply the magic algorithm to estimate xGF
        #    playerxgf_dic = xgf_calculate(logger, shotstat_dic, xg_weights_dic)
        #    xgf_dic = xgscore_get(logger, playerxgf_dic)

        game_header = gameheader_get(logger, 'match_id', match_id, ['gameheader'])
        points = points_get(logger, team, game_header)

        if 'lastEventTime' in game_header:
            lasteventtime = game_header['lastEventTime']
        else:
            lasteventtime = 3600

        data_dic = {
            'match_id': match_id,
            'matchduration': lasteventtime,
            'team_id': team_id,
            'goals_for': match_dic[team]['goals'],
            'goals_for_5v5': goals5v5_dic[team],
            'goals_against': match_dic[o_team]['goals'],
            'goals_against_5v5': goals5v5_dic[o_team],
            'goals_pp': match_dic[team]['ppGoals'],
            'goals_pp_against': match_dic[o_team]['ppGoals'],
            'goals_sh': match_dic[team]['shGoals'],
            'shots_for': match_dic[team]['shotsAttempts'],
            'shots_for_5v5': shots_for_5v5,
            'shots_pctg': pctg_float_get(match_dic[team]['goals'], match_dic[team]['shotsAttempts']),
            'shots_ongoal_for': match_dic[team]['shotsOnGoal'],
            'shots_ongoal_for_5v5': shots_ongoal_for_5v5,
            'shots_against': match_dic[o_team]['shotsAttempts'],
            'shots_against_5v5': shots_against_5v5,
            'shots_ongoal_against': match_dic[o_team]['shotsOnGoal'],
            'shots_ongoal_against_5v5': shots_ongoal_against_5v5,
            'shots_ongoal_pctg': pctg_float_get(match_dic[team]['goals'], match_dic[team]['shotsOnGoal']),
            'saves': match_dic[team]['saves'],
            'saves_pctg': pctg_float_get(match_dic[team]['saves'], match_dic[o_team]['shotsOnGoal']),
            'faceoffswon': match_dic[team]['faceOffsWon'],
            'faceoffslost': match_dic[o_team]['faceOffsWon'],
            'faceoffswon_pctg': match_dic[team]['faceOffsWonPercent'],
            'penaltyminutes_taken': match_dic[team]['penaltyMinutes'],
            'penaltyminutes_drawn': match_dic[o_team]['penaltyMinutes'],
            'powerplayseconds': match_dic[team]['powerPlaySeconds'],
            'rebounds_for': rb_dic[team]['rebounds'],
            'rebounds_against': rb_dic[o_team]['rebounds'],
            'goals_rebound_for': rb_dic[team]['rebound_goals'],
            'goals_rebound_against': rb_dic[o_team]['rebound_goals'],
            'breaks_for': rb_dic[team]['breaks'],
            'breaks_against': rb_dic[o_team]['breaks'],
            'goals_break_for': rb_dic[team]['break_goals'],
            'goals_break_against': rb_dic[o_team]['break_goals'],
            'ppcount': match_dic[team]['ppCount'],
            'shcount': match_dic[team]['shCount'],
            'ppefficiency': match_dic[team]['ppEfficiency'],
            'shefficiency': match_dic[team]['shEfficiency'],
            'points': points,
            'goalie_own_pull': goaliepull_dic['goalieown_pull'],
            'goalie_other_pull': goaliepull_dic['goalieother_pull'],
            'goalie_own_pulltime': goaliepull_dic['goaliepull_time'],
            'goals_en_for': goaliepull_dic['goals_en_for'],
            'goals_en_against': goaliepull_dic['goals_en_against'],
            'goals_wogoalie_for': goaliepull_dic['goals_wogoalie_for']
        }

        if team_id in xg_data_dic:
            logger.debug('teammatchstat_add(): add xg data (sum)')
            data_dic['xgoals_for'] = xg_data_dic[team_id]['xgf']
            data_dic['xgoals_against'] = xg_data_dic[team_id]['xga']

        try:
            # add teammatchstat
            obj, _created = Teammatchstat.objects.update_or_create(match_id=match_id, team_id=team_id, defaults=data_dic)
            obj.save()
            result_list.append(obj.id)
        except BaseException as err_:
            logger.critical('ERROR in teammatchstat_add(): {0}'.format(err_))
            result_list.append(None)

    logger.debug('teammatchstat_add() ended with: {0}'.format(result_list))
    return result_list

def teammatchstats_get(logger, fkey=None, fvalue=None, vlist=None):
    """ get info for a specifc match_id """
    logger.debug('teammatchstat_get({0}:{1})'.format(fkey, fvalue))
    try:
        if fkey:
            if vlist:
                if len(vlist) == 1:
                    teammatchstat_dic = Teammatchstat.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True)
                else:
                    teammatchstat_dic = Teammatchstat.objects.filter(**{fkey: fvalue}).values(*vlist)
            else:
                teammatchstat_dic = Teammatchstat.objects.filter(**{fkey: fvalue}).values()
        else:
            if vlist:
                if len(vlist) == 1:
                    teammatchstat_dic = Teammatchstat.objects.all().order_by('match_id').values_list(vlist[0], flat=True)
                else:
                    teammatchstat_dic = Teammatchstat.objects.all().order_by('match_id').values(*vlist)
            else:
                teammatchstat_dic = Teammatchstat.objects.all().order_by('match_id').values()

    except BaseException as err_:
        logger.critical('error in teammatchstats_get(): {0}'.format(err_))
        teammatchstat_dic = {}

    logger.debug('teammatchstat_get() ended')
    return list(teammatchstat_dic)
