# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413, R0914
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.functions.helper import list_sumup, pctg_float_get
from rest.functions.teammatchstat import teammatchstats_get
from rest.functions.teamstat import teamstat_dic_get


def prematchoverview_get(logger, request, fkey, fvalue, matchinfo_dic):
    """ get pre-stats """
    logger.debug('prematchoverview_get({0}:{1})'.format(fkey, fvalue))

    prematch_dic = {}

    prematch_dic['date'] = matchinfo_dic['date']
    prematch_dic['home_team_logo'] = matchinfo_dic['home_team_logo']
    prematch_dic['home_team_shortcut'] = matchinfo_dic['home_team__shortcut']
    prematch_dic['home_team_color'] = matchinfo_dic['home_team__color_primary']
    prematch_dic['visitor_team_logo'] = matchinfo_dic['visitor_team_logo']
    prematch_dic['visitor_team_shortcut'] = matchinfo_dic['visitor_team__shortcut']
    prematch_dic['visitor_team_color'] = matchinfo_dic['visitor_team__color_secondary']

    # stats per team per match
    matchstat_list = teammatchstats_get(logger, 'match__season_id', matchinfo_dic['season_id'])
    # stacked stats per team
    teamstat_dic = teamstat_dic_get(logger, matchstat_list)

    prematchoverview_dic = _pmodata_get(logger, [matchinfo_dic['home_team_id'], matchinfo_dic['visitor_team_id']], teamstat_dic)
    for team_id in prematchoverview_dic:
        if team_id == matchinfo_dic['home_team_id']:
            team = 'home'
        else:
            team = 'visitor'

        for key in prematchoverview_dic[team_id]:
            prematch_dic['{0}_{1}'.format(team, key)] = prematchoverview_dic[team_id][key]

    return prematch_dic

def _pmodata_get(logger, team_list, teamstat_dic):
    """ get prematch overview data """

    teamstat_sum_dic = {}
    for team_id in team_list:
        teamstat_sum_dic[team_id] = {}
        # sumup data per team
        tmp_list = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'goals_pp', 'goals_pp_against', 'ppcount', 'shcount', 'faceoffslost', 'faceoffswon', 'goals_for', 'goals_against', 'shots_for_5v5', 'shots_against_5v5', 'shots_ongoal_for', 'shots_ongoal_against', 'goals_pp', 'ppcount', 'goals_pp_against', 'shcount', 'saves'])
        games_num = len(tmp_list)

        tmp_dic = tmp_list[-1]
        # faceoff percentage
        teamstat_sum_dic[team_id]['fac_pctg'] = pctg_float_get(tmp_dic['sum_faceoffswon'], tmp_dic['sum_faceoffswon'] + tmp_dic['sum_faceoffslost'], 1)
        # goals per game
        teamstat_sum_dic[team_id]['goals_for_pg'] = round(tmp_dic['sum_goals_for']/games_num, 2)
        teamstat_sum_dic[team_id]['goals_against_pg'] = round(tmp_dic['sum_goals_against']/games_num, 2)
        # shots on goal per game
        teamstat_sum_dic[team_id]['shots_ongoal_for_pg'] = round(tmp_dic['sum_shots_ongoal_for']/games_num, 2)
        teamstat_sum_dic[team_id]['shots_ongoal_against_pg'] = round(tmp_dic['sum_shots_ongoal_against']/games_num, 2)
        # corsi
        teamstat_sum_dic[team_id]['corsi_pctg'] = pctg_float_get(tmp_dic['sum_shots_for_5v5'], tmp_dic['sum_shots_for_5v5'] + tmp_dic['sum_shots_against_5v5'], 1)
        # pp/ppk %
        teamstat_sum_dic[team_id]['pp_pctg'] = pctg_float_get(tmp_dic['sum_goals_pp'], tmp_dic['sum_ppcount'], 0)
        teamstat_sum_dic[team_id]['pk_pctg'] = 100 - pctg_float_get(tmp_dic['sum_goals_pp_against'], tmp_dic['sum_shcount'], 0)
        # pdo
        teamstat_sum_dic[team_id]['sh_pctg'] = pctg_float_get(tmp_dic['sum_goals_for'], tmp_dic['sum_shots_ongoal_for'], 0)
        teamstat_sum_dic[team_id]['sv_pctg'] = pctg_float_get(tmp_dic['sum_saves'], tmp_dic['sum_shots_ongoal_against'], 0)
        teamstat_sum_dic[team_id]['pdo'] = teamstat_sum_dic[team_id]['sh_pctg'] + teamstat_sum_dic[team_id]['sv_pctg']

    return teamstat_sum_dic
