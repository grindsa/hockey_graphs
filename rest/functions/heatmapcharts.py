# -*- coding: utf-8 -*-
""" list of functions for heatmaps """
# pylint: disable=E0401
from rest.functions.chartparameters import variables_get, text_color, font_size, credit, exporting, title, subtitle, color_axis, text_color, title_font_size, title_font_size_mobile, title_font_size_mobile, subtitle_font_size, chartstyle

def teamcomparison_chart_get(logger, ctitle, csubtitle, ismobile, data_dic):
    """ team comparison heatmap chart """
    logger.debug('teamcomparison_chart_get()')

    variable_dic = variables_get(ismobile)

    chart_options = {

        'chart': {
            'type': 'heatmap',
            'height': '110%',
            'inverted': 1,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle, allowhtml=0),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
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

        'legend': {
            'align': 'center',
            'layout': 'horizontal',
            'verticalAlign': 'bottom',
            'useHTML': 0,
            'itemStyle': {'color': text_color, 'font-size': font_size},
        },

        'colorAxis': color_axis(showinlegend=0),

        'series': [{
            'marker': {'symbol': 'square'},
            'borderWidth': variable_dic['border_width'],
            'borderColor': '#ffffff',
            'data': data_dic['data'],
            'showInLegend': 0,
            'dataLabels': {'enabled': 0}
        }],
    }

    return chart_options
