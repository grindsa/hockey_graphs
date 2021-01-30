# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import chartstyle, credit, exporting, legend, responsive_y1, title, subtitle, font_size, responsive_y1_nolabel, plotlines_color, corner_annotations, variables_get, chart_color6, chart_color1, chart_color3

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

def discipline_chart_get(logger, ctitle, csubtitle, ismobile, pppk_data):
    # pylint: disable=E0602
    """ pdo breakdown """
    logger.debug('discipline_chart_get()')

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
        'x_min': pppk_data['x_min'] - 0.2,
        'y_min': pppk_data['y_min'] - 0.2,
        'x_max': pppk_data['x_max'] + 0.2,
        'y_max': pppk_data['y_max'] + 0.2
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
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.penaltyminutes_drawn}min</span><br><span style="font-size: %s">%s: {point.penaltyminutes_taken}min</span><br/>' % (font_size, _('Penaltyminutes drawn'), font_size, _('Penaltyminutes taken'))
        },

        'xAxis': {
            'title': title(_('Penaltyminutes drawn (avg per game)'), font_size),
            'labels': {'style': {'fontSize': font_size},},
            'min': minmax_dic['x_min'],
            'max': minmax_dic['x_max'],
            'tickInterval': 0.5,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'gridLineWidth': 1,
            'plotBands': [{'from': pppk_data['x_avg'] - pppk_data['x_deviation']/2, 'to': pppk_data['x_avg'] + pppk_data['x_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': pppk_data['x_avg']}],
        },

        'yAxis': {
            'title': title(_('Penaltyminutes taken (avg per game)'), font_size),
            'maxPadding': 0.1,
            'min': minmax_dic['y_min'],
            'max': minmax_dic['y_max'],
            'tickInterval': 0.5,
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': pppk_data['y_avg'] - pppk_data['x_deviation']/2, 'to': pppk_data['y_avg'] + pppk_data['x_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': pppk_data['y_avg']}],
        },

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'marker': {'symbol': 'square'}, 'data': pppk_data['data']}],
        'annotations': corner_annotations(ismobile, minmax_dic, _('Undisciplined'), _('Friendly'), _('Chippy'), _('Disciplined'), 1)
    }
    return chart_options

def goaliepullchart_get(logger, ctitle, csubtitle, ismobile, data_dic):
    # pylint: disable=E0602, R0914
    """ create time-on-ice chart """
    logger.debug('gametoichart_create()')

    variable_dic = variables_get(ismobile)

    chart_options = {
        'chart': {
            'type': 'column',
            'height': '80%',
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        'responsive': responsive_y1_nolabel(),
        'tooltip': {
            'sharted': 1,
            'useHTML': 1,
            'headerFormat': '',
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.goalie_own_pull}</span><br><span style="font-size: %s">%s: {point.goals_wogoalie_for}</span><br/><span style="font-size: %s">%s: {point.goals_en_against}</span><br/>' % (font_size, _('Goalie pulls'), font_size, _('Goals after pulling goalie'), font_size, _('Empty net goals taken'))
        },

        'plotOptions': {
            'series': {
                'states': {'inactive': {'opacity': 1}},
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': 1,
                    'inside': 1,
                    'style': {'fontSize': font_size, 'textOutline': 0, 'color': '#ffffff', 'fontWeight': 0},
                    'format': '{point.label}'
                }
            }
        },

        'xAxis': {
            'categories': data_dic['team_list'],
            'title': title('', font_size),
            'labels': {'useHTML': 1, 'align': 'center'},
            # 'labels': {'style': {'fontSize': font_size}},
        },

        'yAxis': {
            # pylint: disable=E0602
            'title': title('', font_size),
            'reversedStacks': 0,
            'tickInterval': 1,
            'labels': {'enabled': 0, 'style': {'fontSize': font_size}},
            'plotLines': [{'color': plotlines_color, 'width': 2, 'value': 100}],
        },

        'series': [
            # pylint: disable=E0602
            {'name': _('Goals after pulling goalie'), 'marker': {'symbol': 'square'}, 'data': data_dic['goals_wogoalie_for_list'], 'color': chart_color3},
            {'name': _('Emptynet goals taken'), 'marker': {'symbol': 'square'}, 'data': data_dic['goals_en_against_list'], 'color': chart_color1},
        ]
    }

    return chart_options
