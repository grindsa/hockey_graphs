# -*- coding: utf-8 -*-
""" list of functions for team comparison """
import numpy as np
from rest.functions.helper import pctg_float_get, list_sumup
from rest.functions.chartparameters import chart_color6, plotlines_color

def _deviation_avg_get(logger, input_list, value_list=None):
    logger.debug('_deviation_add()')

    _tmp_lake = {}
    for value in value_list:
        _tmp_lake[value] = []

    # compile lists
    for ele in input_list:
        for value in value_list:
            _tmp_lake[value].append(ele[value])

    # calculate deviation
    deviation_dic = {}
    for value in _tmp_lake:
        deviation_dic[value] = {'std_deviation': round(np.std(_tmp_lake[value]), 2), 'average': round(np.mean(_tmp_lake[value]), 2), 'min': np.amin(_tmp_lake[value]), 'max': np.amax(_tmp_lake[value])}
    return deviation_dic

def pdo_breakdown_data_get(logger, ismobile, teamstat_dic, teams_dic):
    logger.debug('pdo_breakdown_data_get()')

    if ismobile:
        image_width = 25
        image_height = 25
    else:
        image_width = 40
        image_height = 40

    update_amount = 0
    _teamstat_sum_dic = {}
    for team_id in teamstat_dic:
        # sumup data per team
        _teamstat_sum_dic[team_id] =  list_sumup(logger, teamstat_dic[team_id], ['match_id', 'shots_ongoal_for', 'shots_ongoal_against', 'goals_for', 'saves'])
        # check how many items we have to create in update_dic
        if update_amount < len(_teamstat_sum_dic[team_id]):
            update_amount = len(_teamstat_sum_dic[team_id])

    # psdeudo_data_lake to calculate sums
    _tmp_lake = {}

    # updates_dic = {}
    chartseries_dic = {}
    for ele in range(1, update_amount+1):
        chartseries_dic[ele] = {'data': [], 'x_avg': 0, 'y_avg': 0}
        _tmp_lake[ele] = {'sum_goals_for': 0, 'sum_shots_ongoal_for': 0, 'sum_shots_ongoal_against': 0, 'sum_saves': 0}

    for team_id in _teamstat_sum_dic:
        shortcut = teams_dic[team_id]['shortcut']
        logo = teams_dic[team_id]['team_logo']
        team_name = teams_dic[team_id]['team_name']
        # harmonize lengh by adding list elements at the beginning
        if len(_teamstat_sum_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(_teamstat_sum_dic[team_id])):
                _teamstat_sum_dic[team_id].insert(0, _teamstat_sum_dic[team_id][0])

        for ele in range(1, update_amount+1):
            sum_goals_for = _teamstat_sum_dic[team_id][ele-1]['sum_goals_for']
            sum_shots_ongoal_for = _teamstat_sum_dic[team_id][ele-1]['sum_shots_ongoal_for']
            sum_saves = _teamstat_sum_dic[team_id][ele-1]['sum_saves']
            sum_shots_ongoal_against = _teamstat_sum_dic[team_id][ele-1]['sum_shots_ongoal_against']
            # sum up in datalake
            _tmp_lake[ele]['sum_goals_for'] += sum_goals_for
            _tmp_lake[ele]['sum_shots_ongoal_for'] += sum_shots_ongoal_for
            _tmp_lake[ele]['sum_saves'] += sum_saves
            _tmp_lake[ele]['sum_shots_ongoal_against'] += sum_shots_ongoal_against

            chartseries_dic[ele]['data'].append({'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(logo)}, 'team_name': team_name, 'name': shortcut, 'x': pctg_float_get(sum_goals_for, sum_shots_ongoal_for), 'y': pctg_float_get(sum_saves, sum_shots_ongoal_against)})

    # calculate x_avg and y_avg
    for ele in _tmp_lake:
        chartseries_dic[ele]['x_avg'] = pctg_float_get(_tmp_lake[ele]['sum_goals_for'], _tmp_lake[ele]['sum_shots_ongoal_for'])
        chartseries_dic[ele]['y_avg'] = pctg_float_get(_tmp_lake[ele]['sum_saves'], _tmp_lake[ele]['sum_shots_ongoal_against'])

    # add standard deviation
    for ele in chartseries_dic:
        deviation_dic = _deviation_avg_get(logger, chartseries_dic[ele]['data'], ['x', 'y'])
        chartseries_dic[ele]['x_deviation'] = deviation_dic['x']['std_deviation']
        chartseries_dic[ele]['y_deviation'] = deviation_dic['y']['std_deviation']
        chartseries_dic[ele]['x_min'] = deviation_dic['x']['min']
        chartseries_dic[ele]['x_max'] = deviation_dic['x']['max']
        chartseries_dic[ele]['y_min'] = deviation_dic['y']['min']
        chartseries_dic[ele]['y_max'] = deviation_dic['y']['max']

    return chartseries_dic

def series_updates_get(logger, data_dic):
    logger.debug('pdo_breakdown_updates_get()')

    updates_dic = {}
    for ele in data_dic:
        updates_dic[ele] = {
            'text': ele,
            'chartoptions':  {
                'series': [{
                    'name': _('Standard Deviation'),
                    'color': plotlines_color,
                    'marker': {'symbol': 'square'},
                    'data': data_dic[ele]['data']
                }],
                'xAxis': {
                    'min': data_dic[ele]['x_min'] - 1,
                    'max':  data_dic[ele]['x_max'] + 1,
                    'plotBands': [{'from':  data_dic[ele]['x_avg'] -  data_dic[ele]['x_deviation']/2, 'to':  data_dic[ele]['x_avg'] +  data_dic[ele]['x_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value':  data_dic[ele]['x_avg']}],
                },
                'yAxis': {
                    'min': data_dic[ele]['y_min'] - 1,
                    'max':  data_dic[ele]['y_max'] + 1,
                    'plotBands': [{'from':  data_dic[ele]['y_avg'] -  data_dic[ele]['y_deviation']/2, 'to':  data_dic[ele]['y_avg'] +  data_dic[ele]['y_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value':  data_dic[ele]['y_avg']}],
                },
            }
        }

    return updates_dic
