# -*- coding: utf-8 -*-
""" list of functions for shots """
import math
# pylint: disable=E0401
from rest.functions.chartparameters import credit, exporting, responsive_gameflow, responsive_y1, responsive_y2, plotoptions_marker_disable, title, legend, tooltip, labels, font_size
from rest.functions.chartparameters import text_color, plotlines_color, chart_color1, chart_color2, chart_color3, chart_color4, chart_color5, chart_color6, chart_color8, chart_color9, shot_missed_color, shot_blocked_color, shot_goal_color, shot_sog_color, line_color

# pylint: disable=R0914
def shotsumchart_create(logger, shot_sum_dic, shot_min_dic, goal_dic, plotline_list, machinfo_dic):
    # pylint: disable=E0602
    """ create shotsum chart """
    logger.debug('shotsumchart_create()')

    minute_list = list(shot_sum_dic['home_team'].keys())
    home_team_bar = list(shot_min_dic['home_team'].values())
    visitor_team_bar = list(shot_min_dic['visitor_team'].values())

    home_team_spline = []
    for min_, value in shot_sum_dic['home_team'].items():
        if min_ in goal_dic['home_team'].keys():
            # home_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(machinfo_dic['home_team_logo'])}})
            home_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'radius': 5, 'symbol': 'circle'}, 'dataLabels': {'enabled': 1, 'color': chart_color3, 'format': '{0}'.format(goal_dic['home_team'][min_])}})

        else:
            home_team_spline.append(value)

    visitor_team_spline = []
    for min_, value in shot_sum_dic['visitor_team'].items():
        if min_ in goal_dic['visitor_team'].keys():
            # visitor_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(machinfo_dic['visitor_team_logo'])}})
            visitor_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'radius': 5, 'symbol': 'circle'}, 'dataLabels': {'enabled': 1, 'color': chart_color4, 'format': '{0}'.format(goal_dic['visitor_team'][min_])}})

        else:
            visitor_team_spline.append(value)

    # max value for left y axis
    y_left_max = max(home_team_bar)
    if y_left_max < max(visitor_team_bar):
        y_left_max = max(visitor_team_bar)

    # max value for right y axis
    y_right_tick_interval = 20
    y_right_max = max(list(shot_sum_dic['home_team'].values()))
    if y_right_max < max(list(shot_sum_dic['visitor_team'].values())):
        y_right_max = max(list(shot_sum_dic['visitor_team'].values()))
    # incorporate tick interval to ensure proper scaling
    y_right_max = math.ceil(y_right_max/y_right_tick_interval) * y_right_tick_interval

    chart_options = {

        'chart': {
            'type': 'column',
            'height': '60%',
            'alignTicks': 0,
        },

        # 'exporting': exporting(),
        'title': title(''),
        'legend': legend(),
        'tooltip': tooltip('<b>{point.x}.%s</b><br>' % _('min')),
        'plotOptions': plotoptions_marker_disable('spline'),
        'credits': credit(),
        'responsive': responsive_y2(),

        'xAxis': {
            'categories': minute_list,
            'title': {
                'text': _('Game Time'),
                'style': {'color': text_color, 'font-size': font_size},
            },
            'labels': {'style': {'fontSize': font_size}},
            'tickInterval': 5,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'plotLines': [
                {'color': plotlines_color, 'width': 2, 'value': 20},
                {'color': plotlines_color, 'width': 2, 'value': 40},
                {'color': plotlines_color, 'width': 2, 'value': 60}
                ],
            'plotBands': plotline_list,
        },

        'yAxis': [
            {
                'title': title(_('Shots per minute'), font_size),
                #'max': y1_max,
                'tickInterval': 1,
                'maxPadding': 0.1,
                'labels': labels(),
            }, {
                'title': title(_('Cumulated shots'), font_size),
                'opposite': 1,
                'max': y_right_max,
                'labels': labels()
            }],

        'series': [{
            'name': '{0} {1}'.format(machinfo_dic['home_team__shortcut'], _('per min')),
            'data': home_team_bar,
            'color': chart_color1,
        }, {
            'name': '{0} pro min'.format(machinfo_dic['visitor_team__shortcut']),
            'data': visitor_team_bar,
            'color': chart_color2,
        }, {
            'type': 'spline',
            'name': '{0} Sum'.format(machinfo_dic['home_team__shortcut']),
            'data': home_team_spline,
            'color': chart_color3,
            'yAxis': 1,
            'zIndex': 3,
        }, {
            'type': 'spline',
            'name': '{0} Sum'.format(machinfo_dic['visitor_team__shortcut']),
            'data': visitor_team_spline,
            'color': chart_color4,
            'yAxis': 1,
            'zIndex': 2,
        }, {
            'name': 'PP {0}'.format(machinfo_dic['home_team__shortcut']),
            'color': chart_color5,
            'marker': {'symbol': 'square'},
        }, {
            'name': 'PP {0}'.format(machinfo_dic['visitor_team__shortcut']),
            'color': chart_color6,
            'marker': {'symbol': 'square'},
        }]
    }

    return chart_options

