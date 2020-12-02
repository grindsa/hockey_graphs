# -*- coding: utf-8 -*-
""" list of functions for faceoff charts """
from rest.functions.chartparameters import exporting, title, credit, legend, responsive_y1
from rest.functions.chartparameters import plotlines_color, chart_color6, font_size

def faceoff_overview_chart(logger, ctitle, data_dic):
    """ create chart 5v5 pace """
    # pylint: disable=E0602
    logger.debug('faceoff_overview_chart()')

    chart_options = {

        'chart': {
            'type': 'scatter',
            'height': '60%'
        },

        'exporting': exporting(filename=ctitle),
        'title': title(''),
        'credits': credit(),
        'legend': legend(),
        'responsive': responsive_y1(),

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '',
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.sum_faceoffswon}</span><br><span style="font-size: %s">%s: {point.sum_faceoffslost}</span><br/><span style="font-size: %s">%s: {point.y}</span><br/>' % (font_size, _('Faceoffs won'), font_size, _('Faceoffs lost'), font_size, _('Faceoffs win percentage'))
        },

        'xAxis': {
            'labels': {
                'enabled': 0
            },
            'tickInterval': 0,
        },

        'yAxis': {
            'title': title(ctitle, font_size),
            # 'tickInterval': 1,
            'maxPadding': 0.1,
            'min': data_dic['y_min_minmax'] - 2,
            'max': data_dic['y_max_minmax'] + 2,
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': data_dic['y_avg'] - data_dic['y_deviation']/2, 'to': data_dic['y_avg'] + data_dic['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': data_dic['y_avg']}],
        },

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'data': data_dic['data']}]

    }

    return chart_options
