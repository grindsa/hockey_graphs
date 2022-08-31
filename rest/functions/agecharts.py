# -*- coding: utf-8 -*-
""" functions to feed age-charts """
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_y1, title, subtitle, legend, font_size, plotlines_color, corner_annotations, variables_get
from rest.functions.chartparameters import chart_color1, chart_color2, chart_color3, chart_color6, line_color


def age_overviewchart_get(logger, ctitle, csubtitle, ismobile, agedate_dic):
    """ create chart showing age per teams """
    logger.debug('age_overviewchart_get()')

    variable_dic = variables_get(ismobile)


    x_list = []
    age_list = []
    for team in sorted(agedate_dic, key=lambda x: x['shortcut']):
        x_list.append(team['shortcut'])
        age_list.append(team['y'])

    chart_options = {
        'chart': {
            'type': 'boxplot',
            #'height': '80%',
            #'alignTicks': 0,
            #'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        #'responsive': responsive_y1(),
        #'tooltip': {'enabled': 0},

        #'plotOptions': {
        #    'series': {
        #        'states': {'inactive': {'opacity': 1}},
        #        'dataLabels': {
        #            'enabled': 0,
        #            'useHTML': 0,
        #            'style': {'fontSize': font_size, 'textOutline': 0, 'color': '#ffffff', 'fontWeight': 0}
        #        }
        #    }
        #},

        'xAxis': {
            'categories': x_list,
            'title': title('', font_size),
            'labels': {'useHTML': 1, 'align': 'center'},
            # 'labels': {'style': {'fontSize': font_size}},
        },

        'yAxis': {
            # pylint: disable=E0602
            'title': title(_('PDO'), font_size),
            #'labels': {'style': {'fontSize': font_size}},
            #'min': 80,
            #'max': 130,
            #'height': '50%',
            #'plotLines': [{'color': plotlines_color, 'width': 2, 'value': 100}],
        },

        'series': [
            # pylint: disable=E0602
            {'name': 'home pdo ', 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': age_list},
        ]
    }

    return chart_options

def league_agechart_get(logger, ctitle, csubtitle, ismobile, league_agedate_dic):
    """ create chart showing players per age for entire league """
    logger.debug('league_agechart_get()')

    variable_dic = variables_get(ismobile)

    x_list = []
    player_list = {'GER': [], 'NAM': [], 'Others': []}


    # from pprint import pprint
    # pprint(league_agedate_dic)

    min = sorted(league_agedate_dic.keys())[0]
    max = sorted(league_agedate_dic.keys())[-1]

    for age in range(min, max+1):
        x_list.append(age)
        if age in league_agedate_dic:
            for region in ('GER', 'NAM', 'Others'):
                if region in league_agedate_dic[age]:
                    player_list[region].append(league_agedate_dic[age][region])
                else:
                    player_list[region].append(0)
        else:
            player_list['GER'].append(0)
            player_list['NAM'].append(0)
            player_list['Others'].append(0)

    #from pprint import pprint
    #pprint(league_agedate_dic)
    chart_options = {

        'chart': {
            'type': 'column',
            'height': '60%',
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        #'responsive': responsive_y1(),
        #'tooltip': {'enabled': 0},

        'plotOptions': {
            'column': {'stacking': 1},
            'series': {
                'states': {'inactive': {'opacity': 1}},
                'dataLabels': {
                    'enabled': 0,
                    'useHTML': 0,
                    'style': {'fontSize': font_size, 'textOutline': 0, 'color': '#ffffff', 'fontWeight': 0}
                }
            }
        },

        'xAxis': {
            'categories': x_list,
            'title': title(_('Age'), font_size),
            'labels': {'useHTML': 1, 'align': 'center'},
            # 'labels': {'style': {'fontSize': font_size}},
        },

        'yAxis': {
            # pylint: disable=E0602
            'title': title(_('Number of Players'), font_size),
            'reversedStacks': 0
            #'labels': {'style': {'fontSize': font_size}},
            #'min': 80,
            #'max': 130,
            #'height': '50%',
            #'plotLines': [{'color': plotlines_color, 'width': 2, 'value': 100}],
        },

        'series': [
            {'name': _('Germany'), 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': player_list['GER'], 'color': chart_color3},
            {'name': _('North America'), 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': player_list['NAM'], 'color': chart_color1},
            {'name': _('Others'), 'marker': {'enabled': 0, 'symbol': 'square'}, 'data': player_list['Others'], 'color': line_color}
        ],
    }

    return chart_options