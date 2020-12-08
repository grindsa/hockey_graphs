# -*- coding: utf-8 -*-
""" list of functions for special team performance """
# pylint: disable=E0401, C0413
from functions.helper import list_sumup, pctg_float_get
from functions.corsi import pace_chartseries_get

def _pppk_sumup(logger, teamstat_dic):
    """ sum up faceoff statistics """
    logger.debug('_pppk_sumup()')

    update_amount = 0
    teamstat_sum_dic = {}

    for team_id in teamstat_dic:

        # sumup data per team
        teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'goals_pp', 'goals_pp_against', 'ppcount', 'shcount'])
        # check how many items we have to create in update_dic
        if update_amount < len(teamstat_sum_dic[team_id]):
            update_amount = len(teamstat_sum_dic[team_id])

        for ele in range(1, update_amount+1):
            # calculate pp/ppk
            teamstat_sum_dic[team_id][ele-1]['pp_pctg'] = pctg_float_get(teamstat_sum_dic[team_id][ele-1]['sum_goals_pp'], teamstat_sum_dic[team_id][ele-1]['sum_ppcount'], 0)
            teamstat_sum_dic[team_id][ele-1]['pk_pctg'] = 100 - pctg_float_get(teamstat_sum_dic[team_id][ele-1]['sum_goals_pp_against'], teamstat_sum_dic[team_id][ele-1]['sum_shcount'], 0)

    return (teamstat_sum_dic, update_amount)

def pppk_data_get(logger, ismobile, teamstat_dic, teams_dic):
    """ build structure for pace chart """
    logger.debug('pppk_data_get()')

    if ismobile:
        image_width = 25
    else:
        image_width = 40
    image_height = image_width

    # get summary
    (pppksum_dic, update_amount) = _pppk_sumup(logger, teamstat_dic)

    pppk_lake = {}

    for ele in range(1, update_amount+1):
        pppk_lake[ele] = []

    for team_id in pppksum_dic:
        # harmonize lengh by adding list elements at the beginning
        if len(pppksum_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(pace_sum_dic[team_id])):
                pppksum_dic[team_id].insert(0, pace_sum_dic[team_id][0])

        for idx, ele in enumerate(pppksum_dic[team_id], 1):
            pppk_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(teams_dic[team_id]['team_logo'])},
                'pp_pctg': ele['pp_pctg'],
                'pk_pctg': ele['pk_pctg'],
                'x': ele['pp_pctg'],
                'y': ele['pk_pctg']
            })

    # build final dictionary
    pppk_chartseries_dic = pace_chartseries_get(logger, pppk_lake)

    return pppk_chartseries_dic
