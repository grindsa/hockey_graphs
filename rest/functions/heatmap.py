# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
from functions.helper import list_sumup, pctg_float_get

def  _teampcomparison_data_sumup(logger, teamstat_dic):
    """ sumup data """
    logger.debug('teamcomparison_hmdata_get()')
    update_amount = 0
    teamstat_sum_dic = {}

    for team_id in teamstat_dic:
        # sumup data per team
        teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'shots_for_5v5', 'shots_against_5v5', 'shots_ongoal_for', 'shots_ongoal_against', 'goals_for', 'goals_against', 'saves', 'matchduration', 'faceoffswon', 'faceoffslost', 'rebounds_for', 'rebounds_against', 'goals_rebound_for', 'goals_rebound_against', 'breaks_for', 'breaks_against', 'goals_break_for', 'goals_break_against', 'goals_pp', 'goals_pp_against', 'ppcount', 'shcount'])

        # check how many items we have to create in update_dic
        if update_amount < len(teamstat_sum_dic[team_id]):
            update_amount = len(teamstat_sum_dic[team_id])

        for ele in teamstat_sum_dic[team_id]:
            # calculate 60 data
            ele['sum_shots_for_5v5_60'] = round(ele['sum_shots_for_5v5'] *  3600 / ele['sum_matchduration'], 0)
            ele['sum_shots_against_5v5_60'] = round(ele['sum_shots_against_5v5'] * 3600 / ele['sum_matchduration'], 0)
            ele['sum_corsi_5v5_60'] = ele['sum_shots_for_5v5_60'] - ele['sum_shots_against_5v5_60']
            ele['sum_shots_5v5_60'] = ele['sum_shots_for_5v5_60'] + ele['sum_shots_against_5v5_60']

            # calculate pdo
            ele['sh_pctg'] = pctg_float_get(ele['sum_goals_for'], ele['sum_shots_ongoal_for'])
            ele['sv_pctg'] = pctg_float_get(ele['sum_saves'], ele['sum_shots_ongoal_against'])

            # faceoff success rate
            ele['faceoff_success_rate'] = pctg_float_get(ele['sum_faceoffswon'], (ele['sum_faceoffswon'] + ele['sum_faceoffslost']), 1)

            # rebound rates
            ele['goals_rebound_for_pctg'] = pctg_float_get(ele['sum_goals_rebound_for'], ele['sum_rebounds_for'])
            ele['goals_rebound_against_pctg'] = pctg_float_get(ele['sum_goals_rebound_against'], ele['sum_rebounds_against'])

            # break rates
            ele['goals_break_for_pctg'] = pctg_float_get(ele['sum_goals_break_for'], ele['sum_breaks_for'])
            ele['goals_break_against_pctg'] = pctg_float_get(ele['sum_goals_break_against'], ele['sum_breaks_against'])

            # special team performance
            ele['goals_pp_for_pctg'] = pctg_float_get(ele['sum_goals_pp'], ele['sum_ppcount'])
            ele['goals_pp_kill_pctg'] = 100 - pctg_float_get(ele['sum_goals_pp_against'], ele['sum_shcount'])

    return (teamstat_sum_dic, update_amount)


def _teamcomparison_hm_chartseries_get(logger, data_dic):
    """ build structure for chart series """
    logger.debug('_rebound_chartseries_get()')
    chartseries_dic = {}

    y_category = [
        {'name': 'Cf/60', 'key': 'sum_shots_for_5v5_60'},
        {'name': 'Ca/60', 'key': 'sum_shots_against_5v5_60'},
        {'name': 'C/60', 'key': 'sum_corsi_5v5_60'},
        {'name': 'Pace', 'key': 'sum_shots_5v5_60'},
        {'name': 'Sh%', 'key': 'sh_pctg'},
        {'name': 'Sv%', 'key': 'sv_pctg'},
        {'name': 'FAC%', 'key': 'faceoff_success_rate'},
        {'name': 'Rb+%', 'key': 'goals_rebound_for_pctg'},
        {'name': 'Rb-%', 'key': 'goals_rebound_against_pctg'},
        {'name': 'Br+%', 'key': 'goals_break_for_pctg'},
        {'name': 'Br-%', 'key': 'goals_break_against_pctg'},
        {'name': 'PP%', 'key': 'goals_pp_for_pctg'},
        {'name': 'Pk%', 'key': 'goals_pp_kill_pctg'}
    ]

    for ele in data_dic:
        # foreach matchday
        chartseries_dic[ele] = {'x_category': [], 'y_category': [], 'data': []}
        for value in y_category:
            # create category list
            chartseries_dic[ele]['y_category'].append(value['name'])

        x_cnt = 0
        for datapoint in sorted(data_dic[ele], key=lambda i: i['team_name']):
            # short by team and add shortcut to x_val
            # chartseries_dic[ele]['x_category'].append(datapoint['shortcut'])
            y_cnt = 0
            # print(datapoint['logo'])
            for value in y_category:
                # go over datapoints
                # detect against bar (reverse color scheme needs to be applied)
                reverse = False
                if 'against' in y_category[y_cnt]['key']:
                    reverse = True
                # build data structure
                tmp_dic = {
                    'x': x_cnt,
                    'y': y_cnt,
                    'name': datapoint['name'],
                    'ovalue': datapoint[value['key']],
                    'y_name': y_category[y_cnt]['name'],
                    'reverse': reverse
                }
                y_cnt += 1
                chartseries_dic[ele]['data'].append(tmp_dic)
            x_cnt += 1

    for mday in chartseries_dic:
        chartseries_dic[mday]['data'] = _datapoint_reformat(chartseries_dic[mday]['data'])

    return chartseries_dic

