# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import chartstyle, credit, exporting, title, subtitle, font_size, variables_get, responsive_y1

def shiftsperplayerchart_create(logger, ctitle, csubtitle, ismobile, data_dic):
    # pylint: disable=E0602, R0914
    """ create shift per player chart """
    logger.debug('shiftsperplayerchart_create()')

    variable_dic = variables_get(ismobile)

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
            'tickInterval': 300000,
            'type': 'datetime',
            'tickWidth': 1,
            'grid': {'enabled': 0},
            'opposite': 0,
        }, {
            'title': title(_('Goals'), variable_dic['font_size'], offset=15),
            'tickPositions': [],
            'plotLines': data_dic['x2_plotlines_list'],
            'plotBands': data_dic['plotbands_list'],
            'tickWidth': 0,
            'grid': {'enabled': 0},
            'opposite': 1
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
