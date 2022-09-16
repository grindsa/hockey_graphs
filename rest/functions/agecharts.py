# -*- coding: utf-8 -*-
""" functions to feed age-charts """
from logging import Formatter
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_y1, title, subtitle, legend, font_size, plotlines_color, corner_annotations, variables_get
from rest.functions.chartparameters import chart_color1, chart_color2, chart_color3, chart_color5, chart_color6, chart_color7, line_color, linetrans_color


def age_overviewchart_get(logger, ctitle, csubtitle, ismobile, agedate_dic):
    """ create chart showing age per teams """
    logger.debug('age_overviewchart_get()')

    variable_dic = variables_get(ismobile)


    x_list = []
    age_list = []
    scatter_list = []
    cnt = 0
    for team in sorted(agedate_dic, key=lambda x: x['shortcut']):
        x_list.append(team['logo'])
        age_list.append({'name': team['shortcut'], 'low': team['y'][0], 'high': team['y'][2]})
        scatter_list.append({'x': cnt, 'y': team['y'][1]})
        cnt += 1

    chart_options = {
        'chart': {
            'type': 'dumbbell',
            'height': '75%',
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        #'responsive': responsive_y1(),
        'tooltip': {'enabled': 0},

        'plotOptions': {
            'dumbbell': {'lineColor': '#ff0000'},
            'series': {
                'states': {'inactive': {'opacity': 1}},
                'dataLabels': {
                    'enabled': 1,
                    'useHTML': 0,
                    'style': {'fontSize': font_size, 'textOutline': 0, 'fontWeight': 0}
                }
            }
        },

        'xAxis': {
            'categories': x_list,
            'title': title('', font_size),
            'labels': {'useHTML': 1, 'align': 'center'},
        },

        'yAxis': {
            # pylint: disable=E0602
            'title': title(_('Age'), font_size),
            'labels': {'style': {'fontSize': font_size}},
        },

        'series': [
            # pylint: disable=E0602
            {'name': _('age low/high'), 'data': age_list, 'connectorWidth': 2},
            {'name': _('avg age'), 'type': 'scatter', 'data': scatter_list, 'marker': {'symbol': 'circle', 'fillColor': line_color}}
        ]
    }

    return chart_options

def league_agechart_get(logger, ctitle, csubtitle, ismobile, league_agedate_dic, ly_league_agedate_dic):
    """ create chart showing players per age for entire league """
    logger.debug('league_agechart_get()')

    variable_dic = variables_get(ismobile)

    x_list = []
    player_list = {'GER': [], 'NAM': [], 'Others': []}
    ly_player_list = {'GER': [], 'NAM': [], 'Others': []}

    if league_agedate_dic:
        min = sorted(league_agedate_dic.keys())[0]
        max = sorted(league_agedate_dic.keys())[-1]
    else:
        min = 16
        max = 42

    for age in range(min, max+1):
        x_list.append(age)
        if age in league_agedate_dic:
            for region in ('GER', 'NAM', 'Others'):
                if region in league_agedate_dic[age]:
                    if region == 'GER':
                        player_list[region].append(league_agedate_dic[age][region] * -1)
                    else:
                         player_list[region].append(league_agedate_dic[age][region])
                else:
                    player_list[region].append(0)
        else:
            player_list['GER'].append(0)
            player_list['NAM'].append(0)
            player_list['Others'].append(0)

        if age in ly_league_agedate_dic:
            for region in ('GER', 'NAM', 'Others'):
                if region in ly_league_agedate_dic[age]:
                    if region == 'GER':
                        ly_player_list[region].append(ly_league_agedate_dic[age][region] * -1)
                    else:
                         ly_player_list[region].append(ly_league_agedate_dic[age][region])
                else:
                    ly_player_list[region].append(0)
        else:
            ly_player_list['GER'].append(0)
            ly_player_list['NAM'].append(0)
            ly_player_list['Others'].append(0)

    chart_options = {

        'chart': {
            'type': 'bar',
            'height': '90%',
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(additional_parameters={'reversed': 1}),
        #'responsive': responsive_y1(),
        #'tooltip': {'enabled': 0},

        'plotOptions': {
            'bar': {'stacking': 'normal'},
            'series': {
                'states': {'inactive': {'opacity': 1}},
                'pointPadding': 0,
                'groupPadding': 0,
                'dataLabels': {
                    'enabled': 0,
                    'useHTML': 0,
                    'style': {'fontSize': font_size, 'textOutline': 0, 'color': '#ffffff', 'fontWeight': 0}
                }
            }
        },

        'xAxis': [{
            'categories': x_list,
            'title': title(_('Age'), font_size),
            'reversed': 0,
            'labels': {'step': 2, 'style': {'fontSize': font_size}},
        }, {
            'categories': x_list,
            'title': title(_('Age'), font_size),
            'reversed': 0,
            'opposite': 1,
            'linkedTo': 0,
            'labels': {'step': 2, 'style': {'fontSize': font_size}},
        }],

        'yAxis': {
            # pylint: disable=E0602
            #v'categories': [-5, -4,-3,-2, -1, 0, 1, 2, 3, 4, 5],
            'title': title(_('Number of Players'), font_size),
            'reversedStacks': 0,
            'labels': {'style': {'fontSize': font_size}},  # 'format': '{value:.2}'},
        },

        'series': [
            {'name': _('last season'), 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': ly_player_list['NAM'], 'color': chart_color7, 'stack': 'LY', 'pointPlacement': 0.25},
            {'name': _('North America'), 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': player_list['NAM'], 'color': chart_color1, 'stack': 'DE', 'zIndex': 1},
            {'name': _('last season'), 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': ly_player_list['Others'], 'color': linetrans_color, 'stack': 'LY', 'pointPlacement': 0.25},
            {'name': _('Others'), 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': player_list['Others'], 'color': line_color, 'stack': 'DE', 'zIndex': 1},
            {'name': _('last season'), 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': ly_player_list['GER'], 'color': chart_color5, 'stack': 'LY', 'pointPlacement': 0.25},
            {'name': _('Germany'), 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': player_list['GER'], 'color': chart_color3, 'stack': 'DE', 'zIndex': 1},
        ],
    }

    return chart_options