def gameflowchart_create(logger, shot_flow_dic, goal_dic, plotline_list, matchinfo_dic):
    """ create flow chart """
    # pylint: disable=E0602
    logger.debug('gameflowchart_create()')

    # calculate max and min vals to keep y-axis centered
    y_max = max(list(shot_flow_dic['home_team'].values()))
    if y_max < max(list(shot_flow_dic['visitor_team'].values())):
        y_max = max(list(shot_flow_dic['visitor_team'].values()))
    y_min = y_max * -1

    # x_list
    min_list = list(shot_flow_dic['home_team'].keys())

    # game flow from home team
    home_team_list = []
    for min_, value in shot_flow_dic['home_team'].items():
        # set marker on graph if there was a goal in this min
        if min_ in goal_dic['home_team'].keys():
            home_team_list.append({'y' : value * -1, 'marker' : {'fillColor': chart_color8, 'enabled': 1, 'radius': 5, 'symbol': 'circle'}, 'dataLabels': {'enabled': 1, 'useHTML': 1, 'color': chart_color8, 'format': '{0}'.format(goal_dic['home_team'][min_])}})
        else:
            home_team_list.append(value * -1)

    # game flow from visitor team
    visitor_team_list = []
    for min_, value in shot_flow_dic['visitor_team'].items():
        # set marker on graph if there was a goal in this min
        if min_ in goal_dic['visitor_team'].keys():
            visitor_team_list.append({'y' : value, 'marker' : {'fillColor': chart_color9, 'enabled': 1, 'radius': 5, 'symbol': 'circle'}, 'dataLabels': {'y': 25, 'enabled': 1, 'useHTML': 1, 'color': chart_color9, 'format': '{0}'.format(goal_dic['visitor_team'][min_])}})
        else:
            visitor_team_list.append(value)

    chart_options = {
        'chart': {
            'type': 'areaspline',
            'inverted': 1,
            'height': '100%',
            'alignTicks': 0,
        },

        'exporting': exporting(),
        'credits': credit(_('based on an idea of @DanielT_W'), 'https://twitter.com/danielt_w'),
        'tooltip': tooltip('<b>{point.x}.%s</b><br>' % _('min')),
        'legend': legend(0),
        'plotOptions': plotoptions_marker_disable('areaspline'),
        'responsive': responsive_gameflow(),

        'title': {
            'useHTML': 1,
            'text': '<img src="{0}" width="{1}">'.format(matchinfo_dic['home_team_logo'], 55),
            'floating': 1,
            'align': 'left',
            'x': 100,
            'y': 80,
        },

        'subtitle': {
            'useHTML': 1,
            'text': '<img src="{0}" width="{1}">'.format(matchinfo_dic['visitor_team_logo'], 55),
            'floating': 1,
            'align': 'right',
            'x': -50,
            'y': 80,
        },

        'xAxis': {
            'categories': min_list,
            'title': {
                'text': _('Game Time'),
                'style': {'color': text_color, 'font-size': font_size},
            },
            'labels': {'style': {'fontSize': font_size},},
            'tickInterval': 5,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'breaks': [{'from': 0, 'to': 1, 'breakSize': 0}, {'from': 20, 'to': 21, 'breakSize': 0}, {'from': 40, 'to': 41, 'breakSize': 0}, {'from': 60, 'to': 61, 'breakSize': 0}],
            'plotLines': [{
                'color': plotlines_color,
                'width': 2,
                'value': 20,
            }, {
                'color': plotlines_color,
                'width': 2,
                'value': 40,
            }, {
                'color': plotlines_color,
                'width': 2,
                'value': 60,
            }],
            'plotBands': plotline_list,
        },
        'yAxis': [
            {
                'title': {
                    'text': _('Shot attempts per 60min (SH60)'),
                    'style': {'color': text_color, 'font-size': font_size},
                },
                'tickInterval': 100,
                'maxPadding': 0.1,
                'labels': {'style': {'fontSize': font_size},},
                'min': y_min,
                'max': y_max,
            }],
        'series': [{
            'name': matchinfo_dic['home_team__shortcut'],
            'data': home_team_list,
            'color': chart_color1,
        }, {
            'name': matchinfo_dic['visitor_team__shortcut'],
            'data': visitor_team_list,
            'color': chart_color2,
        }]
    }

    return chart_options

