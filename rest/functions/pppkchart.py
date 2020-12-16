# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_y1, title, subtitle, font_size, plotlines_color, corner_annotations, variables_get, chart_color6

def pppk_chart_get(logger, ctitle, csubtitle, ismobile, pppk_data):
    # pylint: disable=E0602
    """ pdo breakdown """
    logger.debug('pdo_breakdown_chart()')

    variable_dic = variables_get(ismobile)

    # dirty hack
    if pppk_data['x_min'] == 0:
        pppk_data['x_min'] = 1
    if pppk_data['y_min'] == 0:
        pppk_data['y_min'] = 1
    if pppk_data['x_max'] == 100:
        pppk_data['x_max'] = 99
    if pppk_data['y_max'] == 100:
        pppk_data['y_max'] = 99

    minmax_dic = {
        'x_min': pppk_data['x_min'] - 1,
        'y_min': pppk_data['y_min'] - 1,
        'x_max': pppk_data['x_max'] + 1,
        'y_max': pppk_data['y_max'] + 1
    }

    chart_options = {

        'chart': {
            'type': 'scatter',
            'height': '120%',
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': {'enabled': 1},
        'responsive': responsive_y1(),

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '',
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.x}%s</span><br><span style="font-size: %s">%s: {point.y}%s</span><br/>' % (font_size, _('Shooting percentage (Sh%)'), '%', font_size, _('Save percentage (Sv%)'), '%s')
        },

        'xAxis': {
            'title': title(_('Powerplay percentage (Pp%)'), font_size),
            'labels': {'style': {'fontSize': font_size},},
            'min': minmax_dic['x_min'],
            'max': minmax_dic['x_max'],
            'tickInterval': 1,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'gridLineWidth': 1,
            'plotBands': [{'from': pppk_data['x_avg'] - pppk_data['x_deviation']/2, 'to': pppk_data['x_avg'] + pppk_data['x_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': pppk_data['x_avg']}],
        },

        'yAxis': {
            'title': title(_('Penalty Kill percentage (Pk%)'), font_size),
            'maxPadding': 0.1,
            'min': minmax_dic['y_min'],
            'max': minmax_dic['y_max'],
            'tickInterval': 1,
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': pppk_data['y_avg'] - pppk_data['y_deviation']/2, 'to': pppk_data['y_avg'] + pppk_data['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': pppk_data['y_avg']}],
        },

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'marker': {'symbol': 'square'}, 'data': pppk_data['data']}],
        'annotations': corner_annotations(ismobile, minmax_dic, _('Defensive'), _('Overstrained'), _('Agressive'), _('Offensive')),
    }
    return chart_options
