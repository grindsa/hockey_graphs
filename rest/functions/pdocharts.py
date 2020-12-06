# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_y1, title, subtitle, legend, font_size, plotlines_color, corner_annotations, variables_get
from rest.functions.chartparameters import chart_color1, chart_color2, chart_color3, chart_color4, chart_color6, text_color, font_size_mobile

def pdo_overview_chart(logger, ctitle, csubtitle, ismobile, pdo_dic):
    """ pdo overview """

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
            'title': title(_('PDO'), font_size),
            'reversedStacks': 0,
            'labels': {'style': {'fontSize': font_size}},
            'min': 50,
            'plotLines': [{'color': plotlines_color, 'width': 2, 'value': 100}],
        },

        'series': [
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

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'marker': {'symbol': 'square'}, 'data': pdo_list['data']}],
        'annotations': corner_annotations(ismobile, _('Dull'), _('Unlucky'), _('Lucky'), _('Fun')),
    }
    return chart_options