def shotstatussumchart_create(logger, shotsum_dic, _shotstatus_dic, goal_dic, team, matchinfo_dic):
    """ create shotstatus chart """
    # pylint: disable=E0602
    logger.debug('shotstatussumchart_create()')

    # build lists
    min_list = list(shotsum_dic[team][1].keys())
    shot_list = list(shotsum_dic[team][1].values())
    missed_list = list(shotsum_dic[team][2].values())
    block_list = list(shotsum_dic[team][3].values())
    goal_list = []
    for min_, value in shotsum_dic[team][4].items():
        # set marker on graph if there was a goal in this min
        if min_ in goal_dic['home_team'].keys():
            # goal_list.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['home_team_logo']),}})
            goal_list.append({'y' : value, 'marker' : {'enabled': 1, 'radius': 5, 'symbol': 'circle', 'fillColor': chart_color3, 'lineWidth': 2, 'lineColor': shot_missed_color}, 'dataLabels': {'enabled': 1, 'color': chart_color3, 'format': '{0}'.format(goal_dic['home_team'][min_])}})

        elif min_ in goal_dic['visitor_team'].keys():
            # goal_list.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['visitor_team_logo']),}})
            goal_list.append({'y' : value, 'marker' : {'enabled': 1, 'radius': 5, 'symbol': 'circle', 'fillColor': chart_color4, 'lineWidth': 2, 'lineColor': shot_missed_color}, 'dataLabels': {'enabled': 1, 'color': chart_color4, 'format': '{0}'.format(goal_dic['visitor_team'][min_])}})

        else:
            goal_list.append(value)

    chart_options = {

        'chart': {
            'type': 'area',
            'height': '60%'
        },

        'exporting': exporting(),
        'title': title(''),
        'credits': credit(),
        'tooltip': tooltip('<b>{point.x}.%s</b><br>' % _('min')),
        'legend': legend(),
        'responsive': responsive_y1(),

        'plotOptions': {
            'area': {
                'marker': {
                    'enabled': 0,
                },
                # 'stacking': 'percent',
                'stacking': 'normal',
            },
        },

        'xAxis': {
            'categories': min_list,
            'title': title(_('Game Time'), font_size),
            'labels': {'style': {'fontSize': font_size},},
            'tickInterval': 5,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'plotLines': [{
                'color': plotlines_color,
                'width': 2,
                'value': 20,
            }, {
                'color': plotlines_color,
                'width': 2,
                'value': 40,
            }, {
                'color': plotlines_color,
                'width': 2,
                'value': 60,
            }],
        },

        'yAxis': [
            {
                'title': title(_('Cumulated shots'), font_size),
                'labels': {'style': {'fontSize': font_size}},
            }],

        'series': [{
            'name': _('missed'),
            'data': missed_list,
            'color': shot_missed_color,
        }, {
            'name': _('blocked'),
            'data': block_list,
            'color': shot_blocked_color,
        }, {
            'name': _('Goals'),
            'data': goal_list,
            'color': shot_goal_color,
            'zIndex': 2,
        }, {
            'name': _('Shots on Goal'),
            'data': shot_list,
            'color': shot_sog_color,
        },]
    }
    return chart_options

