# -*- coding: utf-8 -*-
""" list of functions for shots """
import math
# pylint: disable=E0401, C0302
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_gameflow, responsive_y1, responsive_y1_label, responsive_y2, responsive_bubble, plotoptions_marker_disable, title, subtitle, legend, tooltip, labels, font_size, font_size_mobile, legend_valign_mobile, corner_annotations, variables_get, gameflow_annotations, shotzonelabel, puckpossession_annotations
from rest.functions.chartparameters import text_color, plotlines_color, chart_color1, chart_color2, chart_color3, chart_color4, chart_color6, chart_color8, shot_posthit_color, shot_missed_color, shot_blocked_color, shot_goal_color, shot_sog_color, line_color, line1_color, line2_color, line3_color, line4_color, line5_color

# pylint: disable=R0914
def shotsumchart_create(logger, ctitle, csubtitle, ismobile, shot_sum_dic, shot_min_dic, goal_dic, plotline_list, machinfo_dic, color_dic):
    # pylint: disable=E0602
    """ create shotsum chart """
    logger.debug('shotsumchart_create()')

    variable_dic = variables_get(ismobile)

    minute_list = list(shot_sum_dic['home_team'].keys())
    home_team_bar = list(shot_min_dic['home_team'].values())
    visitor_team_bar = list(shot_min_dic['visitor_team'].values())

    home_team_spline = []
    for min_, value in shot_sum_dic['home_team'].items():
        if min_ in goal_dic['home_team'].keys():
            home_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(machinfo_dic['home_team_logo'])}, 'dataLabels': {'enabled': 1, 'color': chart_color3, 'format': '{0}'.format(goal_dic['home_team'][min_])}})
            # home_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'radius': 5, 'symbol': 'circle'}, 'dataLabels': {'enabled': 1, 'color': chart_color3, 'format': '{0}'.format(goal_dic['home_team'][min_])}})

        else:
            home_team_spline.append(value)

    visitor_team_spline = []
    for min_, value in shot_sum_dic['visitor_team'].items():
        if min_ in goal_dic['visitor_team'].keys():
            visitor_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(machinfo_dic['visitor_team_logo'])}, 'dataLabels': {'enabled': 1, 'color': chart_color4, 'format': '{0}'.format(goal_dic['visitor_team'][min_])}})
            # visitor_team_spline.append({'y' : value, 'marker' : {'enabled': 1, 'radius': 5, 'symbol': 'circle'}, 'dataLabels': {'enabled': 1, 'color': chart_color4, 'format': '{0}'.format(goal_dic['visitor_team'][min_])}})

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
            'height': '80%',
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
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
            'color': color_dic['home_team_color'],
        }, {
            'name': '{0} pro min'.format(machinfo_dic['visitor_team__shortcut']),
            'data': visitor_team_bar,
            'color': color_dic['visitor_team_color_secondary'],
        }, {
            'type': 'spline',
            'name': '{0} Sum'.format(machinfo_dic['home_team__shortcut']),
            'data': home_team_spline,
            'color': color_dic['home_team_color'],
            'yAxis': 1,
            'zIndex': 3,
        }, {
            'type': 'spline',
            'name': '{0} Sum'.format(machinfo_dic['visitor_team__shortcut']),
            'data': visitor_team_spline,
            'color': color_dic['visitor_team_color_secondary'],
            'yAxis': 1,
            'zIndex': 2,
        }, {
            'name': 'PP {0}'.format(machinfo_dic['home_team__shortcut']),
            'color': color_dic['home_team_color_penalty'],
            'marker': {'symbol': 'square'},
        }, {
            'name': 'PP {0}'.format(machinfo_dic['visitor_team__shortcut']),
            'color': color_dic['visitor_team_color_penalty'],
            'marker': {'symbol': 'square'},
        }]
    }

    return chart_options

