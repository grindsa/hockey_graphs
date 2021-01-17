# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_y1, title, subtitle, font_size, plotlines_color, corner_annotations, variables_get, chart_color6

def xgfa_chart_get(logger, ctitle, csubtitle, ismobile, xgfa_data):
    # pylint: disable=E0602
    """ pdo breakdown """
    logger.debug('pdo_breakdown_chart()')

    variable_dic = variables_get(ismobile)

    # dirty hack
    if xgfa_data['x_min'] == 0:
        xgfa_data['x_min'] = 1
    if xgfa_data['y_min'] == 0:
        xgfa_data['y_min'] = 1
    if xgfa_data['x_max'] == 100:
        xgfa_data['x_max'] = 99
    if xgfa_data['y_max'] == 100:
        xgfa_data['y_max'] = 99

    minmax_dic = {
        'x_min': xgfa_data['x_min'] - 0.2,
        'y_min': xgfa_data['y_min'] - 0.2,
        'x_max': xgfa_data['x_max'] + 0.2,
        'y_max': xgfa_data['y_max'] + 0.2
    }

    print(minmax_dic)

    chart_options = {

        'chart': {
            'type': 'scatter',
            'height': '110%',
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
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.x}</span><br><span style="font-size: %s">%s: {point.y}</span><br/>' % (font_size, _('xGF60'), font_size, _('xGA60'))
        },

        'xAxis': {
            'title': title(_('Expected Goals "For" per 60min (xGF60)'), font_size),
            'labels': {'style': {'fontSize': font_size},},
            'min': minmax_dic['x_min'],
            'max': minmax_dic['x_max'],
            'tickInterval': 0.5,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'gridLineWidth': 1,
            'plotBands': [{'from': xgfa_data['x_avg'] - xgfa_data['x_deviation']/2, 'to': xgfa_data['x_avg'] + xgfa_data['x_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': xgfa_data['x_avg']}],
        },

        'yAxis': {
            'title': title(_('Expected Goals "Against" per 60min (xGA60)'), font_size),
            'maxPadding': 0.1,
            'min': minmax_dic['y_min'],
            'max': minmax_dic['y_max'],
            'tickInterval': 0.5,
            'reversed': 1,
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': xgfa_data['y_avg'] - xgfa_data['y_deviation']/2, 'to': xgfa_data['y_avg'] + xgfa_data['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': xgfa_data['y_avg']}],
        },

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'marker': {'symbol': 'square'}, 'data': xgfa_data['data']}],
        'annotations': corner_annotations(ismobile, minmax_dic, _('Headless'), _('Boring'), _('Exciting'), _('Coolly')),
    }
    return chart_options
