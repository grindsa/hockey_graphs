# -*- coding: utf-8 -*-
""" list of functions for special team performance """
# pylint: disable=E0401, C0413
from functions.helper import list_sumup, pctg_float_get
from functions.corsi import pace_chartseries_get
from rest.functions.chartparameters import chart_color6, plotlines_color, title, font_size, corner_annotations

def _goaliepull_sumup(logger, teamstat_dic):
    """ sum up faceoff statistics """
    logger.debug('_goaliepull_sumup()')

    update_amount = 0
    teamstat_sum_dic = {}

    for team_id in teamstat_dic:
        # sumup data per team
        teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'goalie_own_pull', 'goalie_other_pull', 'goals_en_for', 'goals_en_against', 'goals_wogoalie_for', 'goalie_own_pulltime'])
        # check how many items we have to create in update_dic
        if update_amount < len(teamstat_sum_dic[team_id]):
            update_amount = len(teamstat_sum_dic[team_id])

        # for ele in teamstat_sum_dic[team_id]:
        for idx, ele in enumerate(teamstat_sum_dic[team_id], 1):
            # add amount of games
            ele['games'] = idx
            # calculate pp/ppk
            # ele['goalie_own_pulltime_avg'] = round((ele['games'] * 3600 - ele['sum_goalie_own_pulltime'])/ ele['games'], 0)
            #ele['pk_pctg'] = 100 - pctg_float_get(ele['sum_goals_pp_against'], ele['sum_shcount'], 0)

    return (teamstat_sum_dic, update_amount)

def _pppk_sumup(logger, teamstat_dic):
    """ sum up faceoff statistics """
    logger.debug('_pppk_sumup()')

    update_amount = 0
    teamstat_sum_dic = {}

    for team_id in teamstat_dic:

        # sumup data per team
        teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'goals_pp', 'goals_pp_against', 'ppcount', 'shcount', 'penaltyminutes_drawn', 'penaltyminutes_taken'])
        # check how many items we have to create in update_dic
        if update_amount < len(teamstat_sum_dic[team_id]):
            update_amount = len(teamstat_sum_dic[team_id])

        # for ele in teamstat_sum_dic[team_id]:
        for idx, ele in enumerate(teamstat_sum_dic[team_id], 1):
            # add amount of games
            ele['games'] = idx
            # calculate pp/ppk
            ele['pp_pctg'] = pctg_float_get(ele['sum_goals_pp'], ele['sum_ppcount'], 0)
            ele['pk_pctg'] = 100 - pctg_float_get(ele['sum_goals_pp_against'], ele['sum_shcount'], 0)

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
    discipline_lake = {}

    for ele in range(1, update_amount+1):
        pppk_lake[ele] = []
        discipline_lake[ele] = []

    for team_id in pppksum_dic:
        # harmonize lengh by adding list elements at the beginning
        if len(pppksum_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(pppksum_dic[team_id])):
                pppksum_dic[team_id].insert(0, pppksum_dic[team_id][0])

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

            discipline_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(teams_dic[team_id]['team_logo'])},
                'penaltyminutes_drawn': ele['sum_penaltyminutes_drawn'],
                'penaltyminutes_taken': ele['sum_penaltyminutes_taken'],
                'x': round(ele['sum_penaltyminutes_drawn'] / ele['games'], 1),
                'y': round(ele['sum_penaltyminutes_taken'] / ele['games'], 1),
            })


    # build final dictionary
    pppk_chartseries_dic = pace_chartseries_get(logger, pppk_lake)
    discipline_chartseries_dic = pace_chartseries_get(logger, discipline_lake)

    return (pppk_chartseries_dic, discipline_chartseries_dic)