def gameflowchart_create(logger, ctitle, csubtitle, ismobile, gameflow_dic, goal_dic, plotline_list, matchinfo_dic, color_dic):
    """ create flow chart """
    # pylint: disable=E0602
    logger.debug('gameflowchart_create()')

    variable_dic = variables_get(ismobile)

    # x_list
    min_list = []
    for i in range(61):
        min_list.append(i)

    # game flow from home team
    data_dic = {}

    y_max = 0
    for team in gameflow_dic:
        data_dic[team] = {}
        for period in gameflow_dic[team]:
            data_dic[team][period] = []
            for min_, value in  gameflow_dic[team][period].items():
                # adjust y_max value
                if y_max <= value:
                    y_max = value
                # negate value in case of home-time (needed to show spline on the left side)
                if team == 'home_team':
                    value = value * -1
                # game flow from home team
                if min_ in goal_dic[team].keys():
                    # set marker on graph if there was a goal in this min
                    data_dic[team][period].append({'x': min_, 'y': value, 'marker': {'fillColor': chart_color8, 'enabled': 1, 'radius': 5, 'symbol': 'circle'}, 'dataLabels': {'borderWidth': 1, 'backgroundColor': '#ffffff', 'borderColor': chart_color8, 'enabled': 1, 'useHTML': 1, 'color': chart_color8, 'format': '{0}'.format(goal_dic[team][min_])}})
                    goal_dic[team].pop(min_)
                else:
                    data_dic[team][period].append({'x': min_, 'y': value})

    # calulate y_min
    y_min = y_max * -1

    chart_options = {
        'chart': {
            'type': 'areaspline',
            'inverted': 1,
            'height': '110%',
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'credits': credit(_('based on an idea of @DanielT_W'), 'https://twitter.com/danielt_w'),
        'tooltip': tooltip('<b>{point.x}.%s</b><br>' % _('min')),
        'legend': legend(0),
        'plotOptions': plotoptions_marker_disable('areaspline'),
        'responsive': responsive_gameflow(),

        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),

        'annotations': gameflow_annotations(ismobile, y_max, matchinfo_dic['home_team_logo'], matchinfo_dic['visitor_team_logo']),

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
                # 'color': plotlines_color,
                'color': '#ffffff',
                'width': 3,
                'value': 20,
                'zIndex': 5
            }, {
                # 'color': plotlines_color,
                'color': '#ffffff',
                'width': 3,
                'value': 40,
                'zIndex': 5
            }, {
                # 'color': plotlines_color,
                'color': '#ffffff',
                'width': 4,
                'value': 60,
                'zIndex': 5
            }],
            'plotBands': plotline_list,
        },
        'yAxis': [
            {
                'title': {'text': _('Shot attempts per 60min (SH60)'), 'style': {'color': text_color, 'font-size': font_size}},
                'tickInterval': 100,
                'maxPadding': 0.1,
                'labels': {'style': {'fontSize': font_size}},
                'min': y_min,
                'max': y_max,
                'plotLines': [{'color': '#ffffff', 'width': 3, 'value': 0, 'zIndex': 5}],
            }],
        'series': []
    }

    for ele in [1, 2, 3, 4]:
        if ele in data_dic['home_team']:
            chart_options['series'].append({'name': matchinfo_dic['home_team__shortcut'], 'data': data_dic['home_team'][ele], 'color': color_dic['home_team_color_primary'], 'states': {'inactive': {'opacity': 1}}})
        if ele in data_dic['visitor_team']:
            chart_options['series'].append({'name': matchinfo_dic['visitor_team__shortcut'], 'data': data_dic['visitor_team'][ele], 'color': color_dic['visitor_team_color_secondary'], 'states': {'inactive': {'opacity': 1}}})

    return chart_options

