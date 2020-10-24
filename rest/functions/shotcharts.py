# -*- coding: utf-8 -*-
""" list of functions for shots """
import math

# pylint: disable=R0914
def shotsumchart_create(logger, shot_sum_dic, shot_min_dic, goal_dic, plotline_list, machinfo_dic):
    """ create shotsum chart """
    logger.debug('shotsumchart_create()')

    minute_list = list(shot_sum_dic['home_team'].keys())
    home_team_bar = list(shot_min_dic['home_team'].values())
    visitor_team_bar = list(shot_min_dic['visitor_team'].values())

    home_team_spline = []
    for min_, value in shot_sum_dic['home_team'].items():
        if min_ in goal_dic['home_team'].keys():
            home_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'width': 22, 'height': 22, 'symbol': 'url({0})'.format(machinfo_dic['home_team_logo'])}})
        else:
            home_team_spline.append(value)

    visitor_team_spline = []
    for min_, value in shot_sum_dic['home_team'].items():
        if min_ in goal_dic['home_team'].keys():
            visitor_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'width': 22, 'height': 22, 'symbol': 'url({0})'.format(machinfo_dic['visitor_team_logo'])}})
        else:
            visitor_team_spline.append(value)

    # max value for left y axis
    y_left_max = max(home_team_bar)
    if y_left_max < max(visitor_team_bar):
        y_left_max = max(visitor_team_bar)

    # max value for right y axis
    y_right_tick_interval = 20
    y_right_max = max(list(shot_sum_dic['home_team'].values()))
    if y_right_max < max(list(shot_sum_dic['visitor_team'].values())):
        y_right_max = max(list(shot_sum_dic['visitor_team'].values()))
    # incorporate tick interval to ensure proper scaling
    y_right_max = math.ceil(y_right_max/y_right_tick_interval) * y_right_tick_interval

    title = ''
    chart_options = {

        'chart': {
            'type': 'column',
            'height': '60%',
            'alignTicks': 0,
        },

        'exporting': {
            'chartOptions': {
                'plotOptions': {
                    'series': {
                        'dataLabels': {
                            'enabled': 0,
                        },
                    },
                },
            },
            'fallbackToExportServer': 0,
        },

        'title': {
            'text': title,
            'style': {'color': '#404040', 'font-size': '12px'},
        },

        'legend': {
            'enabled': 1,
            'useHTML': 1,
            'itemStyle': {'color': '#404040', 'font-size': '10px'},
            'verticalAlign': 'bottom',
            'symbolRadius': 0,
        },

        'tooltip': {
            'shared': 1,
            'useHTML': 1,
            'headerFormat': '<b>{point.x}.Minute</b><br>',
        },

        'plotOptions': {
            'spline': {
                'marker': {
                    'enabled': 0,
                },
            },
        },

        'xAxis': {
            'categories': minute_list,
            'title': {
                'text': 'Minute',
                'style': {'color': '#404040', 'font-size': '10px'},
            },
            'labels': {'style': {'fontSize': '10px'},},
            'tickInterval': 5,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'plotLines': [{
                'color': '#d8d9da',
                'width': 2,
                'value': 20,
            }, {
                'color': '#d8d9da',
                'width': 2,
                'value': 40,
            }, {
                'color': '#d8d9da',
                'width': 2,
                'value': 60,
            }],
            'plotBands': plotline_list,
        },

        'yAxis': [
            {
                'title': {
                    'text': 'Schüsse pro Minute',
                    'style': {'color': '#404040', 'font-size': '10px'},
                },
                #'max': y1_max,
                'tickInterval': 1,
                'maxPadding': 0.1,
                'labels': {'style': {'fontSize': '10px'},},
            }, {
                'title': {
                    'text': 'Schüsse gesamt',
                    'style': {'color': '#030357', 'font-size': '10px'},
                },
                'opposite': 1,
                'max': y_right_max,
                'labels': {'style': {'fontSize': '10px'}}}],

        'series': [{
            'name': '{0} pro min'.format(machinfo_dic['home_team__shortcut']),
            'data': home_team_bar,
            'color': '#7cb5ec',
        }, {
            'name': '{0} pro min'.format(machinfo_dic['visitor_team__shortcut']),
            'data': visitor_team_bar,
            'color': '#b0b3b5',
        }, {
            'type': 'spline',
            'name': '{0} Sum'.format(machinfo_dic['home_team__shortcut']),
            'data': home_team_spline,
            'color': '#030357',
            'yAxis': 1,
            'zIndex': 3,
        }, {
            'type': 'spline',
            'name': '{0} Sum'.format(machinfo_dic['visitor_team__shortcut']),
            'data': visitor_team_spline,
            'color': '#68717a',
            'yAxis': 1,
            'zIndex': 2,
        }, {
            'name': 'PP {0}'.format(machinfo_dic['home_team__shortcut']),
            'color': '#e6e6fe',
            'marker': {'symbol': 'square'},
        }, {
            'name': 'PP {0}'.format(machinfo_dic['visitor_team__shortcut']),
            'color': '#f1f2f3',
            'marker': {'symbol': 'square'},
        }]
    }

    return chart_options