def discipline_updates_get(logger, data_dic, string_1=None, string_2=None, string_3=None, string_4=None, ismobile=False):
    # pylint: disable=E0602
    """ build structure for pdo breakdown chart """
    logger.debug('discipline_updates_get()')

    updates_dic = {}
    for ele in data_dic:
        minmax_dic = {
            'x_min': data_dic[ele]['x_min'] - 0.2,
            'y_min': data_dic[ele]['y_min'] - 0.2,
            'x_max': data_dic[ele]['x_max'] + 0.2,
            'y_max': data_dic[ele]['y_max'] + 0.2
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
                    'title': title(_('Penaltyminutes drawn (avg per game)'), font_size),
                    'min': minmax_dic['x_min'],
                    'max': minmax_dic['x_max'],
                    'tickInterval': 0.5,
                    'gridLineWidth': 1,
                    'plotBands': [{'from':  data_dic[ele]['x_avg'] -  data_dic[ele]['x_deviation']/2, 'to':  data_dic[ele]['x_avg'] +  data_dic[ele]['x_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value':  data_dic[ele]['x_avg']}],
                },
                'yAxis': {
                    'title': title(_('Penaltyminutes taken (avg per game)'), font_size),
                    'min': minmax_dic['y_min'],
                    'max': minmax_dic['y_max'],
                    'tickInterval': 0.5,
                    'gridLineWidth': 1,
                    # we use x_deviation on purpose to make data better comparable
                    'plotBands': [{'from':  data_dic[ele]['y_avg'] -  data_dic[ele]['x_deviation']/2, 'to':  data_dic[ele]['y_avg'] +  data_dic[ele]['x_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 3, 'value':  data_dic[ele]['y_avg']}],
                },
            }
        }
        if string_1 and string_2 and string_3 and string_4:
            updates_dic[ele]['chartoptions']['annotations'] = corner_annotations(ismobile, minmax_dic, string_1, string_2, string_3, string_4, 1)

    return updates_dic

def goaliepull_data(logger, ismobile, teamstat_dic, teams_dic):
    # pylint: disable=E0602
    """ build structure for pdo breakdown chart """
    logger.debug('goaliepull_data()')

    if ismobile:
        image_width = 25
        overview_width = 20
        overview_width = 20
    else:
        image_width = 40
        overview_width = 30
    image_height = image_width
    overview_height = overview_width

    (goaliepullsum_dic, update_amount) = _goaliepull_sumup(logger, teamstat_dic)

    goaliepull_lake = {}
    for ele in range(1, update_amount+1):
        goaliepull_lake[ele] = []

    for team_id in goaliepullsum_dic:
        logo_url = '<span><img src="{0}" alt="{1}" width="{2}" height="{3}"></span>'.format(teams_dic[team_id]['team_logo'], teams_dic[team_id]['shortcut'], overview_width, overview_height)

        # harmonize lengh by adding list elements at the beginning
        if len(goaliepullsum_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(goaliepullsum_dic[team_id])):
                goaliepullsum_dic[team_id].insert(0, goaliepullsum_dic[team_id][0])

        for idx, ele in enumerate(goaliepullsum_dic[team_id], 1):
            goaliepull_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(teams_dic[team_id]['team_logo'])},
                'sum_goalie_other_pull': ele['sum_goalie_other_pull'],
                'sum_goalie_own_pull': ele['sum_goalie_own_pull'],
                'sum_goals_en_against': ele['sum_goals_en_against'],
                'sum_goals_en_for': ele['sum_goals_en_for'],
                'sum_goals_wogoalie_for': ele['sum_goals_wogoalie_for'],
                'logo_url': logo_url,
                'goalie_own_pulltime_avg': round(ele['sum_goalie_own_pulltime'] / ele['games'], 0),
            })

    return goaliepull_lake

def goaliepullendata_get(logger, data_dic):
    """ collect data for pdo overview chart """
    logger.debug('pdo_overview_data_get()')

    output_dic = {}

    for mday in data_dic:
        output_dic[mday] = {'team_list': [], 'goals_en_against_list': [], 'goals_wogoalie_for_list': []}
        for datapoint in sorted(data_dic[mday], key=lambda i: i['team_name']):
            # create series for bar
            output_dic[mday]['team_list'].append(datapoint['logo_url'])
            output_dic[mday]['goals_en_against_list'].append({'y': datapoint['sum_goals_en_against'] * -1, 'team_name': datapoint['team_name'], 'goalie_own_pull': datapoint['sum_goalie_own_pull'], 'goals_en_against': datapoint['sum_goals_en_against'], 'goals_wogoalie_for': datapoint['sum_goals_wogoalie_for'], 'label': datapoint['sum_goals_en_against']})
            output_dic[mday]['goals_wogoalie_for_list'].append({'y': datapoint['sum_goals_wogoalie_for'], 'team_name': datapoint['team_name'], 'goalie_own_pull': datapoint['sum_goalie_own_pull'], 'goals_en_against': datapoint['sum_goals_en_against'], 'goals_wogoalie_for': datapoint['sum_goals_wogoalie_for'], 'label': datapoint['sum_goals_wogoalie_for']})
    return output_dic
