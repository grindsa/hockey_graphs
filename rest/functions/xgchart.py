# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_y1, title, legend, subtitle, font_size, font_size_mobile, plotlines_color, corner_annotations, variables_get, chart_color6, color_axis

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

    minmax_dic = {
        'x_min': xgfa_data['x_min'] - 0.2,
        'y_min': xgfa_data['y_min'] - 0.2,
        'x_max': xgfa_data['x_max'] + 0.2,
        'y_max': xgfa_data['y_max'] + 0.2
    }

    chart_options = {

        'chart': {
            'type': 'scatter',
            'height': '100%',
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
            'tickInterval': 0.25,
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
            'tickInterval': 0.25,
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

def gfxgf_chart_get(logger, ctitle, csubtitle, ismobile, gfxgf_data):
    # pylint: disable=E0602
    """ pdo breakdown """
    logger.debug('pdo_breakdown_chart()')

    variable_dic = variables_get(ismobile)

    # dirty hack
    if gfxgf_data['x_min'] == 0:
        gfxgf_data['x_min'] = 1
    if gfxgf_data['y_min'] == 0:
        gfxgf_data['y_min'] = 1
    if gfxgf_data['x_max'] == 100:
        gfxgf_data['x_max'] = 99
    if gfxgf_data['y_max'] == 100:
        gfxgf_data['y_max'] = 99

    minmax_dic = {
        'x_min': int(round(gfxgf_data['x_min'], 0)) - 5,
        'y_min': int(round(gfxgf_data['y_min'], 0)) - 2.5,
        'x_max': int(round(gfxgf_data['x_max'], 0)) + 5,
        'y_max': int(round(gfxgf_data['y_max'], 0)) + 5,
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
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.x}</span><br><span style="font-size: %s">%s: {point.y}</span><br/>' % (font_size, _('GF%'), font_size, _('xGF%'))
        },

        'xAxis': {
            'title': title(_('Goals percentage on 5v5 (Gf%)'), font_size),
            'labels': {'style': {'fontSize': font_size},},
            'min': minmax_dic['x_min'],
            'max': minmax_dic['x_max'],
            #'tickInterval': 2,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'gridLineWidth': 1,
            'plotBands': [{'from': gfxgf_data['x_avg'] - gfxgf_data['x_deviation']/2, 'to': gfxgf_data['x_avg'] + gfxgf_data['x_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': gfxgf_data['x_avg']}],
        },

        'yAxis': {
            'title': title(_('expected Goals percentage on 5v5 (xGf%)'), font_size),
            'maxPadding': 0.1,
            'min': minmax_dic['y_min'],
            'max': minmax_dic['y_max'],
            #'tickInterval': 2,
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': gfxgf_data['y_avg'] - gfxgf_data['y_deviation']/2, 'to': gfxgf_data['y_avg'] + gfxgf_data['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': gfxgf_data['y_avg']}],
        },

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'marker': {'symbol': 'square'}, 'data': gfxgf_data['data']}],
        'annotations': corner_annotations(ismobile, minmax_dic, _('Underperforming'), _('Bad'), _('Good'), _('Overperforming')),
    }
    return chart_options

def dgf_chart_get(logger, ctitle, csubtitle, ismobile, data_dic):
    # pylint: disable=E0602
    """ pdo overview """
    logger.debug('pdo_overview_chart()')

    variable_dic = variables_get(ismobile)

    if ismobile:
        chart_height = '100%'
        legent_title_size = font_size_mobile
    else:
        chart_height = '80%'
        legent_title_size = font_size

    chart_options = {
        'chart': {
            'type': 'column',
            'height': chart_height,
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(1, {'title': {'text': 'GF%', 'style': {'fontSize': legent_title_size}}}),
        'responsive': responsive_y1(),

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '',
            'pointFormat': '<span><b>{point.shortcut}</b></span></br><span style="font-size: %s">%s: {point.gf_pctg}</span><br><span style="font-size: %s">%s: {point.y}</span><br/>' % (font_size, _('GF%'), font_size, _('dGF%'))
        },


        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': 1,
                    'useHTML': 0,
                    'style': {'fontSize': font_size, 'textOutline': 0, 'color': '#ffffff', 'fontWeight': 0}
                }
            }
        },

        'xAxis': {
            'categories': data_dic['data']['team_list'],
            'title': title('', font_size),
            'labels': {'useHTML': 1, 'align': 'center'},
        },

        'colorAxis': color_axis(showinlegend=1, minimum=data_dic['gf_5v5_pctg_min']),
        'yAxis': {
            # pylint: disable=E0602
            'title': title(_('Difference of GF% and xGF% (dGF%)'), font_size),
            'labels': {'style': {'fontSize': font_size}},
            'plotLines': [{'color': plotlines_color, 'width': 2, 'value': 100}],
        },

        'series': [
            # pylint: disable=E0602
            {'name': _('dGF%'), 'marker': {'symbol': 'square'}, 'data': data_dic['data']['dgf_list']},
        ]
    }

    return chart_options
