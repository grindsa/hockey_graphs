# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import credit, exporting, responsive_y1, title, legend, font_size, plotlines_color
from rest.functions.chartparameters import chart_color1, chart_color2, chart_color3, chart_color4, chart_color6, text_color, font_size_mobile

def pdo_breakdown_chart(logger, ctitle, pdo_list):
    # pylint: disable=E0602
    """ create time-on-ice chart """
    logger.debug('pdo_breakdown_chart()')


    # print(pdo_list['x_avg'], pdo_list['x_deviation'], pdo_list['y_avg'], pdo_list['y_deviation'])

    chart_options = {

        'chart': {
            'type': 'scatter',
            'height': '100%',
        },

        'exporting': exporting(filename=ctitle),
        'title': title(''),
        'credits': credit(),
        'legend': {'enabled': 0},
        'responsive': responsive_y1(),

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '',
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.x}%s</span><br><span style="font-size: %s">%s: {point.y}%s</span><br/>' % (font_size, _('Shooting percentage (Sh%)'), '%', font_size, _('Save percentage (Sv%)'), '%s')
        },

        'xAxis': {
            'title': title(_('Shooting percentage (Sh%)'), font_size),
            'labels': {'style': {'fontSize': font_size},},
            'tickInterval': 1,
            'min': pdo_list['x_min'] - 1,
            'max': pdo_list['x_max'] + 1,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'gridLineWidth': 1,
            'plotBands': [{'from': pdo_list['x_avg'] - pdo_list['x_deviation']/2, 'to': pdo_list['x_avg'] + pdo_list['x_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': pdo_list['x_avg']}],
        },

        'yAxis': {
            'title': title(_('Save percentage (Sv%)'), font_size),
            'tickInterval': 1,
            'maxPadding': 0.1,
            'min': pdo_list['y_min'] - 1,
            'max': pdo_list['y_max'] + 1,
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': pdo_list['y_avg'] - pdo_list['y_deviation']/2, 'to': pdo_list['y_avg'] + pdo_list['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': pdo_list['y_avg']}],
        },

        'series': [{'data': pdo_list['data']}]

    }
    return chart_options
