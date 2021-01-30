# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_y1, title, subtitle, legend, font_size, plotlines_color, corner_annotations, variables_get
from rest.functions.chartparameters import chart_color1, chart_color3, chart_color6

def pdo_overview_chart(logger, ctitle, csubtitle, ismobile, pdo_dic):
    """ pdo overview """
    logger.debug('pdo_overview_chart()')

    variable_dic = variables_get(ismobile)

    chart_options = {
        'chart': {
            'type': 'bar',
            'height': '120%',
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        'responsive': responsive_y1(),
        'tooltip': {'enabled': 0},

        'plotOptions': {
            'series': {
                'states': {'inactive': {'opacity': 1}},
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': 1,
                    'useHTML': 0,
                    'style': {'fontSize': font_size, 'textOutline': 0, 'color': '#ffffff', 'fontWeight': 0}
                }
            }
        },

        'xAxis': {
            'categories': pdo_dic['team_list'],
            'title': title('', font_size),
            'labels': {'useHTML': 1, 'align': 'center'},
            # 'labels': {'style': {'fontSize': font_size}},
        },

        'yAxis': {
            # pylint: disable=E0602
            'title': title(_('PDO'), font_size),
            'reversedStacks': 0,
            'labels': {'style': {'fontSize': font_size}},
            'min': 50,
            'plotLines': [{'color': plotlines_color, 'width': 2, 'value': 100}],
        },

        'series': [
            # pylint: disable=E0602
            {'name': _('Save percentage (Sv%)'), 'marker': {'symbol': 'square'}, 'data': pdo_dic['sv_list'], 'color': chart_color3},
            {'name': _('Shooting percentage (Sh%)'), 'marker': {'symbol': 'square'}, 'data': pdo_dic['sh_list'], 'color': chart_color1},
        ]
    }

    return chart_options

def pdo_breakdown_chart(logger, ctitle, csubtitle, ismobile, pdo_list):
    # pylint: disable=E0602
    """ pdo breakdown """
    logger.debug('pdo_breakdown_chart()')

    variable_dic = variables_get(ismobile)

    minmax_dic = {
        'x_min': round(pdo_list['x_min'] - 1, 0),
        'y_min': round(pdo_list['y_min'] - 1, 0),
        'x_max': round(pdo_list['x_max'] + 1, 0),
        'y_max': round(pdo_list['y_max'] + 1, 0)
        }

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
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.x}%s</span><br><span style="font-size: %s">%s: {point.y}%s</span><br/>' % (font_size, _('Shooting percentage (Sh%)'), '%', font_size, _('Save percentage (Sv%)'), '%s')
        },

        'xAxis': {
            'title': title(_('Shooting percentage (Sh%)'), font_size),
            'labels': {'style': {'fontSize': font_size},},
            'tickInterval': 1,
            'min': minmax_dic['x_min'],
            'max': minmax_dic['x_max'],
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
            'min': minmax_dic['y_min'],
            'max': minmax_dic['y_max'],
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': pdo_list['y_avg'] - pdo_list['y_deviation']/2, 'to': pdo_list['y_avg'] + pdo_list['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': pdo_list['y_avg']}],
        },

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'marker': {'symbol': 'square'}, 'data': pdo_list['data']}],
        'annotations': corner_annotations(ismobile, minmax_dic, _('Dull'), _('Unlucky'), _('Lucky'), _('Fun')),
    }
    return chart_options

def ppg_chart_get(logger, ctitle, csubtitle, ismobile, ppg_data):
    # pylint: disable=E0602
    """ points per game / shotpercentage breakdown"""
    logger.debug('ppg_chart_get()')

    variable_dic = variables_get(ismobile)

    # dirty hack
    if ppg_data['y_min'] == 0:
        ppg_data['y_min'] = 1
    if ppg_data['y_max'] == 100:
        ppg_data['y_max'] = 99

    chart_options = {

        'chart': {
            'type': 'scatter',
            'height': '80%',
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
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.y}</span><br><span style="font-size: %s">%s: {point.games}</span><br/><span style="font-size: %s">%s: {point.points}</span><br/>' % (font_size, _('Points per Game'), font_size, _('Matches'), font_size, _('Points'))
        },

        'xAxis': {
            'labels': {
                'enabled': 0
            },
            'tickInterval': 0,
        },

        'yAxis': {
            'title': title(_('Point per Game (Ppg)'), font_size),
            'maxPadding': 0.1,
            'min': 0,
            'tickInterval': 0.5,
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': ppg_data['y_avg'] - ppg_data['y_deviation']/2, 'to': ppg_data['y_avg'] + ppg_data['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': ppg_data['y_avg']}],
        },

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'marker': {'symbol': 'square'}, 'data': ppg_data['data']}],
    }
    return chart_options
