# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
import math
from rest.functions.chartparameters import chartstyle, credit, exporting, title, subtitle, chart_color4, legend, font_size, variables_get, text_color, plotlines_color, responsive_y1

def shiftsperplayerchart_create(logger, ctitle, csubtitle, ismobile, data_dic, matchinfo_dic, color_dic):
    # pylint: disable=E0602, R0914
    """ create shift per player chart """
    logger.debug('shiftsperplayerchart_create()')

    variable_dic = variables_get(ismobile)

    if ismobile:
        img_width = 15
    else:
        img_width = 23


    chart_options = {
        'ctype': 'gantt',
        'chart': {
            'height': '110%',
            'alignTicks': 0,
            'style': chartstyle()
        },
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': {'enabled': 0},
        'exporting': exporting(filename=ctitle),
        'responsive': responsive_y1(),
        'plotOptions': {'series': {'states': {'inactive': {'opacity': 1}}}},

        'tooltip': {
            'useHTML': 0,
            'headerFormat': '',
            'pointFormat': '<b>{point.playername}</b><br>#{point.cnt} - {point.type}: {point.start_human}m - {point.end_human}m',
            'followPointer': 1,
        },

        'xAxis': [{
            'title': title(_('Game Time'), variable_dic['font_size']),
            'labels': {'align': 'center', 'style': {'fontSize': variable_dic['font_size']}},
            # 'categories': data_dic['x_list'],
            'tickInterval': 300000,
            'type': 'datetime',
            #'tickPositions':  data_dic['xtickposition_list'],
            'tickWidth': 1,
            'grid': {'enabled': 0},
            'opposite': 0,
            }],

        'yAxis': {
            'title': title('', font_size),
            'categories': data_dic['playername_list'],
            'labels': {'useHTML': 1, 'align': 'right', 'style': {'fontSize': variable_dic['font_size']}},
            'grid': {'enabled': 0},
            'plotLines': data_dic['y_plotlines_list']
            },

        'series': [
            {'name': ('Even Strength'), 'data': data_dic['shifts_list'], 'color': '#404040', 'marker': {'symbol': 'square'}},
        ]
    }
    return chart_options