def shotstatussumchart_create(logger, ctitle, csubtitle, ismobile, shotsum_dic, _shotstatus_dic, goal_dic, team, matchinfo_dic):
    """ create shotstatus chart """
    # pylint: disable=E0602
    logger.debug('shotstatussumchart_create()')

    variable_dic = variables_get(ismobile)

    # build lists
    min_list = list(shotsum_dic[team][1].keys())
    shot_list = list(shotsum_dic[team][1].values())
    missed_list = list(shotsum_dic[team][2].values())
    block_list = list(shotsum_dic[team][3].values())
    posthit_list = list(shotsum_dic[team][5].values())

    goal_list = []

    for min_, value in shotsum_dic[team][4].items():
        # set marker on graph if there was a goal in this min
        if min_ in goal_dic['home_team'].keys():
            goal_list.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['home_team_logo'])}, 'dataLabels': {'y': -15, 'style': {'fontSize': variable_dic['label_size']}, 'borderWidth': 1, 'backgroundColor': '#ffffff', 'borderColor': chart_color8, 'enabled': 1, 'useHTML': 1, 'color': chart_color8, 'format': '{0}'.format(goal_dic['home_team'][min_])}})
        elif min_ in goal_dic['visitor_team'].keys():
            goal_list.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['visitor_team_logo'])}, 'dataLabels': {'y': -15, 'style': {'fontSize': variable_dic['label_size']}, 'borderWidth': 1, 'backgroundColor': '#ffffff', 'borderColor': chart_color8, 'enabled': 1, 'useHTML': 1, 'color': chart_color8, 'format': '{0}'.format(goal_dic['visitor_team'][min_])}})
        else:
            goal_list.append(value)

    chart_options = {

        'chart': {
            'type': 'areaspline',
            'height': '80%',
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'tooltip': tooltip('<b>{point.x}.%s</b><br>' % _('min')),
        'legend': legend(),
        'responsive': responsive_y1(),

        'plotOptions': {
            'areaspline': {
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
            'name': _('Post hit'),
            'data': posthit_list,
            'color': shot_posthit_color,
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

def shotmapchart_create(logger, ctitle, csubtitle, ismobile, shotmap_list):
    """ create shotmap """
    # pylint: disable=E0602
    logger.debug('shotmapchart_create()')

    variable_dic = variables_get(ismobile)

    data_dic = {1 :[], 2: [], 3: [], 4: [], 5: []}

    cnt = 0
    for shot in sorted(shotmap_list, key=lambda x: (x['match_shot_resutl_id'])):
        cnt += 1
        tmp_dic = {
            'x': shot['x'],
            'y': shot['y'],
            'z': 2,
            'jersey': shot['player__jersey'],
            'name': shot['name'],
            'labelrank': 2000 + cnt,
            'minute': shot['minute'],
            }

        if shot['match_shot_resutl_id'] == 2:
            tmp_dic['labelrank'] = 1000 + cnt
            # tmp_dic['zIndex'] = 1
        elif shot['match_shot_resutl_id'] == 3:
            tmp_dic['dataLabels'] = {'color': '#ffffff'}
            tmp_dic['labelrank'] = 3000 + cnt
        elif shot['match_shot_resutl_id'] == 5:
            tmp_dic['dataLabels'] = {'color': '#ffffff'}
            tmp_dic['labelrank'] = 4000 + cnt
        elif shot['match_shot_resutl_id'] == 4:
            tmp_dic['labelrank'] = 5000 + cnt

        if shot['match_shot_resutl_id'] in data_dic:
            data_dic[shot['match_shot_resutl_id']].append(tmp_dic)

    bg_image = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTkwIiBoZWlnaHQ9IjU5NSIgdmlld0JveD0iMCAwIDU5MCA1OTUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiPjx0aXRsZT5Hcm91cCBDb3B5PC90aXRsZT48ZGVmcz48cGF0aCBkPSJNNzkgMzMwYzIwLjU0IDAgMzctMTYuNTY1IDM3LTM3cy0xNi41NjUtMzctMzctMzd2NzR6IiBpZD0iYSIvPjxtYXNrIGlkPSJiIiB4PSIwIiB5PSIwIiB3aWR0aD0iMzciIGhlaWdodD0iNzQiIGZpbGw9IiNmZmYiPjx1c2UgeGxpbms6aHJlZj0iI2EiLz48L21hc2s+PC9kZWZzPjxnIHRyYW5zZm9ybT0icm90YXRlKDkwIDI5Mi41IDI5NSkiIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+PHBhdGggZD0iTTE0OCAwaDQ0MXY1ODRIMTQ4UzIxLjUwNCA1ODQgLjcwMyA0NDAuNDczVjE0NS4yMDdTMTIuOTIyIDkuOTYxIDE0OCAweiIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9IjYiIGZpbGw9IiNGRkYiLz48cGF0aCBkPSJNNTg3IDM4MVYyMDVjLTQ4LjYwMSAwLTg4IDM5LjM5OS04OCA4OHMzOS4zOTkgODggODggODh6IiBzdHJva2U9IiMyNTc1RDIiIHN0cm9rZS13aWR0aD0iMyIvPjxwYXRoIGQ9Ik00MTkgMS41djU4MiIgc3Ryb2tlPSIjMjU3NUQyIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiLz48cGF0aCBkPSJNNzkuNSAyMS41djU0MyIgc3Ryb2tlPSIjRUUyQTQyIiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiLz48dXNlIHN0cm9rZT0iI0VFMkE0MiIgbWFzaz0idXJsKCNiKSIgc3Ryb2tlLXdpZHRoPSI2IiBmaWxsLW9wYWNpdHk9Ii4zIiBmaWxsPSIjMjU3NUQyIiB4bGluazpocmVmPSIjYSIvPjxwYXRoIGQ9Ik0xNzkuNSA2MC41djIwNy4wMDJNMjE5LjUgNjAuNXYyMDcuMDAyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBzdHJva2Utd2lkdGg9IjMiIGZpbGw9IiNGRkYiIGN4PSIxOTkiIGN5PSIxNjQiIHI9Ijg5Ii8+PHBhdGggZD0iTTE0Ny41IDE1Ni41aDM5TTE0Ny41IDE3MS41aDM5TTIxMi41IDE1Ni41aDM5TTIxMi41IDE3MS41aDM5TTE4Ni41IDEzNC41djIyTTIxMi41IDEzNC41djIyTTE4Ni41IDE3MS41djIyTTIxMi41IDE3MS41djIyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBmaWxsPSIjRUUyQTQyIiBjeD0iMTk5IiBjeT0iMTY0IiByPSI2Ii8+PGNpcmNsZSBzdHJva2U9IiNFRTJBNDIiIGZpbGw9IiNFRTJBNDIiIGN4PSI0NDMiIGN5PSIxNjQiIHI9IjYiLz48cGF0aCBkPSJNMTc5LjUgMzIyLjV2MjA3LjAwMk0yMTkuNSAzMjIuNXYyMDcuMDAyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBzdHJva2Utd2lkdGg9IjMiIGZpbGw9IiNGRkYiIGN4PSIxOTkiIGN5PSI0MjYiIHI9Ijg5Ii8+PHBhdGggZD0iTTE0Ny41IDQxOC41aDM5TTE0Ny41IDQzMy41aDM5TTIxMi41IDQxOC41aDM5TTIxMi41IDQzMy41aDM5TTE4Ni41IDM5Ni41djIyTTIxMi41IDM5Ni41djIyTTE4Ni41IDQzMy41djIyTTIxMi41IDQzMy41djIyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBmaWxsPSIjRUUyQTQyIiBjeD0iMTk5IiBjeT0iNDI2IiByPSI2Ii8+PGNpcmNsZSBzdHJva2U9IiNFRTJBNDIiIGZpbGw9IiNFRTJBNDIiIGN4PSI0NDMiIGN5PSI0MjYiIHI9IjYiLz48cGF0aCBkPSJNMTQ4IDBoNDQxdjU4NEgxNDhTMjEuNTA0IDU4NCAuNzAzIDQ0MC40NzNWMTQ1LjIwN1MxMi45MjIgOS45NjEgMTQ4IDB6IiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iNiIvPjwvZz48L3N2Zz4="

    chart_options = {

        'chart': {
            'type': 'scatter',
            'plotBorderWidth': 0,
            'plotBackgroundImage': bg_image,
            'zoomType': 'xy',
            'height': variable_dic['shotmap_height_pctg'],
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
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
                    'y': 11,
                    'format': '{point.jersey}',
                    'align': 'center',
                    'allowOverlap': 0,
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
            {'name': _('missed'), 'zIndex': 1, 'data': data_dic[2], 'color': shot_missed_color, 'marker': {'lineColor': chart_color2, 'lineWidth': 1, 'symbol': 'circle', 'radius': 15}},
            {'name': _('Shots on Goal'), 'color': shot_sog_color, 'zIndex': 2, 'data': data_dic[1], 'marker': {'lineColor': '#2083df', 'lineWidth': 1, 'radius': 15, 'symbol': 'circle'}},
            {'name': _('blocked'), 'zIndex': 3, 'color': shot_blocked_color, 'data': data_dic[3], 'marker': {'symbol': 'circle', 'radius': 15}},
            {'name': _('Post hit'), 'zIndex': 4, 'color': chart_color4, 'data': data_dic[5], 'marker': {'symbol': 'circle', 'radius': 15}},
            {'name': _('Goals'), 'zIndex': 5, 'color': shot_goal_color, 'data': data_dic[4], 'marker': {'symbol': 'circle', 'radius': 15}},
            ],

        'responsive': {
            'rules': [{
                'condition': {'maxWidth': 500},
                'chartOptions': {
                    'series': [
                        {'name': _('missed'), 'zIndex': 1, 'data': data_dic[2], 'color': shot_missed_color, 'marker': {'lineColor': chart_color2, 'lineWidth': 1, 'symbol': 'circle', 'radius': 12}},
                        {'name': _('Shots on Goal'), 'zIndex': 2, 'color': shot_sog_color, 'data': data_dic[1], 'marker': {'lineColor': '#2083df', 'lineWidth': 1, 'radius': 12, 'symbol': 'circle'}},
                        {'name': _('blocked'), 'zIndex': 3, 'color': shot_blocked_color, 'data': data_dic[3], 'marker': {'symbol': 'circle', 'radius': 12}},
                        {'name': _('Post hit'), 'zIndex': 4, 'color': chart_color4, 'data': data_dic[5], 'marker': {'symbol': 'circle', 'radius': 12}},
                        {'name': _('Goals'), 'zIndex': 5, 'color': shot_goal_color, 'data': data_dic[4], 'marker': {'symbol': 'circle', 'radius': 12}},
                    ],
                    'plotOptions':{'series': {'dataLabels': {'y': 10}}}
                    }
            }]
        }
    }

    return chart_options

def shotzonedata_build(logger, ismobile, shotzoneaggr_dic):
    """ create shotzone data """
    # pylint: disable=E0602
    logger.debug('shotzonedata_build()')

    if ismobile:
        image_width = 25
        label_size = '14px'
    else:
        image_width = 50
        label_size = '28px'

    image_height = image_width

    data_list = [
        # left
        {'x': 2, 'y': 12, 'z': 2, 'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(shotzoneaggr_dic['home_team']['logo'])}},
        {'x': 4, 'y': 11.5, 'z': 2, 'marker': {'enabled': 0}, 'dataLabels': shotzonelabel(shotzoneaggr_dic['home_team']['left']['roundpercent'], label_size)},
        {'x': 2, 'y': 10, 'z': 2, 'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(shotzoneaggr_dic['visitor_team']['logo'])}},
        {'x': 4, 'y': 9.5, 'z': 2, 'marker': {'enabled': 0}, 'dataLabels': shotzonelabel(shotzoneaggr_dic['visitor_team']['left']['roundpercent'], label_size)},

        # slot
        {'x': 9, 'y': 12, 'z': 2, 'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(shotzoneaggr_dic['home_team']['logo'])}},
        {'x': 11, 'y': 11.5, 'z': 2, 'marker': {'enabled': 0}, 'dataLabels': shotzonelabel(shotzoneaggr_dic['home_team']['slot']['roundpercent'], label_size)},
        {'x': 9, 'y': 10, 'z': 2, 'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(shotzoneaggr_dic['visitor_team']['logo'])}},
        {'x': 11, 'y': 9.5, 'z': 2, 'marker': {'enabled': 0}, 'dataLabels': shotzonelabel(shotzoneaggr_dic['visitor_team']['slot']['roundpercent'], label_size)},

        # right
        {'x': 16, 'y': 12, 'z': 2, 'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(shotzoneaggr_dic['home_team']['logo'])}},
        {'x': 18, 'y': 11.5, 'z': 2, 'marker': {'enabled': 0}, 'dataLabels': shotzonelabel(shotzoneaggr_dic['home_team']['right']['roundpercent'], label_size)},
        {'x': 16, 'y': 10, 'z': 2, 'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(shotzoneaggr_dic['visitor_team']['logo'])}},
        {'x': 18, 'y': 9.5, 'z': 2, 'marker': {'enabled': 0}, 'dataLabels': shotzonelabel(shotzoneaggr_dic['visitor_team']['right']['roundpercent'], label_size)},

        # blue
        {'x': 9, 'y': 4, 'z': 2, 'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(shotzoneaggr_dic['home_team']['logo'])}},
        {'x': 11, 'y': 3.5, 'z': 2, 'marker': {'enabled': 0}, 'dataLabels': shotzonelabel(shotzoneaggr_dic['home_team']['blue_line']['roundpercent'], label_size)},
        {'x': 9, 'y': 2, 'z': 2, 'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(shotzoneaggr_dic['visitor_team']['logo'])}},
        {'x': 11, 'y': 1.5, 'z': 2, 'marker': {'enabled': 0}, 'dataLabels': shotzonelabel(shotzoneaggr_dic['visitor_team']['blue_line']['roundpercent'], label_size)},
    ]

    return data_list

def shotzonechart_create(logger, ctitle, csubtitle, ismobile, request, shotzoneaggr_dic, bg_image):
    """ create shotzone chart """
    # pylint: disable=E0602
    logger.debug('shotmapchart_create()')

    variable_dic = variables_get(ismobile)

    data_list = shotzonedata_build(logger, ismobile, shotzoneaggr_dic)

    chart_options = {

        'chart': {
            'type': 'scatter',
            'plotBorderWidth': 0,
            'plotBackgroundImage': bg_image,
            'zoomType': 'xy',
            'height': variable_dic['shotzone_height_pctg'],
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(enabled=0),

        'tooltip': {'enabled': 0},

        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': 1,
                    'color': '#000000',
                    'style': {'textShadow': 0, 'textOutline': 0, 'fontSize': font_size},
                    'y': 11,
                    'format': '{point.jersey}',
                    'align': 'center',
                    'allowOverlap': 0,
                },
                'color': shot_sog_color,
                'lineColor': line_color,
            },
        },

        'xAxis': {
            'visible': 0,
            'labels': {'enabled': 0},
            'min': 0,
            'max': 20,
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
            'max': 20,
            'tickInterval': 0,
        },

        'series': [{'data': data_list}],
    }

    return chart_options

def gamecorsichart_create(logger, ctitle, csubtitle, ismobile, player_corsi_dic):
    """ create corsi chart for a certain game """
    # pylint: disable=E0602, R0915
    logger.debug('gamecorsichart_create()')

    variable_dic = variables_get(ismobile)

    # format data series in a way we need it
    data_list = {}
    # this dictionary is to create temporary bubble overlaps
    tmp_pos_dic = {}

    # plotlines will be calculated based on this dictionary
    shotsum_dic = {'shots': 0, 'shots_against': 0}

    # we scale the bars depending on amout of shots or shots-against
    scale_max = 0

    minmax_dic = {'x_min': None, 'x_max': 0, 'y_min': None, 'y_max': 0}

    for player in sorted(player_corsi_dic.values(), key=lambda x: (x['shots'])):
        # count shotsum
        shotsum_dic['shots'] += player['shots']
        shotsum_dic['shots_against'] += player['shots_against']

        if not minmax_dic['x_min'] or minmax_dic['x_min'] > player['shots']:
            minmax_dic['x_min'] = player['shots']
        if minmax_dic['x_max'] < player['shots']:
            minmax_dic['x_max'] = player['shots']
        if not minmax_dic['y_min'] or minmax_dic['y_min'] > player['shots_against']:
            minmax_dic['y_min'] = player['shots_against']
        if minmax_dic['y_max'] < player['shots_against']:
            minmax_dic['y_max'] = player['shots_against']

        tmp_dic = {
            'x': player['shots'],
            'y': player['shots_against'],
            'mx': player['shots'],
            'my': player['shots_against'],
            'z': math.ceil(player['toi']/60),
            # 'z': 4,
            'name': player['name'],
            'mtoi': '{0:02d}:{1:02d}'.format(*divmod(player['toi'], 60)),
            'jersey': player['jersey'],
            'labelrank': 1,
            }

        if scale_max < player['shots']:
            scale_max = player['shots']
        if scale_max < player['shots_against']:
            scale_max = player['shots_against']

        # hack to fix bubble overlaps
        pos = '{0}:{1} '.format(player['shots'], player['shots_against'])
        if pos in tmp_pos_dic:
            tmp_dic['x'] += 0.5
            tmp_dic['y'] += 0.5
            tmp_pos_dic[pos] = '{0}:{1} '.format(tmp_dic['x'], tmp_dic['y'])
        else:
            tmp_pos_dic[pos] = 1

        if 'line_number' in player:
            if player['line_number'] not in data_list:
                data_list[player['line_number']] = []
            tmp_dic['labelrank'] = 5 - player['line_number']
            data_list[player['line_number']].append(tmp_dic)
        else:
            tmp_dic['labelrank'] = 1
            if 4 not in data_list:
                data_list[4] = []
            data_list[4].append(tmp_dic)

    shotsum_dic['shots_avg'] = round(shotsum_dic['shots'] / len(player_corsi_dic.keys()), 0)
    shotsum_dic['shots_against_avg'] = round(shotsum_dic['shots_against'] / len(player_corsi_dic.keys()), 0)

    # adjust max values for the bars - min is already 0 so no adjustment needed
    minmax_dic['x_min'] = 0
    minmax_dic['y_min'] = 0
    minmax_dic['x_max'] += 2
    minmax_dic['y_max'] += 2

    chart_options = {

        'chart': {
            'type': 'bubble',
            'plotBorderWidth': 1,
            'zoomType': 'xy',
            'height': '120%',
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        'responsive': responsive_bubble(),
        'annotations': corner_annotations(ismobile, minmax_dic, _('Bad'), _('Dull'), _('Fun'), _('Good')),

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '<table class="w3-tiny">',
            'pointFormat': '<tr><td colspan="3"><b>{point.name} ({point.jersey})<b></td></tr>' +
                           '<tr><td>%s:</td><td>{point.mx}</td></tr>' % _('Shot attempts "for" at 5v5') +
                           '<tr><td>%s:</td><td>{point.my}</td></tr>' % _('Shot attempts "against" at 5v5') +
                           '<tr><td>%s:</td><td>{point.mtoi}m</td></tr>' % _('Time on Ice'),
            'footerFormat': '</table>',
            'followPointer': 1,
        },

        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': 1,
                    'style': {'textShadow': 0, 'textOutline': 0, 'fontSize': font_size},
                    'format': '{point.jersey}',
                },
                'color': 'rgba(189, 191, 193, 6)',
                'lineColor': line_color,
            },
            'bubble': {
                'minSize': 3,
                'maxSize': 50,
            }
        },

        'xAxis': {
            'gridLineWidth': 1,
            'title': title(_('Shot attempts "for" at 5v5'), font_size),
            'labels': {'style': {'fontSize': font_size}},
            'plotLines': [{'color': plotlines_color, 'width': 2, 'value': shotsum_dic['shots_avg']}],
            'min': 0,
            'max': minmax_dic['x_max'],
            'tickInterval': 1,
            'showFirstLabel': 1,
            'showLastLabel': 1,
        },
        'yAxis': {
            'title': title(_('Shot attempts "against" at 5v5'), font_size),
            'labels': {'style': {'fontSize': font_size},},
            'plotLines': [{'color': plotlines_color, 'width': 2, 'value': shotsum_dic['shots_against_avg']}],
            'min': 0,
            'max': minmax_dic['y_max'],
            'reversed': 1,
            'tickInterval': 1,
            'showFirstLabel': 1,
            'showLastLabel': 1,
        },

        'series': [],
    }

    line_dic = {1: _('1st line'), 2: _('2nd line'), 3: _('3rd line'), 4: _('4th line'), 5: _('5th line')}

    # data_dic = {1: '#333333', 2: '#595959', 3: '#8c8c8c', 4: '#bfbfbf', 5: '#f2f2f2'}
    data_dic = {1: line1_color, 2: line2_color, 3: line3_color, 4: line4_color, 5: line5_color}
    if len(data_list) == 1:
        chart_options['series'].append({'name': _('Player'), 'data': list(data_list.values())[0], 'zIndex': 1, 'marker': {'fillOpacity': 0.7}})
    else:
        for line in sorted(data_dic.keys()):
            if line in data_list:
                chart_options['series'].append({'name': '{0}'.format(line_dic[line]), 'data': data_list[line], 'zIndex': 5-line, 'color': data_dic[line], 'marker': {'fillOpacity': 0.7}})

    return chart_options

def gamecorsippctgchart_create(logger, ctitle, csubtitle, ismobile, player_corsi_dic):
    """ create corsi chart for a certain game """
    # pylint: disable=E0602
    logger.debug('gamecorsippctgchart_create()')

    variable_dic = variables_get(ismobile)

    # create x axis with player names
    x_list = []
    y_dic = {'shots': [], 'shots_against': []}

    shot_sum = 0
    count = 0
    for player in sorted(player_corsi_dic.values(), key=lambda x: x['cf_pctg'], reverse=True):

        x_list.append(player['name'])
        y_dic['shots'].append(player['cf_pctg'])
        y_dic['shots_against'].append(100 - player['cf_pctg'])
        count += 1
        shot_sum = shot_sum + player['cf_pctg']

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
        'tooltip': {'enabled': 0},

        'plotOptions': {
            'bar': {
                'stacking': 'percent',
                'dataLabels': {
                    'enabled': 1,
                    'format': '{y} %',
                    'useHTML': 0,
                    'style': {'fontSize': font_size, 'textOutline': 0, 'color': '#ffffff', 'fontWeight': 0}
                }
            }
        },

        'xAxis': {
            'categories': x_list,
            'title': title(''),
            'labels': {'style': {'fontSize': font_size},},
            'tickInterval': 1,
            'showFirstLabel': 1,
            'showLastLabel': 1,
        },

        'yAxis':
            {
                'title': title(_('Shot attempts (Percentage)'), font_size),
                'reversedStacks': 0,
                'tickInterval': 25,
                'maxPadding': 0.1,
                'labels': {'style': {'fontSize': font_size}},
                'plotLines': [{'color': plotlines_color, 'width': 3, 'value': int(shot_sum/count)}]
            },

        'series': [{
            'name': '{0} 5v5 (%)'.format(_('Shot attempts "for" at 5v5')),
            'data': y_dic['shots'],
            'color': chart_color3
        }, {
            'name': '{0} 5v5 (%)'.format(_('Shot attempts "against" at 5v5')),
            'data': y_dic['shots_against'],
            'color': chart_color1,
            'dataLabels': 0,
        }],

        'responsive': {
            'rules': [{
                'condition': {'maxWidth': 500},
                'chartOptions': {
                    'legend': {'verticalAlign': legend_valign_mobile, 'layout': 'horizontal', 'itemStyle': {'font-size': font_size_mobile}},
                    'xAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                    'yAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                    'plotOptions': {'bar': {'dataLabels': {'style': {'fontSize': '7px', 'textOutline': 0, 'color': '#ffffff', 'fontWeight': 0}}}}
                }
            }]
        }
    }
    return chart_options

def puckpossessionchart_create(logger, ctitle, csubtitle, ismobile, shotsum_dic, goal_dic, matchinfo_dic, color_dic):
    """ create area chart showing puck possession """
    # pylint: disable=E0602
    logger.debug('puckpossessionchart_create()')

    variable_dic = variables_get(ismobile)

    min_list = list(shotsum_dic['home_team'].keys())

    # max x value (OT or not OT) needed for annotation module
    x_max = min_list[-1]

    y1_list = []
    for min_, value in shotsum_dic['home_team'].items():

        # on the fly zero value fix at gamestart
        #if shotsum_dic['home_team'][min_] == 0 and shotsum_dic['visitor_team'][min_] == 0:
        #    # we need to modify "value" for home-team as this is used in the chart
        #    value = 1
        #    shotsum_dic['visitor_team'][min_] = 1

        # set marker on graph if there was a goal in this min
        if min_ in goal_dic['home_team']:
            y1_list.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['home_team_logo'])}, 'dataLabels': {'y': -15, 'style': {'fontSize': variable_dic['label_size']}, 'borderWidth': 1, 'backgroundColor': '#ffffff', 'borderColor': chart_color8, 'useHTML': 1, 'enabled': 1, 'color': chart_color8, 'format': '{0}'.format(goal_dic['home_team'][min_])}})
        elif min_ in goal_dic['visitor_team']:
            y1_list.append({'y' : value, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['visitor_team_logo'])}, 'dataLabels': {'y': -15, 'style': {'fontSize': variable_dic['label_size']}, 'borderWidth': 1, 'backgroundColor': '#ffffff', 'borderColor': chart_color8, 'useHTML': 1, 'enabled': 1, 'color': chart_color8, 'format': '{0}'.format(goal_dic['visitor_team'][min_])}})
        else:
            y1_list.append(value)

    y2_list = list(shotsum_dic['visitor_team'].values())

    chart_options = {

        'chart': {
            'type': 'areaspline',
            'height': '80%',
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        'responsive': responsive_y1(),
        'annotations': puckpossession_annotations(ismobile, x_max, matchinfo_dic['home_team_logo'], matchinfo_dic['visitor_team_logo']),

        'tooltip': {
            'pointFormat': '<span style="color:{series.color}">{series.name}</span>: <b>{point.percentage:.1f}%</b> ({point.y:,.0f} shots)<br/>',
            'split': 1,
        },

        'plotOptions': {
            'areaspline': {
                'stacking': 'percent',
                'lineColor': '#ffffff',
                'lineWidth': 2,
                'marker': {
                    'enabled': 0,
                    'symbol': 'diamond'},
                },
            },
        'xAxis': {
            'categories': min_list,
            'title': title(_('Game Time'), font_size, decoration=True),
            'labels': {'style': {'fontSize': font_size},},
            'tickInterval': 5,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'plotLines': [
                {'color': plotlines_color, 'width': 2, 'value': 20},
                {'color': plotlines_color, 'width': 2, 'value': 40},
                {'color': plotlines_color, 'width': 2, 'value': 60}
            ],
        },

        'yAxis': [
            {
                'title': title(_('Puck Posession (%)'), font_size),
                'plotLines': [{'color': plotlines_color, 'width': 2, 'value': 50}],
                'tickInterval': 25,
                'maxPadding': 0.1,
                'labels': {'style': {'fontSize': font_size},},
                'reversedStacks': 0,
            }],
        'series': [
            {'name': '{0}'.format(matchinfo_dic['home_team__shortcut']), 'data': y1_list, 'color': color_dic['home_team_color_primary'], 'zIndex': 2},
            {'name': '{0}'.format(matchinfo_dic['visitor_team__shortcut']), 'data': y2_list, 'color': color_dic['visitor_team_color_secondary'], 'zIndex': 1}
        ]
    }
    return chart_options


def pace_chart_get(logger, ctitle, csubtitle, ismobile, pace_dic):
    """ create chart 5v5 pace """
    # pylint: disable=E0602
    logger.debug('pace_chart_get()')

    variable_dic = variables_get(ismobile)

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
        'legend': legend(),
        'responsive': responsive_y1(),

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '',
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">CF60: {point.sum_shots_for_5v5_60}</span><br><span style="font-size: %s">CA60: {point.sum_shots_against_5v5_60}</span><br/>' % (font_size, font_size)
        },

        'xAxis': {
            'labels': {
                'enabled': 0
            },
            'tickInterval': 0,
        },

        'yAxis': {
            'title': title(ctitle, font_size),
            # 'tickInterval': 1,
            'maxPadding': 0.1,
            'min': pace_dic['y_min'] - 2,
            'max': pace_dic['y_max'] + 2,
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': pace_dic['y_avg'] - pace_dic['y_deviation']/2, 'to': pace_dic['y_avg'] + pace_dic['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': pace_dic['y_avg']}],
        },

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'data': pace_dic['data']}]

    }

    return chart_options

