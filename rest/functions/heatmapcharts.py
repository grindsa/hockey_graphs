# -*- coding: utf-8 -*-
""" list of functions for heatmaps """
# pylint: disable=E0401
from rest.functions.chartparameters import credit, exporting, title, color_axis, text_color

def teamcomparison_chart_get(logger, ctitle, ismobile, data_dic):
    """ team comparison heatmap chart """
    logger.debug('teamcomparison_chart_get()')

    if ismobile:
        border_width = 5
    else:
        border_width = 10

    chart_options = {

        'chart': {
            'type': 'heatmap',
            'height': '90%',
            'inverted': 1,
        },

        'exporting': exporting(filename=ctitle, allowhtml=0),
        'title': title(''),
        'credits': credit(),

        'xAxis': {
            'categories': data_dic['x_category'],
            'type': 'category',
            'labels': {'useHTML': 1, 'align': 'center'}
        },

        'yAxis': {
            'categories': data_dic['y_category'],
            'title': '',
            'opposite':1,
        },

        'tooltip': {
            'headerFormat': '',
            'pointFormat': '<b>{point.y_name}</b>: {point.ovalue}',
            'split': 1,
        },

        'colorAxis': color_axis(),

        'legend': {
            'enabled': 0
        },

        'series': [{
            'name': '',
            # 'borderWidth': 1,
            # 'borderColor': '#000000',
            'borderWidth': border_width,
            'borderColor': '#ffffff',
            'data': data_dic['data'],
            'dataLabels': {
                'enabled': 0,
                'useHTML': 0,
                'style': {'fontSize': '8px', 'textOutline': 0, 'color': text_color}
            }
        }],
    }

    return chart_options
