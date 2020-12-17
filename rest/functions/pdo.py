# -*- coding: utf-8 -*-
""" list of functions for team comparison """
# pylint: disable=E0401, R0914
from rest.functions.helper import pctg_float_get, list_sumup, deviation_avg_get
from rest.functions.chartparameters import chart_color1, chart_color3, chart_color6, plotlines_color, title, font_size, corner_annotations
from rest.functions.corsi import pace_chartseries_get

def _ppg_sumup(logger, teamstat_dic):
    """ get data for breakdown chart """
    logger.debug('_ppg_sumup()')
    update_amount = 0
    _teamstat_sum_dic = {}
    for team_id in teamstat_dic:
        # sumup data per team
        _teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'shots_ongoal_for', 'goals_for', 'points'])

        # add amount of games
        for idx, match in enumerate(_teamstat_sum_dic[team_id], 1):
            match['games'] = idx

        # check how many items we have to create in update_dic
        if update_amount < len(_teamstat_sum_dic[team_id]):
            update_amount = len(_teamstat_sum_dic[team_id])

    return (_teamstat_sum_dic, update_amount)

def ppg_data_get(logger, ismobile, teamstat_dic, teams_dic):
    """ get data for breakdown chart """
    logger.debug('ppg_data_get()')

    if ismobile:
        image_width = 25
        image_height = 25
    else:
        image_width = 40
        image_height = 40

    # get summary
    (ppghsum_dic, update_amount) = _ppg_sumup(logger, teamstat_dic)

    # build temporary dictionary for data. we build the final sorted in next step
    ppg_lake = {}
    for ele in range(1, update_amount+1):
        ppg_lake[ele] = []

    for team_id in ppghsum_dic:
        # harmonize lengh by adding list elements at the beginning
        if len(ppghsum_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(ppghsum_dic[team_id])):
                ppghsum_dic[team_id].insert(0, ppghsum_dic[team_id][0])

        for idx, ele in enumerate(ppghsum_dic[team_id], 1):

            ppg_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(teams_dic[team_id]['team_logo'])},
                # points per games
                'ppg': round(ele['sum_points'] / ele['games'], 2),
                'sh_pctg':  pctg_float_get(ele['sum_goals_for'], ele['sum_shots_ongoal_for']),
                'games': ele['games'],
                'goals_for': ele['goals_for'],
                'shots_ongoal_for': ele['sum_shots_ongoal_for'],
                'points': ele['sum_points'],
                # 'x': pctg_float_get(ele['sum_goals_for'], ele['sum_shots_ongoal_for']),
                'y': round(ele['sum_points'] / ele['games'], 2)
            })

    # build final dictionary for chartseries
    ppg_chartseries_dic = pace_chartseries_get(logger, ppg_lake)

    return ppg_chartseries_dic