def shotrates_chart_get(logger, ctitle, csubtitle, ismobile, shotrates_dic):
    """ create chart 5v5 pace """
    # pylint: disable=E0602
    logger.debug('shotrates_chart_get()')

    variable_dic = variables_get(ismobile)


    minmax_dic = {
        'x_min': round(shotrates_dic['x_min'] - 1, 0),
        'y_min': round(shotrates_dic['y_min'] - 1, 0),
        'x_max': round(shotrates_dic['x_max'] + 1, 0),
        'y_max': round(shotrates_dic['y_max'] + 1, 0)
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
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">%s: {point.x}</span><br><span style="font-size: %s">%s: {point.y}</span><br/>' % (font_size, _('Corsi For per 60 minutes at 5v5 (Cf/60)'), font_size, _('Corsi Against per 60 minutes at 5v5 (Ca/60)'))
        },

        'xAxis': {
            'title': title(_('Corsi For per 60 minutes at 5v5 (Cf/60)'), font_size),
            'labels': {'style': {'fontSize': font_size}},
            'tickInterval': 1,
            'min': minmax_dic['x_min'],
            'max': minmax_dic['x_max'],
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'gridLineWidth': 1,
            'plotBands': [{'from': shotrates_dic['x_avg'] - shotrates_dic['x_deviation']/2, 'to': shotrates_dic['x_avg'] + shotrates_dic['x_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': shotrates_dic['x_avg']}],
        },

        'yAxis': {
            'title': title(_('Corsi Against per 60 minutes at 5v5 (Ca/60)'), font_size),
            'maxPadding': 0.1,
            'tickInterval': 1,
            'reversed': 1,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'min': minmax_dic['y_min'],
            'max': minmax_dic['y_max'],
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': shotrates_dic['y_avg'] - shotrates_dic['y_deviation']/2, 'to': shotrates_dic['y_avg'] + shotrates_dic['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': shotrates_dic['y_avg']}],
        },

        'annotations': corner_annotations(ismobile, minmax_dic, _('Bad'), _('Dull'), _('Fun'), _('Good')),

        'series': [{'zIndex': 2, 'name': _('Standard Deviation'), 'color': plotlines_color, 'marker': {'symbol': 'square'}, 'data': shotrates_dic['data']}]

    }

    return chart_options

