# -*- coding: utf-8 -*-
""" list of functions for shots """
import math
from rest.functions.chartparameters import exporting, plotoptions_spline, title, legend, tooltip, labels, font_size, text_color, plotlines_color, chart_color1, chart_color2, chart_color3, chart_color4, chart_color5, chart_color6


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
    for min_, value in shot_sum_dic['visitor_team'].items():
        if min_ in goal_dic['visitor_team'].keys():
            visitor_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(machinfo_dic['visitor_team_logo'])}})
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

    chart_options = {

        'chart': {
           'type': 'column',
            'height': '60%',
            'alignTicks': 0,
        },

        'exporting': exporting(),
        'title': title(''),
        'legend': legend(),
        'tooltip': tooltip('<b>{point.x}.Minute</b><br>'),
        'plotOptions': plotoptions_spline(),

        'xAxis': {
            'categories': minute_list,
            'title': {
                'text': 'Minute',
                'style': {'color': text_color, 'font-size': font_size},
            },
            'labels': {'style': {'fontSize': font_size}},
            'tickInterval': 5,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'plotLines': [
                {'color': plotlines_color, 'width': 2, 'value': 20},
                {'color': plotlines_color, 'width': 2, 'value': 40},
                {'color': plotlines_color, 'width': 2, 'value': 60}
                ],
            'plotBands': plotline_list,
        },

        'yAxis': [
            {
                'title': title('Schüsse pro Minute', font_size),
                #'max': y1_max,
                'tickInterval': 1,
                'maxPadding': 0.1,
                'labels': labels(),
            }, {
                'title': title('Schüsse gesamt', font_size),
                'opposite': 1,
                'max': y_right_max,
                'labels': labels()
            }],

        'series': [{
            'name': '{0} pro min'.format(machinfo_dic['home_team__shortcut']),
            'data': home_team_bar,
            'color': chart_color1,
        }, {
            'name': '{0} pro min'.format(machinfo_dic['visitor_team__shortcut']),
            'data': visitor_team_bar,
            'color': chart_color2,
        }, {
            'type': 'spline',
            'name': '{0} Sum'.format(machinfo_dic['home_team__shortcut']),
            'data': home_team_spline,
            'color': chart_color3,
            'yAxis': 1,
            'zIndex': 3,
        }, {
            'type': 'spline',
            'name': '{0} Sum'.format(machinfo_dic['visitor_team__shortcut']),
            'data': visitor_team_spline,
            'color': chart_color4,
            'yAxis': 1,
            'zIndex': 2,
        }, {
            'name': 'PP {0}'.format(machinfo_dic['home_team__shortcut']),
            'color': chart_color5,
            'marker': {'symbol': 'square'},
        }, {
            'name': 'PP {0}'.format(machinfo_dic['visitor_team__shortcut']),
            'color': chart_color6,
            'marker': {'symbol': 'square'},
        }]
    }

    return chart_options
