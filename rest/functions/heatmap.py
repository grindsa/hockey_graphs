# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
from functions.helper import list_sumup

def  _teampcomparison_data_sumup(logger, teamstat_dic):
    """ sumup data """
    logger.debug('teamcomparison_hmdata_get()')
    update_amount = 0
    teamstat_sum_dic = {}

    for team_id in teamstat_dic:
        # sumup data per team
        teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'shots_for_5v5', 'shots_against_5v5', 'shots_ongoal_for', 'shots_ongoal_against', 'goals_for', 'goals_against', 'saves', 'matchduration'])
        # check how many items we have to create in update_dic
        if update_amount < len(teamstat_sum_dic[team_id]):
            update_amount = len(teamstat_sum_dic[team_id])

        for ele in range(1, update_amount+1):
            # we nbeed to add the 60 data
            sum_shots_for_5v5 = teamstat_sum_dic[team_id][ele-1]['sum_shots_for_5v5']
            sum_shots_against_5v5 = teamstat_sum_dic[team_id][ele-1]['sum_shots_against_5v5']
            sum_matchduration = teamstat_sum_dic[team_id][ele-1]['sum_matchduration']

            # calculate 60
            teamstat_sum_dic[team_id][ele-1]['sum_shots_for_5v5_60'] = round(sum_shots_for_5v5 *  3600 / sum_matchduration, 0)
            teamstat_sum_dic[team_id][ele-1]['sum_shots_against_5v5_60'] = round(sum_shots_against_5v5 * 3600 / sum_matchduration, 0)
            teamstat_sum_dic[team_id][ele-1]['sum_shots_5v5_60'] = teamstat_sum_dic[team_id][ele-1]['sum_shots_for_5v5_60'] + teamstat_sum_dic[team_id][ele-1]['sum_shots_against_5v5_60']

    return (teamstat_sum_dic, update_amount)


def _teamcomparison_hm_chartseries_get(logger, data_dic, minmax=False):
    """ build structure for chart series """
    logger.debug('_rebound_chartseries_get()')
    chartseries_dic = {}

    y_category = [
        {'name': 'Cf/60', 'key': 'sum_shots_for_5v5_60'},
        {'name': 'Ca/60', 'key': 'sum_shots_against_5v5_60'},
        {'name': 'Pace', 'key': 'sum_shots_5v5_60'}
    ]

    for ele in data_dic:
        # foreach matchday
        chartseries_dic[ele] = {'x_category': [], 'y_category': [], 'data': []}
        for value in y_category:
            # create category list
            chartseries_dic[ele]['y_category'].append(value['name'])

        x_cnt = 0
        for datapoint in sorted(data_dic[ele], key=lambda i: i['shortcut']):
            # short by team and add shortcut to x_val
            chartseries_dic[ele]['x_category'].append(datapoint['shortcut'])
            y_cnt = 0
            for value in y_category:
                # go over datapoints
                tmp_dic = {
                    'x': x_cnt,
                    'y': y_cnt,
                    'ovalue': datapoint[value['key']],
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

    for team_id in sumup_dic:
        # harmonize lengh by adding list elements at the beginning
        if len(sumup_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(sumup_dic[team_id])):
                sumup_dic[team_id].insert(0, sumup_dic[team_id][0])

        for idx, ele in enumerate(sumup_dic[team_id], 1):
            heatmap_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'sum_shots_for_5v5_60': ele['sum_shots_for_5v5_60'],
                'sum_shots_against_5v5_60': ele['sum_shots_against_5v5_60'],
                'sum_shots_5v5_60': ele['sum_shots_5v5_60'],
            })

    chart_options = _teamcomparison_hm_chartseries_get(logger, heatmap_lake)

    return chart_options