def shotshare_chart_get(logger, ctitle, csubtitle, ismobile, shotshare_dic):
    """ create chart 5v5 pace """
    # pylint: disable=E0602
    logger.debug('pace_chart_get()')

    variable_dic = variables_get(ismobile)

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
        'legend': legend(enabled=1),
        'responsive': responsive_y1(),

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '',
            'pointFormat': '<span><b>{point.team_name}</b></span></br><span style="font-size: %s">CF60: {point.sum_shots_for_5v5_60}</span><br><span style="font-size: %s">CA60: {point.sum_shots_against_5v5_60}</span><br/>' % (font_size, font_size)
        },

        'xAxis': {
            'labels': {
                'enabled': 0
            },
            'tickInterval': 0,
        },

        'yAxis': {
            'title': title(ctitle, font_size),
            # 'tickInterval': 1,
            'maxPadding': 0.1,
            'min': shotshare_dic['y_min'] - 2,
            'max': shotshare_dic['y_max'] + 2,
            'labels': {'style': {'fontSize': font_size},},
            'gridLineWidth': 1,
            'plotBands': [{'from': shotshare_dic['y_avg'] - shotshare_dic['y_deviation']/2, 'to': shotshare_dic['y_avg'] + shotshare_dic['y_deviation']/2, 'color': chart_color6}],
            'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value': shotshare_dic['y_avg']}],
        },

        'series': [{'zIndex': 1, 'name': _('Standard Deviation'), 'color': plotlines_color, 'data': shotshare_dic['data']}]

    }

    return chart_options