def shotmapchart_create(logger, shotmap_list):
    """ create shotmap """
    # pylint: disable=E0602
    logger.debug('shotmapchart_create()')

    data_dic = {1 :[], 2: [], 3: [], 4: []}

    for shot in sorted(shotmap_list, key=lambda x: (x['match_shot_resutl_id'])):
        tmp_dic = {
            'x': shot['x'],
            'y': shot['y'],
            'z': 2,
            'jersey': shot['player__jersey'],
            'name': shot['name'],
            'labelrank': 2,
            'minute': shot['minute'],
            }

        if shot['match_shot_resutl_id'] == 2:
            tmp_dic['labelrank'] = 1
        elif shot['match_shot_resutl_id'] == 3:
            tmp_dic['dataLabels'] = {'color': '#ffffff'}
            tmp_dic['labelrank'] = 3
        elif shot['match_shot_resutl_id'] == 4:
            tmp_dic['labelrank'] = 4

        data_dic[shot['match_shot_resutl_id']].append(tmp_dic)

    bg_image = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTkwIiBoZWlnaHQ9IjU5NSIgdmlld0JveD0iMCAwIDU5MCA1OTUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiPjx0aXRsZT5Hcm91cCBDb3B5PC90aXRsZT48ZGVmcz48cGF0aCBkPSJNNzkgMzMwYzIwLjU0IDAgMzctMTYuNTY1IDM3LTM3cy0xNi41NjUtMzctMzctMzd2NzR6IiBpZD0iYSIvPjxtYXNrIGlkPSJiIiB4PSIwIiB5PSIwIiB3aWR0aD0iMzciIGhlaWdodD0iNzQiIGZpbGw9IiNmZmYiPjx1c2UgeGxpbms6aHJlZj0iI2EiLz48L21hc2s+PC9kZWZzPjxnIHRyYW5zZm9ybT0icm90YXRlKDkwIDI5Mi41IDI5NSkiIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+PHBhdGggZD0iTTE0OCAwaDQ0MXY1ODRIMTQ4UzIxLjUwNCA1ODQgLjcwMyA0NDAuNDczVjE0NS4yMDdTMTIuOTIyIDkuOTYxIDE0OCAweiIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9IjYiIGZpbGw9IiNGRkYiLz48cGF0aCBkPSJNNTg3IDM4MVYyMDVjLTQ4LjYwMSAwLTg4IDM5LjM5OS04OCA4OHMzOS4zOTkgODggODggODh6IiBzdHJva2U9IiMyNTc1RDIiIHN0cm9rZS13aWR0aD0iMyIvPjxwYXRoIGQ9Ik00MTkgMS41djU4MiIgc3Ryb2tlPSIjMjU3NUQyIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiLz48cGF0aCBkPSJNNzkuNSAyMS41djU0MyIgc3Ryb2tlPSIjRUUyQTQyIiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiLz48dXNlIHN0cm9rZT0iI0VFMkE0MiIgbWFzaz0idXJsKCNiKSIgc3Ryb2tlLXdpZHRoPSI2IiBmaWxsLW9wYWNpdHk9Ii4zIiBmaWxsPSIjMjU3NUQyIiB4bGluazpocmVmPSIjYSIvPjxwYXRoIGQ9Ik0xNzkuNSA2MC41djIwNy4wMDJNMjE5LjUgNjAuNXYyMDcuMDAyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBzdHJva2Utd2lkdGg9IjMiIGZpbGw9IiNGRkYiIGN4PSIxOTkiIGN5PSIxNjQiIHI9Ijg5Ii8+PHBhdGggZD0iTTE0Ny41IDE1Ni41aDM5TTE0Ny41IDE3MS41aDM5TTIxMi41IDE1Ni41aDM5TTIxMi41IDE3MS41aDM5TTE4Ni41IDEzNC41djIyTTIxMi41IDEzNC41djIyTTE4Ni41IDE3MS41djIyTTIxMi41IDE3MS41djIyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBmaWxsPSIjRUUyQTQyIiBjeD0iMTk5IiBjeT0iMTY0IiByPSI2Ii8+PGNpcmNsZSBzdHJva2U9IiNFRTJBNDIiIGZpbGw9IiNFRTJBNDIiIGN4PSI0NDMiIGN5PSIxNjQiIHI9IjYiLz48cGF0aCBkPSJNMTc5LjUgMzIyLjV2MjA3LjAwMk0yMTkuNSAzMjIuNXYyMDcuMDAyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBzdHJva2Utd2lkdGg9IjMiIGZpbGw9IiNGRkYiIGN4PSIxOTkiIGN5PSI0MjYiIHI9Ijg5Ii8+PHBhdGggZD0iTTE0Ny41IDQxOC41aDM5TTE0Ny41IDQzMy41aDM5TTIxMi41IDQxOC41aDM5TTIxMi41IDQzMy41aDM5TTE4Ni41IDM5Ni41djIyTTIxMi41IDM5Ni41djIyTTE4Ni41IDQzMy41djIyTTIxMi41IDQzMy41djIyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBmaWxsPSIjRUUyQTQyIiBjeD0iMTk5IiBjeT0iNDI2IiByPSI2Ii8+PGNpcmNsZSBzdHJva2U9IiNFRTJBNDIiIGZpbGw9IiNFRTJBNDIiIGN4PSI0NDMiIGN5PSI0MjYiIHI9IjYiLz48cGF0aCBkPSJNMTQ4IDBoNDQxdjU4NEgxNDhTMjEuNTA0IDU4NCAuNzAzIDQ0MC40NzNWMTQ1LjIwN1MxMi45MjIgOS45NjEgMTQ4IDB6IiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iNiIvPjwvZz48L3N2Zz4="

    chart_options = {

        'chart': {
            'type': 'scatter',
            'plotBorderWidth': 0,
            'plotBackgroundImage': bg_image,
            'zoomType': 'xy',
            'height': '110%'
        },

        'exporting': exporting(),
        'title': title(''),
        'credits': credit(),
        'legend': legend(),

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '<table class="w3-tiny">',
            'pointFormat': '<tr><td><b>{point.name} ({point.jersey})<b></td></tr>' +
                           '<tr><td>{point.minute}. %s</td></tr>' % _('min'),
            'footerFormat': '</table>',
            'followPointer': 1,
        },

        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': 1,
                    'color': '#000000',
                    'style': {'textShadow': 0, 'textOutline': 0, 'fontSize': font_size},
                    'y': 13,
                    'format': '{point.jersey}',
                    'align': 'center',
                    'allowOverlap': 1,
                },
                'color': shot_sog_color,
                'lineColor': line_color,
            },
        },

        'xAxis': {
            'visible': 0,
            'labels': {'enabled': 0},
            'min': -100,
            'max': 100,
            'tickInterval': 0,
        },

        'yAxis': {
            'visible': 0,
            'gridLineWidth': 0,
            'title': {
                'text': '',
            },
            'labels': {'enabled': 0},
            'min': 0,
            'max': 105,
            'tickInterval': 0,
        },

        'series': [
            {'name': _('Shots on Goal'), 'color': shot_sog_color, 'data': data_dic[1], 'marker': {'radius': 15, 'symbol': 'circle'}},
            {'name': _('missed'), 'data': data_dic[2], 'color': shot_missed_color, 'marker': {'symbol': 'circle', 'radius': 15}},
            {'name': _('blocked'), 'color': shot_blocked_color, 'data': data_dic[3], 'marker': {'symbol': 'circle', 'radius': 15}},
            {'name': _('Goals'), 'color': shot_goal_color, 'data': data_dic[4], 'marker': {'symbol': 'circle', 'radius': 15}},
            ],

       'responsive': {
            'rules': [{
                'condition': {'maxWidth': 500},
                'chartOptions': {
                'series': [
                    {'name': _('Shots on Goal'), 'color': shot_sog_color, 'data': data_dic[1], 'marker': {'radius': 12, 'symbol': 'circle'}},
                    {'name': _('missed'), 'data': data_dic[2], 'color': shot_missed_color, 'marker': {'symbol': 'circle', 'radius': 12}},
                    {'name': _('blocked'), 'color': shot_blocked_color, 'data': data_dic[3], 'marker': {'symbol': 'circle', 'radius': 12}},
                    {'name': _('Goals'), 'color': shot_goal_color, 'data': data_dic[4], 'marker': {'symbol': 'circle', 'radius': 12}},
                    ],
                'plotOptions':{'series': {'dataLabels': {'y': 15}}}
                }
            }]
         }
    }

    return chart_options