def _datapoint_reformat(datapoint):
    """ reformat data to align against heatmap """

    _tmp_dic = {}
    # build initial dictionary
    for ele in datapoint:
        if ele['y'] not in _tmp_dic:
            _tmp_dic[ele['y']] = {'data': []}

        _tmp_dic[ele['y']]['data'].append(ele['ovalue'])

    # gget over dictionary to get mins and max
    for ele in _tmp_dic:
        _tmp_dic[ele]['max'] = max(_tmp_dic[ele]['data'])
        _tmp_dic[ele]['min'] = min(_tmp_dic[ele]['data'])

    for ele in datapoint:
        if ele['reverse']:
            # high values are bad (usually aginst values)
            ele['value'] = 100 - round((ele['ovalue'] - _tmp_dic[ele['y']]['min']) / (_tmp_dic[ele['y']]['max'] - _tmp_dic[ele['y']]['min']) * 100, 2)
        else:
            # low values are bad
            ele['value'] = round((ele['ovalue'] - _tmp_dic[ele['y']]['min']) / (_tmp_dic[ele['y']]['max'] - _tmp_dic[ele['y']]['min']) * 100, 2)

        ele['dataLabels'] = {'format': '{0}'.format(int(ele['ovalue']))}

    return datapoint


def teamcomparison_hmdata_get(logger, ismobile, teamstat_dic, teams_dic):
    """ get data for team heatmap """
    logger.debug('teamcomparison_hmdata_get()')

    # get summary
    (sumup_dic, update_amount) = _teampcomparison_data_sumup(logger, teamstat_dic)

    # build temporary dictionary for date. we build the final sorted in next step
    heatmap_lake = {}
    for ele in range(1, update_amount+1):
        heatmap_lake[ele] = []

    if ismobile:
        img_width = '20'
        img_height = '20'
    else:
        img_width = '30'
        img_height = '30'

    for team_id in sumup_dic:
        # harmonize lengh by adding list elements at the beginning
        if len(sumup_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(sumup_dic[team_id])):
                sumup_dic[team_id].insert(0, sumup_dic[team_id][0])

        for idx, ele in enumerate(sumup_dic[team_id], 1):
            heatmap_lake[idx].append({
                'team_logo': teams_dic[team_id]['team_logo'],
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'name': '<span><img src="{0}" alt="{1}" width="{2}" height="{3}"></span>'.format(teams_dic[team_id]['team_logo'], teams_dic[team_id]['shortcut'], img_width, img_height),
                'sum_shots_for_5v5_60': ele['sum_shots_for_5v5_60'],
                'sum_shots_against_5v5_60': ele['sum_shots_against_5v5_60'],
                'sum_shots_5v5_60': ele['sum_shots_5v5_60'],
                'sum_corsi_5v5_60': ele['sum_corsi_5v5_60'],
                'sh_pctg': ele['sh_pctg'],
                'sv_pctg': ele['sv_pctg'],
                'faceoff_success_rate': ele['faceoff_success_rate'],
                'goals_rebound_for_pctg': ele['goals_rebound_for_pctg'],
                'goals_rebound_against_pctg': ele['goals_rebound_against_pctg'],
                'goals_break_for_pctg': ele['goals_rebound_for_pctg'],
                'goals_break_against_pctg': ele['goals_rebound_against_pctg'],
                'goals_pp_for_pctg': ele['goals_pp_for_pctg'],
                'goals_pp_kill_pctg': ele['goals_pp_kill_pctg']
            })

    chart_options = _teamcomparison_hm_chartseries_get(logger, heatmap_lake)

    return chart_options

def teamcomparison_updates_get(logger, _title, ismobile, data_dic):
    """ prepare structure for updates """
    logger.debug('teamcomparison_updates_get()')

    if ismobile:
        border_width = 5
    else:
        border_width = 10

    updates_dic = {}
    for ele in data_dic:
        updates_dic[ele] = {
            'chartoptions':  {
                'series': [
                    # pylint: disable=E0602
                    {'marker': {'symbol': 'square'}, 'showInLegend': 0, 'data': data_dic[ele]['data'], 'borderWidth': border_width, 'borderColor': '#ffffff', 'dataLabels': {'enabled': 0}},
                ]
            }
        }

    return updates_dic