def ppg_updates_get(logger, data_dic, ctitle):
    """ get updates for points per game chart """
    logger.debug('ppg_updates_get()')

    updates_dic = {}
    for ele in data_dic:
        updates_dic[ele] = {
            'text': ele,
            'chartoptions':  {
                'series': [{
                    # pylint: disable=E0602
                    'name': _('Standard Deviation'),
                    'color': plotlines_color,
                    'marker': {'symbol': 'square'},
                    'data': data_dic[ele]['data']
                }],

                'yAxis': {
                    'title': title(ctitle, font_size),
                    'min': 0,
                    'tickInterval': 0.5,
                    # 'max':  data_dic[ele]['y_max'] + 2,
                    'plotBands': [{'from':  data_dic[ele]['y_avg'] -  data_dic[ele]['y_deviation']/2, 'to':  data_dic[ele]['y_avg'] +  data_dic[ele]['y_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 3, 'value':  data_dic[ele]['y_avg']}],
                },
            }
        }

    return updates_dic


def pdo_breakdown_data_get(logger, ismobile, teamstat_dic, teams_dic):
    """ get data for breakdown chart """
    logger.debug('pdo_breakdown_data_get()')

    if ismobile:
        image_width = 25
        image_height = 25
        overview_width = 20
        overview_height = 20
    else:
        image_width = 40
        image_height = 40
        overview_width = 30
        overview_height = 30

    update_amount = 0
    _teamstat_sum_dic = {}
    for team_id in teamstat_dic:
        # sumup data per team
        _teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'shots_ongoal_for', 'shots_ongoal_against', 'goals_for', 'saves'])
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
        logo_url = '<span><img src="{0}" alt="{1}" width="{2}" height="{3}"></span>'.format(teams_dic[team_id]['team_logo'], teams_dic[team_id]['shortcut'], overview_width, overview_height)
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

            chartseries_dic[ele]['data'].append({'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(logo)}, 'logo_url': logo_url, 'team_name': team_name, 'name': shortcut, 'x': pctg_float_get(sum_goals_for, sum_shots_ongoal_for), 'y': pctg_float_get(sum_saves, sum_shots_ongoal_against)})

    # calculate x_avg and y_avg
    for ele in _tmp_lake:
        chartseries_dic[ele]['x_avg'] = pctg_float_get(_tmp_lake[ele]['sum_goals_for'], _tmp_lake[ele]['sum_shots_ongoal_for'])
        chartseries_dic[ele]['y_avg'] = pctg_float_get(_tmp_lake[ele]['sum_saves'], _tmp_lake[ele]['sum_shots_ongoal_against'])

    # add standard deviation
    for ele in chartseries_dic:
        deviation_dic = deviation_avg_get(logger, chartseries_dic[ele]['data'], ['x', 'y'])
        chartseries_dic[ele]['x_deviation'] = deviation_dic['x']['std_deviation']
        chartseries_dic[ele]['y_deviation'] = deviation_dic['y']['std_deviation']
        chartseries_dic[ele]['x_min'] = deviation_dic['x']['min']
        chartseries_dic[ele]['x_max'] = deviation_dic['x']['max']
        chartseries_dic[ele]['y_min'] = deviation_dic['y']['min']
        chartseries_dic[ele]['y_max'] = deviation_dic['y']['max']

    return chartseries_dic

def overview_updates_get(logger, data_dic):
    """ build structure for pdo_overview_chart updates """
    logger.debug('breakdown_updates_get()')

    updates_dic = {}
    for ele in data_dic:
        updates_dic[ele] = {
            'chartoptions':  {
                'xAxis': {'categories': data_dic[ele]['team_list']},
                'series': [
                    # pylint: disable=E0602
                    {'name': _('Save percentage (Sv%)'), 'marker': {'symbol': 'square'}, 'data': data_dic[ele]['sv_list'], 'color': chart_color3},
                    {'name': _('Shooting percentage (Sh%)'), 'marker': {'symbol': 'square'}, 'data': data_dic[ele]['sh_list'], 'color': chart_color1},
                ]
            }
        }

    return updates_dic

def breakdown_updates_get(logger, data_dic, string_1=None, string_2=None, string_3=None, string_4=None, ismobile=False):
    # pylint: disable=E0602
    """ build structure for pdo breakdown chart """
    logger.debug('breakdown_updates_get()')

    updates_dic = {}
    for ele in data_dic:
        minmax_dic = {
            'x_min': round(data_dic[ele]['x_min'] - 1, 0),
            'y_min': round(data_dic[ele]['y_min'] - 1, 0),
            'x_max': round(data_dic[ele]['x_max'] + 1, 0),
            'y_max': round(data_dic[ele]['y_max'] + 1, 0)
        }
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
                    'title': title(_('Shooting percentage (Sh%)'), font_size),
                    'min': minmax_dic['x_min'],
                    'max': minmax_dic['x_max'],
                    'tickInterval': 1,
                    'gridLineWidth': 1,
                    'plotBands': [{'from':  data_dic[ele]['x_avg'] -  data_dic[ele]['x_deviation']/2, 'to':  data_dic[ele]['x_avg'] +  data_dic[ele]['x_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value':  data_dic[ele]['x_avg']}],
                },
                'yAxis': {
                    'title': title(_('Save percentage (Sv%)'), font_size),
                    'min': minmax_dic['y_min'],
                    'max': minmax_dic['y_max'],
                    'tickInterval': 1,
                    'gridLineWidth': 1,
                    'plotBands': [{'from':  data_dic[ele]['y_avg'] -  data_dic[ele]['y_deviation']/2, 'to':  data_dic[ele]['y_avg'] +  data_dic[ele]['y_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 3, 'value':  data_dic[ele]['y_avg']}],
                },
            }
        }
        if string_1 and string_2 and string_3 and string_4:
            updates_dic[ele]['chartoptions']['annotations'] = corner_annotations(ismobile, minmax_dic, string_1, string_2, string_3, string_4)

    return updates_dic

def pdo_overview_data_get(logger, _ismobile, data_dic):
    """ collect data for pdo overview chart """
    logger.debug('pdo_overview_data_get()')

    overview_dic = {}

    for mday in data_dic:
        overview_dic[mday] = {'team_list': [], 'sh_list': [], 'sv_list': []}
        for datapoint in sorted(data_dic[mday]['data'], key=lambda i: i['team_name']):

            # create series for bar
            overview_dic[mday]['sh_list'].append(datapoint['x'])
            overview_dic[mday]['team_list'].append(datapoint['logo_url'])
            overview_dic[mday]['sv_list'].append(datapoint['y'])

    return overview_dic