def rebound_overview_chart(logger, ctitle, csubtitle, ismobile, data_dic):
    """ create chart for rebound statistics """
    # pylint: disable=E0602
    logger.debug('rebound_overview_chart()')

    variable_dic = variables_get(ismobile)

    chart_options = {

        'chart': {
            'type': 'bar',
            'height': '120%',
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        'responsive': responsive_y1_label(),

        # 'plotOptions': { 'series': {'stacking': 'normal'}},
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': 1,
                    'format': '{y} %'
                }
            }
        },

        'xAxis': {
            'categories': data_dic['x_category'],
            'title': title(''),
            'maxPadding': 0.1,
            'labels': {'useHTML': 1, 'align': 'center'},
        },

        'yAxis': {
            'title': title(_('Rebound percentage'), font_size),
            'maxPadding': 0.1,
            'labels': {'style': {'fontSize': font_size}},
            'tickInterval': 5,
        },

        'series': [
            {'index': 0, 'name': _('leading to own goal'), 'data': data_dic['goals_rebound_for_pctg'], 'color': chart_color3},
            {'index': 1, 'name': _('leading to goal against'), 'data': data_dic['goals_rebound_against_pctg'], 'color': chart_color2},
        ]
    }
    return chart_options

def break_overview_chart(logger, ctitle, csubtitle, ismobile, data_dic):
    """ create chart for break statistics """
    # pylint: disable=E0602
    logger.debug('break_overview_chart()')

    variable_dic = variables_get(ismobile)

    chart_options = {

        'chart': {
            'type': 'bar',
            'height': '120%',
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        'responsive': responsive_y1_label(),

        # 'plotOptions': { 'series': {'stacking': 'normal'}},
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': 1,
                    'format': '{y} %'
                }
            }
        },

        'xAxis': {
            'categories': data_dic['x_category'],
            'title': title(''),
            'maxPadding': 0.1,
            'labels': {'useHTML': 1, 'align': 'center'},
        },

        'yAxis': {
            'title': title(_('break percentage'), font_size),
            'maxPadding': 0.1,
            'labels': {'style': {'fontSize': font_size}},
            'tickInterval': 5,
        },

        'series': [
            {'index': 0, 'name': _('leading to own goal'), 'data': data_dic['goals_break_for_pctg'], 'color': chart_color3},
            {'index': 1, 'name': _('leading to goal against'), 'data': data_dic['goals_break_against_pctg'], 'color': chart_color2},
        ]
    }
    return chart_options
