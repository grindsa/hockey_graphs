# -*- coding: utf-8 -*-
""" list of functions for shots """
import math
# pylint: disable=E0401, C0302
from rest.functions.helper import highlowabs_get
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

        'exporting': exporting(filename=ctitle, sourcewidth=variable_dic['export_sourcewidth'], sourceheight=variable_dic['export_sourceheight']),
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

        'exporting': exporting(filename=ctitle, sourcewidth=variable_dic['export_sourcewidth'], sourceheight=variable_dic['export_sourceheight']/80*110),
        'credits': credit(),
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

def shotmapchart_create(logger, ctitle, csubtitle, ismobile, shotmap_list, player_chart=False):
    """ create shotmap """
    # pylint: disable=E0602
    logger.debug('shotmapchart_create()')

    variable_dic = variables_get(ismobile)

    if player_chart:
        datalabels_enabled = 0
        scatter_radius = 5
        scatter_radius_responsive = 4
    else:
        datalabels_enabled = 1
        scatter_radius = 15
        scatter_radius_responsive = 12

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

    # print(len(data_dic[4]))

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
                    'enabled': datalabels_enabled,
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
            {'name': _('missed'), 'zIndex': 1, 'data': data_dic[2], 'color': shot_missed_color, 'marker': {'lineColor': chart_color2, 'lineWidth': 1, 'symbol': 'circle', 'radius': scatter_radius}},
            {'name': _('Shots on Goal'), 'color': shot_sog_color, 'zIndex': 2, 'data': data_dic[1], 'marker': {'lineColor': '#2083df', 'lineWidth': 1, 'radius': scatter_radius, 'symbol': 'circle'}},
            {'name': _('blocked'), 'zIndex': 3, 'color': shot_blocked_color, 'data': data_dic[3], 'marker': {'symbol': 'circle', 'radius': scatter_radius}},
            {'name': _('Post hit'), 'zIndex': 4, 'color': chart_color4, 'data': data_dic[5], 'marker': {'symbol': 'circle', 'radius': scatter_radius}},
            {'name': _('Goals'), 'zIndex': 5, 'color': shot_goal_color, 'data': data_dic[4], 'marker': {'symbol': 'circle', 'radius': scatter_radius}},
            ],

        'responsive': {
            'rules': [{
                'condition': {'maxWidth': 500},
                'chartOptions': {
                    'series': [
                        {'name': _('missed'), 'zIndex': 1, 'data': data_dic[2], 'color': shot_missed_color, 'marker': {'lineColor': chart_color2, 'lineWidth': 1, 'symbol': 'circle', 'radius': scatter_radius_responsive}},
                        {'name': _('Shots on Goal'), 'zIndex': 2, 'color': shot_sog_color, 'data': data_dic[1], 'marker': {'lineColor': '#2083df', 'lineWidth': 1, 'radius': scatter_radius_responsive, 'symbol': 'circle'}},
                        {'name': _('blocked'), 'zIndex': 3, 'color': shot_blocked_color, 'data': data_dic[3], 'marker': {'symbol': 'circle', 'radius': scatter_radius_responsive}},
                        {'name': _('Post hit'), 'zIndex': 4, 'color': chart_color4, 'data': data_dic[5], 'marker': {'symbol': 'circle', 'radius': scatter_radius_responsive}},
                        {'name': _('Goals'), 'zIndex': 5, 'color': shot_goal_color, 'data': data_dic[4], 'marker': {'symbol': 'circle', 'radius': scatter_radius_responsive}},
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

def gameplayercorsichart_create(logger, ctitle, csubtitle, ismobile, player_corsi_dic):
    """ create corsi chart for a certain game """
    # pylint: disable=E0602, R0915
    logger.debug('gameplayercorsichart_create()')

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

# pylint: disable=R0914
def gamecorsichart_create(logger, ctitle, csubtitle, ismobile, corsi_dic, plotbands_list, matchinfo_dic, color_dic):
    # pylint: disable=E0602
    """ create shotsum chart """
    logger.debug('shotsumchart_create()')

    variable_dic = variables_get(ismobile)

    minute_list = corsi_dic.keys()

    value_list = corsi_dic.values()
    abs_value = highlowabs_get(logger, value_list)

    if ismobile:
        img_width = 30
        home_y = 10
        visitor_y = 120
        export_sourcewidth = 373
        export_sourceheight =  298
    else:
        img_width = 85
        home_y = 30
        visitor_y = 380
        export_sourcewidth = 800
        export_sourceheight = 640

    chart_options = {

        'chart': {
            'type': 'line',
            'height': '80%',
            'alignTicks': 0,
            'style': chartstyle()
        },
        'exporting': exporting(filename=ctitle, sourcewidth=export_sourcewidth, sourceheight=export_sourceheight),
        #'exporting': {
        #    'sourceWidth': 800,
        #    'sourceHeight': 640
        #},
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'plotOptions': plotoptions_marker_disable('line'),
        'legend': legend(),
        'responsive': responsive_y1(),
        'credits': credit(),
        'tooltip': {
            'useHTML': 0,
            'headerFormat': '',
            'pointFormat': '<b>{point.x} %s</b><br>{series.name}: {point.y}' % (_('min')),
            'followPointer': 1,
        },

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
            'plotBands': plotbands_list,
        },

        'annotations': [{
            'shapes': [
                {'type': 'image', 'src': matchinfo_dic['visitor_team_logo'], 'width': img_width, 'height': img_width, 'point': {'x': 2, 'y': home_y, 'xAxis': 0}},
                {'type': 'image', 'src': matchinfo_dic['home_team_logo'], 'width': img_width, 'height': img_width, 'point': {'x': 2, 'y': visitor_y, 'xAxis': 0}},
            ],
        }],

        'yAxis':[
            {
                'title': title(_('Shots per minute'), font_size),
                'max': abs_value + 1,
                'min': (abs_value + 1) * -1,
                'maxPadding': 0.1,
                'labels': labels(),
                'plotLines': [{'color': plotlines_color, 'width': 2, 'value': 0}],
            }],

        'series': [{
            'name': 'Corsi {0}'.format(_('cumulated')),
            'data': value_list,
            'step': 'right',
            'color': '#000000',
            'lineWidth': variable_dic['linewidth']
        }, {
            'name': '{0} {1}'.format(_('Goals'), matchinfo_dic['home_team__shortcut']),
            'color': color_dic['home_team_color_primary'],
            'marker': {'symbol': 'circle'},
            'type': 'scatter',
        }, {
            'name': '{0} {1}'.format(_('Goals'), matchinfo_dic['visitor_team__shortcut']),
            'color': color_dic['visitor_team_color_secondary'],
            'marker': {'symbol': 'circle'},
            'type': 'scatter',
        }]
    }

    return chart_options


def shotmapchart_new_create(logger, ctitle, csubtitle, ismobile, shotmap_dic, matchinfo_dic, player_chart=False):
    """ create shotmap """
    # pylint: disable=E0602
    logger.debug('shotmapchart_create()')

    variable_dic = variables_get(ismobile)

    if ismobile:
        img_width = 25
        home_x = -26
        home_y = 85
        visitor_x = 22
        visitor_y = 85
        scatter_radius = 5
    else:
        img_width = 55
        home_x = -26
        home_y = 170
        visitor_x = 22
        visitor_y = 170
        scatter_radius = 8

    # data_dic = {'home_team': {1 :[], 2: [], 3: [], 4: [], 5: []}, 'visitor_team': {1 :[], 2: [], 3: [], 4: [], 5: []}}
    data_dic = {}
    for team, shotmap_list in shotmap_dic.items():
        data_dic[team] = {1 :[], 2: [], 3: [], 4: [], 5: []}
        cnt = 0
        for shot in sorted(shotmap_list, key=lambda x: (x['match_shot_resutl_id'])):
            cnt += 1
            tmp_dic = {
                'x': shot['meters_x'],
                'y': shot['meters_y'],
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

            if shot['match_shot_resutl_id'] in data_dic[team]:
                data_dic[team][shot['match_shot_resutl_id']].append(tmp_dic)


    # bg_image = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTkwIiBoZWlnaHQ9IjU5NSIgdmlld0JveD0iMCAwIDU5MCA1OTUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiPjx0aXRsZT5Hcm91cCBDb3B5PC90aXRsZT48ZGVmcz48cGF0aCBkPSJNNzkgMzMwYzIwLjU0IDAgMzctMTYuNTY1IDM3LTM3cy0xNi41NjUtMzctMzctMzd2NzR6IiBpZD0iYSIvPjxtYXNrIGlkPSJiIiB4PSIwIiB5PSIwIiB3aWR0aD0iMzciIGhlaWdodD0iNzQiIGZpbGw9IiNmZmYiPjx1c2UgeGxpbms6aHJlZj0iI2EiLz48L21hc2s+PC9kZWZzPjxnIHRyYW5zZm9ybT0icm90YXRlKDkwIDI5Mi41IDI5NSkiIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+PHBhdGggZD0iTTE0OCAwaDQ0MXY1ODRIMTQ4UzIxLjUwNCA1ODQgLjcwMyA0NDAuNDczVjE0NS4yMDdTMTIuOTIyIDkuOTYxIDE0OCAweiIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9IjYiIGZpbGw9IiNGRkYiLz48cGF0aCBkPSJNNTg3IDM4MVYyMDVjLTQ4LjYwMSAwLTg4IDM5LjM5OS04OCA4OHMzOS4zOTkgODggODggODh6IiBzdHJva2U9IiMyNTc1RDIiIHN0cm9rZS13aWR0aD0iMyIvPjxwYXRoIGQ9Ik00MTkgMS41djU4MiIgc3Ryb2tlPSIjMjU3NUQyIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiLz48cGF0aCBkPSJNNzkuNSAyMS41djU0MyIgc3Ryb2tlPSIjRUUyQTQyIiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiLz48dXNlIHN0cm9rZT0iI0VFMkE0MiIgbWFzaz0idXJsKCNiKSIgc3Ryb2tlLXdpZHRoPSI2IiBmaWxsLW9wYWNpdHk9Ii4zIiBmaWxsPSIjMjU3NUQyIiB4bGluazpocmVmPSIjYSIvPjxwYXRoIGQ9Ik0xNzkuNSA2MC41djIwNy4wMDJNMjE5LjUgNjAuNXYyMDcuMDAyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBzdHJva2Utd2lkdGg9IjMiIGZpbGw9IiNGRkYiIGN4PSIxOTkiIGN5PSIxNjQiIHI9Ijg5Ii8+PHBhdGggZD0iTTE0Ny41IDE1Ni41aDM5TTE0Ny41IDE3MS41aDM5TTIxMi41IDE1Ni41aDM5TTIxMi41IDE3MS41aDM5TTE4Ni41IDEzNC41djIyTTIxMi41IDEzNC41djIyTTE4Ni41IDE3MS41djIyTTIxMi41IDE3MS41djIyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBmaWxsPSIjRUUyQTQyIiBjeD0iMTk5IiBjeT0iMTY0IiByPSI2Ii8+PGNpcmNsZSBzdHJva2U9IiNFRTJBNDIiIGZpbGw9IiNFRTJBNDIiIGN4PSI0NDMiIGN5PSIxNjQiIHI9IjYiLz48cGF0aCBkPSJNMTc5LjUgMzIyLjV2MjA3LjAwMk0yMTkuNSAzMjIuNXYyMDcuMDAyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBzdHJva2Utd2lkdGg9IjMiIGZpbGw9IiNGRkYiIGN4PSIxOTkiIGN5PSI0MjYiIHI9Ijg5Ii8+PHBhdGggZD0iTTE0Ny41IDQxOC41aDM5TTE0Ny41IDQzMy41aDM5TTIxMi41IDQxOC41aDM5TTIxMi41IDQzMy41aDM5TTE4Ni41IDM5Ni41djIyTTIxMi41IDM5Ni41djIyTTE4Ni41IDQzMy41djIyTTIxMi41IDQzMy41djIyIiBzdHJva2U9IiNFRTJBNDIiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InNxdWFyZSIvPjxjaXJjbGUgc3Ryb2tlPSIjRUUyQTQyIiBmaWxsPSIjRUUyQTQyIiBjeD0iMTk5IiBjeT0iNDI2IiByPSI2Ii8+PGNpcmNsZSBzdHJva2U9IiNFRTJBNDIiIGZpbGw9IiNFRTJBNDIiIGN4PSI0NDMiIGN5PSI0MjYiIHI9IjYiLz48cGF0aCBkPSJNMTQ4IDBoNDQxdjU4NEgxNDhTMjEuNTA0IDU4NCAuNzAzIDQ0MC40NzNWMTQ1LjIwN1MxMi45MjIgOS45NjEgMTQ4IDB6IiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iNiIvPjwvZz48L3N2Zz4="
    # bg_image = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+DQo8IS0tIENyZWF0ZWQgd2l0aCBJbmtzY2FwZSAoaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvKSAtLT4NCjxzdmc6c3ZnIHhtbG5zOmk9Imh0dHA6Ly9ucy5hZG9iZS5jb20vQWRvYmVJbGx1c3RyYXRvci8xMC4wLyIgeG1sbnM6c3ZnPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHZlcnNpb249IjEuMCIgd2lkdGg9Ijc0OC40OTc5OSIgaGVpZ2h0PSIzNDcuNSIgdmlld0JveD0iMCAwIDc0OC40OTggMzQ3LjUiIGlkPSJzdmcyIiB4bWw6c3BhY2U9InByZXNlcnZlIj48c3ZnOmRlZnMgaWQ9ImRlZnM0OCIvPg0KCQ0KCQkNCgkJCTxuYW1lZHZpZXcgY3VycmVudC1sYXllcj0ic3ZnMiIgd2luZG93LXk9IjM0MyIgd2luZG93LXg9IjE2NjUiIGN5PSIzMjMuNjk3NTYiIGN4PSI0NDQuMjYzMzMiIHpvb209IjAuOTM5MDAyNDUiIHBhZ2Vjb2xvcj0iI2ZmZmZmZiIgYm9yZGVyY29sb3I9IiM2NjY2NjYiIGJvcmRlcm9wYWNpdHk9IjEuMCIgcGFnZW9wYWNpdHk9IjAuMCIgcGFnZXNoYWRvdz0iMiIgd2luZG93LXdpZHRoPSI3NTkiIHdpbmRvdy1oZWlnaHQ9IjUzOSIgaWQ9ImJhc2UiPg0KCQkJPC9uYW1lZHZpZXc+DQoJCQ0KCQkJPHN2ZzpwYXR0ZXJuIHZpZXdCb3g9IjAgLTQ1MCA4MDAgNDUwIiBpZD0icGF0dGVybjE1NjAiIHBhdHRlcm5Vbml0cz0idXNlclNwYWNlT25Vc2UiIGhlaWdodD0iNDUwIiB3aWR0aD0iODAwIiB5PSI1NDQuOTY0IiB4PSI0NS45NTgiPg0KCQkJPHN2ZzpnIGlkPSJnNiI+DQoJCQkJPHN2Zzpwb2x5Z29uIGlkPSJwb2x5Z29uOCIgcG9pbnRzPSIwLDAgODAwLDAgODAwLTQ1MCAwLTQ1MCAiIGZpbGw9Im5vbmUiIGk6a25vY2tvdXQ9Ik9mZiIvPg0KCQkJPC9zdmc6Zz4NCgkJPC9zdmc6cGF0dGVybj4NCgkJDQoJCQk8c3ZnOnBhdHRlcm4gdmlld0JveD0iMCAtNDUwIDgwMCA0NTAiIGlkPSJwYXR0ZXJuMTU2NCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgaGVpZ2h0PSI0NTAiIHdpZHRoPSI4MDAiIHk9IjU0NC45NjQiIHg9IjQ1Ljk1OCI+DQoJCQk8c3ZnOmcgaWQ9ImcxMSI+DQoJCQkJPHN2Zzpwb2x5Z29uIGlkPSJwb2x5Z29uMTMiIHBvaW50cz0iMCwwIDgwMCwwIDgwMC00NTAgMC00NTAgIiBmaWxsPSJub25lIiBpOmtub2Nrb3V0PSJPZmYiLz4NCgkJCTwvc3ZnOmc+DQoJCTwvc3ZnOnBhdHRlcm4+DQoJCTxzdmc6ZyBpZD0iTGF5ZXJfMSI+DQoJCQk8c3ZnOnBhdGggZD0iTSAxMDUuMzc1LDIuMDAyIEwgNjQzLjEyNCwyLjAwMiBDIDcwMC4yMTUsMi4wMDIgNzQ2LjQ5Niw0My4zNDggNzQ2LjQ5Niw5NC4zNSBMIDc0Ni40OTYsMjUzLjE0OCBDIDc0Ni40OTYsMzA0LjE1MSA3MDAuMjE1LDM0NS40OTcgNjQzLjEyNCwzNDUuNDk3IEwgMTA1LjM3NSwzNDUuNDk3IEMgNDguMjg0LDM0NS40OTcgMi4wMDMsMzA0LjE1MSAyLjAwMywyNTMuMTQ4IEwgMi4wMDMsOTQuMzUxIEMgMi4wMDIsNDMuMzQ4IDQ4LjI4NCwyLjAwMiAxMDUuMzc1LDIuMDAyIHogIiBzdHlsZT0iZmlsbDp3aGl0ZTtzdHJva2U6YmxhY2s7c3Ryb2tlLXdpZHRoOjQuMDA0NDk5OTE7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLWxpbmVqb2luOnJvdW5kIiBpZD0icmVjdDIyMDYiLz4NCgkJCQ0KCQkJCTxzdmc6ZWxsaXBzZSBjeD0iMzc2LjczOTk5IiBjeT0iMTcwLjAyOTAxIiByeD0iMzcuMzIwOTk5IiByeT0iMzguMjA5OTk5IiBzdHlsZT0iZmlsbDpub25lO3N0cm9rZTojNDZiO3N0cm9rZS13aWR0aDozLjAwOTcwMDA2O3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZCIgaWQ9InBhdGgyMjA4Ii8+IA0KCQkJDQoJCQkJPHN2ZzplbGxpcHNlIGN4PSIyNDkuMDE5IiBjeT0iODIuMTY4OTk5IiByeD0iNS4yNjkwMDAxIiByeT0iNS4zMzQwMDAxIiBzdHlsZT0iZmlsbDojYzMzO3N0cm9rZTojZTI0YjVhO3N0cm9rZS13aWR0aDowLjUwMTYwMDAzO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZCIgaWQ9InBhdGgyMjEwIi8+IA0KCQkJDQoJCQkJPHN2ZzplbGxpcHNlIGN4PSIyNDkuMDE5IiBjeT0iMjU4LjQxMTk5IiByeD0iNS4yNjkwMDAxIiByeT0iNS4zMzUiIHN0eWxlPSJmaWxsOiNjMzM7c3Ryb2tlOiNlMjRiNWE7c3Ryb2tlLXdpZHRoOjAuNTAxNjAwMDM7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLWxpbmVqb2luOnJvdW5kIiBpZD0icGF0aDIyMTIiLz4gDQoJCQkNCgkJCQk8c3ZnOmVsbGlwc2UgY3g9IjUwNC4wMTkwMSIgY3k9IjI1OC40MTE5OSIgcng9IjUuMjY5MDAwMSIgcnk9IjUuMzM1IiBzdHlsZT0iZmlsbDojYzMzO3N0cm9rZTojZTI0YjVhO3N0cm9rZS13aWR0aDowLjUwMTYwMDAzO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZCIgaWQ9InBhdGgyMjE0Ii8+IA0KCQkJDQoJCQkJPHN2ZzplbGxpcHNlIGN4PSI1MDQuMDE5MDEiIGN5PSI4Mi4xNjg5OTkiIHJ4PSI1LjI2OTAwMDEiIHJ5PSI1LjMzNDAwMDEiIHN0eWxlPSJmaWxsOiNjMzM7c3Ryb2tlOiNlMjRiNWE7c3Ryb2tlLXdpZHRoOjAuNTAxNjAwMDM7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLWxpbmVqb2luOnJvdW5kIiBpZD0icGF0aDIyMTYiLz4gDQoJCQkNCgkJCQk8c3ZnOmxpbmUgaWQ9InBhdGgyMjE4IiBmaWxsPSJub25lIiBzdHJva2U9IiNDQzMzMzMiIHN0cm9rZS13aWR0aD0iMi45OTc2IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1kYXNoYXJyYXk9IjguOTkyOSA4Ljk5MjkiIHgxPSIzNzYuOTk3OTkiIHkxPSI3Ljg4MDAwMDEiIHgyPSIzNzcuMzQzOTkiIHkyPSIzNDUuOTk3OTkiIHN0eWxlPSJmaWxsOm5vbmU7c3Ryb2tlOiNjMzM7c3Ryb2tlLXdpZHRoOjIuOTk3NjAwMDg7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLWRhc2hhcnJheTo4Ljk5MjksIDguOTkyOSIvPg0KCQkJPHN2ZzpsaW5lIGlkPSJwYXRoMzA5MyIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjNDQ2NkJCIiBzdHJva2Utd2lkdGg9IjguMDI1OCIgeDE9IjIyNy41MTE5OSIgeTE9IjMuNTgyOTk5OSIgeDI9IjIyNy43NyIgeTI9IjM0My40ODQwMSIgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2U6IzQ2YjtzdHJva2Utd2lkdGg6OC4wMjU3OTk3NSIvPg0KCQkJPHN2ZzpsaW5lIGlkPSJwYXRoMzA5NSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjNDQ2NkJCIiBzdHJva2Utd2lkdGg9IjguMDI1OCIgeDE9IjUyNi42MzIwMiIgeTE9IjMuOTkzIiB4Mj0iNTI2LjYzNTk5IiB5Mj0iMzQzLjQ4NDAxIiBzdHlsZT0iZmlsbDpub25lO3N0cm9rZTojNDZiO3N0cm9rZS13aWR0aDo4LjAyNTc5OTc1Ii8+DQoJCQk8c3ZnOnBhdGggZD0iTSAxNzAuNjcxLDI1Ni43MyBDIDE3MC42NzEsMjc4LjgwMiAxNTIuMzc3LDI5Ni43MTYgMTI5LjgzNywyOTYuNzE2IEMgMTA3LjI5NywyOTYuNzE2IDg5LjAwMywyNzguODAyIDg5LjAwMywyNTYuNzMgQyA4OS4wMDMsMjM0LjY1NyAxMDcuMjk3LDIxNi43NDIgMTI5LjgzNywyMTYuNzQyIEMgMTUyLjM3NywyMTYuNzQyIDE3MC42NzEsMjM0LjY1NyAxNzAuNjcxLDI1Ni43MyB6IE0gMTIwLjYxNywyMTYuNzQyIEwgMTIwLjYxNywyMDYuOTY5IE0gMTM4LjE4LDIwNi45NjggTCAxMzguMTgsMjE3LjYzIE0gMTM5LjkzNiwyOTYuNzE2IEwgMTM5LjkzNiwzMDYuNDkxIE0gMTE5LjczOSwyOTcuNjA1IEwgMTE5LjczOSwzMDYuNDkyIiBzdHlsZT0iZmlsbDpub25lO3N0cm9rZTojYzMzO3N0cm9rZS13aWR0aDozLjAwOTcwMDA2O3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZCIgaWQ9InBhdGgyNSIvPg0KCQkJPHN2ZzpwYXRoIGQ9Ik0gMTM2LjU4NiwyNTcuOTQxIEMgMTM2LjU4NiwyNjEuMjg0IDEzMy45MDUsMjYzLjk5NyAxMzAuNjAzLDI2My45OTcgQyAxMjcuMzAxLDI2My45OTcgMTI0LjYyLDI2MS4yODQgMTI0LjYyLDI1Ny45NDEgQyAxMjQuNjIsMjU0LjU5OSAxMjcuMzAxLDI1MS44ODYgMTMwLjYwMywyNTEuODg2IEMgMTMzLjg5OSwyNTEuODg2IDEzNi41NzYsMjU0LjU4NSAxMzYuNTg2LDI1Ny45MjEiIHN0eWxlPSJmaWxsOiNjMzMiIGlkPSJwYXRoMjQyMDMiLz4NCgkJCTxzdmc6cGF0aCBkPSJNIDE3MC42NzEsODEuNzI5IEMgMTcwLjY3MSwxMDMuODAyIDE1Mi4zNzcsMTIxLjcxNyAxMjkuODM3LDEyMS43MTcgQyAxMDcuMjk3LDEyMS43MTcgODkuMDAzLDEwMy44MDIgODkuMDAzLDgxLjcyOSBDIDg5LjAwMyw1OS42NTYgMTA3LjI5Nyw0MS43NDIgMTI5LjgzNyw0MS43NDIgQyAxNTIuMzc3LDQxLjc0MiAxNzAuNjcxLDU5LjY1NyAxNzAuNjcxLDgxLjcyOSB6IE0gMTIwLjYxNyw0MS43NDIgTCAxMjAuNjE3LDMxLjk2OCBNIDEzOC4xOCwzMS45NjggTCAxMzguMTgsNDIuNjMxIE0gMTM5LjkzNiwxMjEuNzE3IEwgMTM5LjkzNiwxMzEuNDkxIE0gMTE5LjczOSwxMjIuNjA1IEwgMTE5LjczOSwxMzEuNDkxIiBzdHlsZT0iZmlsbDpub25lO3N0cm9rZTojYzMzO3N0cm9rZS13aWR0aDozLjAwOTcwMDA2O3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZCIgaWQ9InBhdGgyOCIvPg0KCQkJPHN2ZzpwYXRoIGQ9Ik0gMTM2LjI4NCw4MS42OTkgQyAxMzYuMjg0LDg1LjA0MiAxMzMuNjAzLDg3Ljc1NCAxMzAuMzAxLDg3Ljc1NCBDIDEyNi45OTcsODcuNzU0IDEyNC4zMTcsODUuMDQyIDEyNC4zMTcsODEuNjk5IEMgMTI0LjMxNyw3OC4zNTcgMTI2Ljk5OCw3NS42NDQgMTMwLjMwMSw3NS42NDQgQyAxMzMuNTk3LDc1LjY0NCAxMzYuMjczLDc4LjM0MyAxMzYuMjg0LDgxLjY3OCIgc3R5bGU9ImZpbGw6I2MzMyIgaWQ9InBhdGgyNDE5MSIvPg0KCQkJPHN2ZzpwYXRoIGQ9Ik0gNjU2LjY3MSw4MS43MjkgQyA2NTYuNjcxLDEwMy44MDIgNjM4LjM3NywxMjEuNzE3IDYxNS44MzcsMTIxLjcxNyBDIDU5My4yOTcsMTIxLjcxNyA1NzUuMDAzLDEwMy44MDIgNTc1LjAwMyw4MS43MjkgQyA1NzUuMDAzLDU5LjY1NiA1OTMuMjk3LDQxLjc0MiA2MTUuODM3LDQxLjc0MiBDIDYzOC4zNzcsNDEuNzQyIDY1Ni42NzEsNTkuNjU3IDY1Ni42NzEsODEuNzI5IHogTSA2MDYuNjE3LDQxLjc0MiBMIDYwNi42MTcsMzEuOTY4IE0gNjI0LjE3OSwzMS45NjggTCA2MjQuMTc5LDQyLjYzMSBNIDYyNS45MzYsMTIxLjcxNyBMIDYyNS45MzYsMTMxLjQ5MSBNIDYwNS43MzksMTIyLjYwNSBMIDYwNS43MzksMTMxLjQ5MSIgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2U6I2MzMztzdHJva2Utd2lkdGg6My4wMDk3MDAwNjtzdHJva2UtbGluZWNhcDpyb3VuZDtzdHJva2UtbGluZWpvaW46cm91bmQiIGlkPSJwYXRoMzEiLz4NCgkJCTxzdmc6cGF0aCBkPSJNIDYyMi40NjcsODEuNjk5IEMgNjIyLjQ2Nyw4NS4wNDIgNjE5Ljc4NSw4Ny43NTQgNjE2LjQ4Myw4Ny43NTQgQyA2MTMuMTgxLDg3Ljc1NCA2MTAuNSw4NS4wNDIgNjEwLjUsODEuNjk5IEMgNjEwLjUsNzguMzU3IDYxMy4xODEsNzUuNjQ0IDYxNi40ODMsNzUuNjQ0IEMgNjE5Ljc3OSw3NS42NDQgNjIyLjQ1Niw3OC4zNDMgNjIyLjQ2Niw4MS42NzgiIHN0eWxlPSJmaWxsOiNjMzMiIGlkPSJwYXRoMjQxNzkiLz4NCgkJCTxzdmc6cGF0aCBkPSJNIDY1Ni42NzEsMjU2LjczIEMgNjU2LjY3MSwyNzguODAyIDYzOC4zNzcsMjk2LjcxNiA2MTUuODM3LDI5Ni43MTYgQyA1OTMuMjk3LDI5Ni43MTYgNTc1LjAwMywyNzguODAyIDU3NS4wMDMsMjU2LjczIEMgNTc1LjAwMywyMzQuNjU3IDU5My4yOTcsMjE2Ljc0MiA2MTUuODM3LDIxNi43NDIgQyA2MzguMzc3LDIxNi43NDIgNjU2LjY3MSwyMzQuNjU3IDY1Ni42NzEsMjU2LjczIHogTSA2MDYuNjE3LDIxNi43NDIgTCA2MDYuNjE3LDIwNi45NjkgTSA2MjQuMTc5LDIwNi45NjggTCA2MjQuMTc5LDIxNy42MyBNIDYyNS45MzYsMjk2LjcxNiBMIDYyNS45MzYsMzA2LjQ5MSBNIDYwNS43MzksMjk3LjYwNSBMIDYwNS43MzksMzA2LjQ5MiIgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2U6I2MzMztzdHJva2Utd2lkdGg6My4wMDk3MDAwNjtzdHJva2UtbGluZWNhcDpyb3VuZDtzdHJva2UtbGluZWpvaW46cm91bmQiIGlkPSJwYXRoMzQiLz4NCgkJCTxzdmc6cGF0aCBkPSJNIDYyMi40NjYsMjU3Ljk0MSBDIDYyMi40NjYsMjYxLjI4NCA2MTkuNzg1LDI2My45OTcgNjE2LjQ4MywyNjMuOTk3IEMgNjEzLjE3OSwyNjMuOTk3IDYxMC40OTksMjYxLjI4NCA2MTAuNDk5LDI1Ny45NDEgQyA2MTAuNDk5LDI1NC41OTkgNjEzLjE4LDI1MS44ODYgNjE2LjQ4MywyNTEuODg2IEMgNjE5Ljc3OSwyNTEuODg2IDYyMi40NTUsMjU0LjU4NSA2MjIuNDY2LDI1Ny45MjEiIHN0eWxlPSJmaWxsOiNjMzMiIGlkPSJwYXRoMjQxNjciLz4NCgkJCTxzdmc6cGF0dGVybiBwYXR0ZXJuVHJhbnNmb3JtPSJtYXRyaXgoMC4xNjUxIDAgMCAtMC4xNjcgLTY2NzcuMDI4MyAtOTgwMi42MjIxKSIgeGxpbms6aHJlZj0iI3BhdHRlcm4xNTY0IiBpZD0icGF0aDE0NTQ1XzFfIj4NCgkJCTwvc3ZnOnBhdHRlcm4+DQoJCQk8c3ZnOnBhdGggZD0iTSA2Ni40ODQsMTkyLjkyMyBDIDY2LjQ4NCwxOTIuOTIzIDU0LjI2MSwxOTIuODA4IDUzLjc2MSwxOTIuNTQgQyA0My41NjksMTg3LjA5NCA1My4yOTYsMTc4LjEyIDUyLjk2NiwxNzcuODA1IEMgNDUuMjMxLDE3MC40MjEgNTEuNDc2LDE2Mi4yOTYgNTUuMDY2LDE2Mi41ODkgTCA2Ni4yNzYsMTYyLjQ2MiIgc3R5bGU9ImZpbGw6dXJsKCNwYXRoMTQ1NDVfMV8pO3N0cm9rZTojYzMzO3N0cm9rZS13aWR0aDozLjAwOTcwMDA2IiBpZD0icGF0aDE0NTQ1Ii8+DQoJCQk8c3ZnOnBhdGggZD0iTSA2NS42LDEyLjU4NiBMIDY1LjU1NSwzMzUuMTczIE0gNjYuMjQ2LDE0Ny4xMDkgQyAxMDguODU3LDE0Ny4wMDkgMTEwLjI3MSwyMDguMDE2IDY1LjgyMywyMDcuNzU4IE0gNjYuMTU5LDE1OS4yNjMgQyA2Ny4xNywxNTkuNDA5IDgxLjM5MSwxNTkuMTY1IDgxLjM5MSwxNTkuMTY1IEwgODEuNjY4LDE5NS4xMDggTCA2NS43MDYsMTk1LjEwOCIgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2U6I2MzMztzdHJva2Utd2lkdGg6My4wMDk3MDAwNjtzdHJva2UtbGluZWNhcDpyb3VuZCIgaWQ9InBhdGgzOSIvPg0KCQkJDQoJCQkJPHN2ZzpwYXR0ZXJuIHBhdHRlcm5UcmFuc2Zvcm09Im1hdHJpeCgtMC4xNjUxIC0wLjAwMTMgLTAuMDAxMyAwLjE2NyAtODQ1MC4yNTk4IC02ODY3LjkzOSkiIHhsaW5rOmhyZWY9IiNwYXR0ZXJuMTU2MCIgaWQ9InBhdGgxNTQzM18xXyI+DQoJCQk8L3N2ZzpwYXR0ZXJuPg0KCQkJPHN2ZzpwYXRoIGQ9Ik0gNjc5Ljk3OCwxNTkuNjczIEMgNjc5Ljk3OCwxNTkuNjczIDY5Mi4yLDE1OS44ODQgNjkyLjY5NywxNjAuMTU0IEMgNzAyLjg0NywxNjUuNjc5IDY5My4wNTIsMTc0LjU3OCA2OTMuMzgxLDE3NC44OTUgQyA3MDEuMDYsMTgyLjMzOSA2OTQuNzUzLDE5MC40MTUgNjkxLjE2NiwxOTAuMDk0IEwgNjc5Ljk1NSwxOTAuMTM0IiBzdHlsZT0iZmlsbDp1cmwoI3BhdGgxNTQzM18xXyk7c3Ryb2tlOiNjMzM7c3Ryb2tlLXdpZHRoOjMuMDA5NzAwMDYiIGlkPSJwYXRoMTU0MzMiLz4NCgkJCTxzdmc6cGF0aCBkPSJNIDY3OS44NTcsMzM1Ljk0IEwgNjgwLjA0NCwxMS40NDcgTSA2NzkuODY4LDIwNS40ODggQyA2MzYuNTI3LDIwNS4yODYgNjM0LjY5OCwxNDQuOTUyIDY3OS45MywxNDQuODM4IE0gNjc5LjkyNywxOTMuNjg3IEMgNjczLjYzMiwxOTMuMjU1IDY2NC44MTQsMTkzLjMxNSA2NjQuODE0LDE5My4zMTUgTCA2NjQuNDU4LDE1Ny4zNjcgTCA2NzkuOTUxLDE1Ny40ODgiIHN0eWxlPSJmaWxsOm5vbmU7c3Ryb2tlOiNjMzM7c3Ryb2tlLXdpZHRoOjMuMDA5NzAwMDY7c3Ryb2tlLWxpbmVjYXA6cm91bmQiIGlkPSJwYXRoNDMiLz4NCgkJCTxzdmc6cGF0aCBkPSJNIDM4MS4yMTgsMTY5Ljk3OCBDIDM4MS4yMiwxNzEuNDEzIDM4MC40ODUsMTcyLjc0IDM3OS4yOSwxNzMuNDU4IEMgMzc4LjA5NSwxNzQuMTc2IDM3Ni42MjIsMTc0LjE3NiAzNzUuNDI3LDE3My40NTggQyAzNzQuMjMyLDE3Mi43MzkgMzczLjQ5NiwxNzEuNDEyIDM3My40OTgsMTY5Ljk3OCBDIDM3My40OTYsMTY4LjU0MiAzNzQuMjMxLDE2Ny4yMTUgMzc1LjQyNywxNjYuNDk4IEMgMzc2LjYyMiwxNjUuNzc5IDM3OC4wOTUsMTY1Ljc3OSAzNzkuMjksMTY2LjQ5OCBDIDM4MC40ODUsMTY3LjIxNSAzODEuMjIsMTY4LjU0MiAzODEuMjE4LDE2OS45NzggTCAzODEuMjE4LDE2OS45NzggeiAiIHN0eWxlPSJmaWxsOiM1NTY3YjAiIGlkPSJwYXRoMjk1MjkiLz4NCgkJCTxzdmc6cGF0aCBkPSJNIDMxNi4wNzcsMzQzLjkxNiBDIDMxNS42MzIsMzI2LjkzNCAzMjcuMjQ0LDMxMS4wOTQgMzQ2LjQzNCwzMDIuNTA1IEMgMzY1LjYyNSwyOTMuOTE2IDM4OS4zOTgsMjkzLjkyIDQwOC41ODQsMzAyLjUxNSBDIDQyNy43NywzMTEuMTEgNDM5LjM3NCwzMjYuOTUzIDQzOC45MiwzNDMuOTM1IiBzdHlsZT0iZmlsbDpub25lO3N0cm9rZTojYzMzO3N0cm9rZS13aWR0aDoyLjEzMDg5OTkxIiBpZD0icGF0aDY1NzgiLz4NCgkJPC9zdmc6Zz4NCgk8L3N2Zzpzdmc+"
    bg_image = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/Pgo8IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDIwMDEwOTA0Ly9FTiIKICJodHRwOi8vd3d3LnczLm9yZy9UUi8yMDAxL1JFQy1TVkctMjAwMTA5MDQvRFREL3N2ZzEwLmR0ZCI+CjxzdmcgdmVyc2lvbj0iMS4wIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiB3aWR0aD0iNjQyLjAwMDAwMHB0IiBoZWlnaHQ9IjMzNi4wMDAwMDBwdCIgdmlld0JveD0iMCAwIDY0Mi4wMDAwMDAgMzM2LjAwMDAwMCIKIHByZXNlcnZlQXNwZWN0UmF0aW89InhNaWRZTWlkIG1lZXQiPgo8bWV0YWRhdGE+CkNyZWF0ZWQgYnkgcG90cmFjZSAxLjE2LCB3cml0dGVuIGJ5IFBldGVyIFNlbGluZ2VyIDIwMDEtMjAxOQo8L21ldGFkYXRhPgo8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLjAwMDAwMCwzMzYuMDAwMDAwKSBzY2FsZSgwLjEwMDAwMCwtMC4xMDAwMDApIgpmaWxsPSIjMDAwMDAwIiBzdHJva2U9Im5vbmUiPgo8cGF0aCBkPSJNNjkwIDMzNDkgYy0xNTggLTQyIC0yMzQgLTgxIC0zNDEgLTE3MyAtOTggLTgzIC0xNzggLTE4OSAtMjM4IC0zMTcKLTk1IC0xOTkgLTk0IC0xOTEgLTg3IC03NDMgMyAtMjY1IDkgLTY3NCAxMiAtOTExIDIgLTIzNiAxMCAtNDU1IDE1IC00ODUgNjAKLTMxNyAyNjAgLTU3MCA1MjQgLTY2MyAxNTQgLTU1IDIxIC01MiAyNjUwIC01MiAyMzAxIDAgMjU4NSAyIDI1ODUgMTYgMCAzIDI0CjEzIDUzIDIzIDEyNyA0NSAyNjYgMTQ4IDM1OSAyNzAgNjggODggMTM5IDIzMiAxNzMgMzUxIGwyNSA5MCAtMiA5NTAgLTMgOTUwCi0yOSA4NSBjLTk1IDI4MyAtMjY4IDQ4MSAtNTAxIDU3NSAtMTE2IDQ3IC0xOCA0NSAtMjY2OCA0NCAtMTUwNyAwIC0yNTA2IC00Ci0yNTI3IC0xMHogbTUwNzkgLTM0IGM4IC00IDExIC0xOTYgMTEgLTYzMSBsMCAtNjI0IC0yOSAwIGMtODQgMCAtMjE4IC04MgotMjgwIC0xNzIgLTUwIC03MiAtNzAgLTE0MSAtNjYgLTIyMSA1IC03NyAyMCAtMTIxIDY5IC0xOTAgNjEgLTg3IDE5MyAtMTY2CjI3OSAtMTY3IGwyNyAwIDAgLTYyOSAwIC02MjkgLTI3IC03IGMtMTYgLTUgLTM2OSAtMTAgLTc4NSAtMTIgbC03NTggLTQgMAoxNjUwIDAgMTY1MSA2OTggMiBjNjU1IDMgODM2IC0xIDg2MSAtMTd6IG0tMzQ5OSAtMTYzNiBsMCAtMTY1MCAtNzU3IDQgYy01NjEKMyAtNzcwIDcgLTgwNSAxNiBsLTQ4IDEzIDAgNjI0IDAgNjI0IDI2IDAgYzkwIDAgMjIzIDgwIDI4NSAxNzEgOTQgMTM5IDkzCjI3NiAtNCA0MTIgLTY0IDg5IC0xOTMgMTY3IC0yNzggMTY3IGwtMjkgMCAwIDYyNSAwIDYyNSAyMyA0IGMxMiAzIDMxIDcgNDIgOQoxMSAzIDM2MyA1IDc4MyA2IGw3NjIgMSAwIC0xNjUxeiBtOTQwIDEwNzcgbDAgLTU3NCAtNTIgLTcgYy0zMzcgLTQ3IC01MjIKLTQwMSAtMzY4IC03MDUgMzcgLTc0IDEyNiAtMTY4IDE5MCAtMjAwIDY4IC0zNCAxNDkgLTYwIDE5MiAtNjAgbDM4IDAgMCAtNTkwCjAgLTU5MCAtNDU1IDAgLTQ1NSAwIDAgMTY1MCAwIDE2NTAgNDU1IDAgNDU1IDAgMCAtNTc0eiBtOTcwIC0xMDc2IGwwIC0xNjUwCi00NzAgMCAtNDcwIDAgMCA1OTAgMCA1OTAgMzMgMCBjODIgMCAyMTEgNjIgMjg3IDEzOSAxNTEgMTUyIDE4OCAzNjMgOTYgNTU2Ci02OSAxNDUgLTIwNSAyNDUgLTM2OCAyNjkgbC00OCA3IDAgNTc1IDAgNTc0IDQ3MCAwIDQ3MCAwIDAgLTE2NTB6IG0xNzkwCjE1NjIgYzY4IC0zOSAxODIgLTE0NCAyMzggLTIyMCA1NSAtNzQgOTMgLTE0NCAxMjggLTIzOCA1NSAtMTQ4IDU0IC0xMjIgNTQKLTExMDAgMCAtODcwIC0xIC05MDkgLTIwIC05ODIgLTU1IC0yMTMgLTE0NiAtMzY2IC0yOTcgLTQ5OCAtNjkgLTYwIC0xNjYKLTExNiAtMjQwIC0xMzggbC0yMyAtNyAwIDE2MjUgMCAxNjI2IDU4IC0yMiBjMzEgLTExIDc3IC0zMiAxMDIgLTQ2eiBtLTUzNDAKLTE1NTcgYzAgLTg4OCAtMSAtMTYxNSAtMyAtMTYxNSAtMTQgMCAtMTMwIDUyIC0xNjMgNzIgLTc1IDQ4IC0xNzEgMTM2IC0yMjIKMjA2IC03NiAxMDIgLTEzOSAyNTMgLTE2MSAzODcgLTkgNTIgLTIxIDkwNyAtMjUgMTY2MCAtMSAyMjggLTEgMjMxIDI4IDMxNQo5MSAyNzEgMjczIDQ4NCA0ODYgNTcxIDI1IDEwIDQ4IDE4IDUzIDE4IDQgMSA3IC03MjYgNyAtMTYxNHogbTI3MDQgNDU5IGMxNTkKLTQxIDI4MiAtMTYxIDMzMiAtMzIzIDIxIC02OSAxOSAtMjA0IC01IC0yNzMgLTM4IC0xMTEgLTExOCAtMjA3IC0yMjAgLTI2NAotNzYgLTQyIC0xNDQgLTU3IC0yNDUgLTUyIC04MCAzIC0xMDEgOCAtMTY5IDQxIC0xNzAgODAgLTI2OCAyMzUgLTI2OCA0MjIgMQozMDMgMjg0IDUyNCA1NzUgNDQ5eiBtLTI1ODQgLTExOCBjMTI3IC0zOCAyNDEgLTE2MyAyNjEgLTI4NSAxNCAtOTAgLTEgLTE1OQotNTMgLTIzOSAtNjEgLTkzIC0xODYgLTE3MiAtMjc1IC0xNzIgbC0yMyAwIDAgMzU1IDAgMzU1IDIzIDAgYzEyIDAgNDIgLTYgNjcKLTE0eiBtNTAzMCAtMzQxIGwwIC0zNTUgLTIyIDAgYy04MyAwIC0yMDcgNzQgLTI2NSAxNTcgLTUxIDczIC02NSAxMTcgLTY0CjIwMCAwIDgzIDE0IDEyMyA2NCAxOTUgNTYgODAgMTgyIDE1NSAyNjUgMTU3IGwyMiAxIDAgLTM1NXoiLz4KPHBhdGggZD0iTTUwODAgMzE2MyBjLTIzNCAtMjkgLTQyMCAtMjQwIC00MjAgLTQ3NyAwIC0xOTcgMTA1IC0zNjMgMjgxIC00NDYKMzIwIC0xNDkgNjg5IDg3IDY4OSA0NDIgMCA3OCAtMjcgMTc5IC02NSAyNDQgLTM2IDYyIC0xMTkgMTQzIC0xODEgMTc4IC04Mgo0NiAtMjEwIDcxIC0zMDQgNTl6IG0yMTYgLTQzIGMxODMgLTYzIDMxMyAtMjQ4IDMxNCAtNDQ1IDAgLTEwMyAtNTQgLTIzNQotMTMwIC0zMTQgLTk2IC0xMDAgLTE5NyAtMTQzIC0zMzUgLTE0MyAtMzkzIDAgLTYwNSA0NDcgLTM1NyA3NTggNjggODYgMTgyCjE1MCAyOTcgMTY3IDQ5IDcgMTU2IC01IDIxMSAtMjN6Ii8+CjxwYXRoIGQ9Ik01MDgwIDExOTkgYy0xOTAgLTI4IC0zMzkgLTE2MCAtMzk3IC0zNTMgLTIyIC03MiAtMTkgLTIwNyA2IC0yNzgKMTcgLTUwIDY3IC0xMzYgMTAzIC0xNzggMjIgLTI2IDEwMSAtODcgMTM3IC0xMDUgMjM5IC0xMjEgNTQ0IC0xOSA2NTggMjIwIDY4CjE0MyA2NyAyOTAgLTEgNDMwIC0zNyA3NCAtMTE1IDE2MCAtMTgyIDIwMiAtODcgNTIgLTIxOSA3OCAtMzI0IDYyeiBtMTk1IC0zMQpjMTY0IC00MSAzMDggLTIwNCAzMzUgLTM4MCAzMyAtMjE2IC05OSAtNDM3IC0zMDQgLTUwOCAtMzA0IC0xMDQgLTYxNiAxMTgKLTYxNiA0MzggMCAxNjAgNzUgMzAwIDIwNSAzODYgMTE3IDc4IDI0MSA5OSAzODAgNjR6Ii8+CjxwYXRoIGQ9Ik0xMjI1IDMxNDAgYy0xODMgLTMwIC0zMjIgLTE0OCAtMzg3IC0zMzAgLTI4IC03NyAtMjggLTIyMyAwIC0zMDIKNzQgLTIwNiAyNDggLTMzMSA0NjIgLTMzMSAxMzcgMCAyNDkgNDUgMzQwIDEzNyAxMDEgMTAzIDE0MyAyMDUgMTQzIDM0NiAtMQoxNDAgLTQyIDI0NCAtMTM4IDM0MSAtNTcgNTkgLTExNiA5NSAtMTkwIDEyMCAtNjYgMjIgLTE2NSAzMCAtMjMwIDE5eiBtMTQ1Ci0yMCBjMjI3IC0zNiAzOTEgLTIyOSAzOTEgLTQ2MCAwIC0xMzggLTQ1IC0yNDQgLTE0NSAtMzM4IC0xNzUgLTE2NiAtNDQ0Ci0xNjkgLTYyMyAtOCAtMTAzIDkzIC0xNTMgMjA2IC0xNTMgMzQ1IDAgMjU0IDE4OCA0NTEgNDUwIDQ3MCA4IDAgNDQgLTQgODAKLTl6Ii8+CjxwYXRoIGQ9Ik0xMjcwIDEyMDMgYy0xMzggLTE1IC0yOTAgLTExNyAtMzYyIC0yNDMgLTg1IC0xNDkgLTgzIC0zNDggNSAtNDk0CjM2IC01OSAxMjYgLTE0NSAxODEgLTE3MyAyODIgLTE0NCA2MTIgLTkgNzAzIDI4NyAyNCA3OSAyMSAyMTggLTYgMjk0IC03OAoyMTkgLTI5MiAzNTQgLTUyMSAzMjl6IG0xODUgLTM1IGMxNDAgLTM2IDI2NCAtMTU1IDMxNiAtMzA0IDI1IC03NCAyOCAtMTk2IDUKLTI3NCAtODIgLTI3OSAtMzkxIC00MTUgLTY1MSAtMjg2IC0xNjAgNzkgLTI1NSAyMzQgLTI1NSA0MTYgMCAzMDkgMjgzIDUyNgo1ODUgNDQ4eiIvPgo8L2c+Cjwvc3ZnPgo"
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
                'states': {'inactive': {'opacity': 1}},
                'dataLabels': {
                    'enabled': 0,
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

        'annotations': [{
            'shapes': [
                {'type': 'image', 'src': matchinfo_dic['home_team_logo'], 'width': img_width, 'height': img_width, 'point': {'x': home_x, 'y': home_y, 'xAxis': 0}},
                {'type': 'image', 'src': matchinfo_dic['visitor_team_logo'], 'width': img_width, 'height': img_width, 'point': {'x': visitor_x, 'y': visitor_y, 'xAxis': 0}},
            ],
        }],

        'xAxis': {
            'visible': 0,
            'labels': {'enabled': 1},
            'min': -30.5,
            'max': 30.5,
            'tickInterval': 1,
        },

        'yAxis': {
            'visible': 0,
            'gridLineWidth': 0,
            'title': {
                'text': '',
            },
            'labels': {'enabled': 1},
            'min': -15,
            'max': 15,
            'tickInterval': 1,
        },

        'series': [
            {'name': _('missed'), 'zIndex': 1, 'data': data_dic['home_team'][2], 'color': shot_missed_color, 'marker': {'lineColor': chart_color2, 'lineWidth': 1, 'symbol': 'diamond', 'radius': scatter_radius}},
            {'name': _('Shots on Goal'), 'color': shot_sog_color, 'zIndex': 2, 'data': data_dic['home_team'][1], 'marker': {'lineColor': '#2083df', 'lineWidth': 1, 'radius': scatter_radius, 'symbol': 'diamond'}},
            {'name': _('blocked'), 'zIndex': 3, 'color': shot_blocked_color, 'data': data_dic['home_team'][3], 'marker': {'symbol': 'diamond', 'radius': scatter_radius}},
            {'name': _('Post hit'), 'zIndex': 4, 'color': chart_color4, 'data': data_dic['home_team'][5], 'marker': {'symbol': 'diamond', 'radius': scatter_radius}},
            {'name': _('Goals'), 'zIndex': 7, 'color': '#ffffff', 'data': data_dic['home_team'][4], 'marker': {'lineColor': shot_goal_color, 'lineWidth': 5, 'symbol': 'circle', 'radius': scatter_radius-2}},
            {'name': _('missed'), 'zIndex': 1, 'data': data_dic['visitor_team'][2], 'color': shot_missed_color, 'marker': {'lineColor': chart_color2, 'lineWidth': 1, 'symbol': 'diamond', 'radius': scatter_radius}, 'showInLegend': 0},
            {'name': _('Shots on Goal'), 'color': shot_sog_color, 'zIndex': 2, 'data': data_dic['visitor_team'][1], 'marker': {'lineColor': '#2083df', 'lineWidth': 1, 'radius': scatter_radius, 'symbol': 'diamond'}, 'showInLegend': 0},
            {'name': _('blocked'), 'zIndex': 3, 'color': shot_blocked_color, 'data': data_dic['visitor_team'][3], 'marker': {'symbol': 'diamond', 'radius': scatter_radius}, 'showInLegend': 0, 'showInLegend': 0},
            {'name': _('Post hit'), 'zIndex': 4, 'color': chart_color4, 'data': data_dic['visitor_team'][5], 'marker': {'symbol': 'diamond', 'radius': scatter_radius}, 'showInLegend': 0},
            {'name': _('Goals'), 'zIndex': 7, 'color': '#ffffff', 'data': data_dic['visitor_team'][4], 'marker': {'lineColor': shot_goal_color, 'lineWidth': 5, 'symbol': 'circle', 'radius': scatter_radius-2}, 'showInLegend': 0},
            ],

        'responsive': {
            'rules': [{
                'condition': {'maxWidth': 500},
                'chartOptions': {
                    #'series': [
                    #    {'name': _('missed'), 'zIndex': 1, 'data': data_dic[2], 'color': shot_missed_color, 'marker': {'lineColor': chart_color2, 'lineWidth': 1, 'symbol': 'circle', 'radius': scatter_radius_responsive}},
                    #    {'name': _('Shots on Goal'), 'zIndex': 2, 'color': shot_sog_color, 'data': data_dic[1], 'marker': {'lineColor': '#2083df', 'lineWidth': 1, 'radius': scatter_radius_responsive, 'symbol': 'circle'}},
                    #    {'name': _('blocked'), 'zIndex': 3, 'color': shot_blocked_color, 'data': data_dic[3], 'marker': {'symbol': 'circle', 'radius': scatter_radius_responsive}},
                    #    {'name': _('Post hit'), 'zIndex': 4, 'color': chart_color4, 'data': data_dic[5], 'marker': {'symbol': 'circle', 'radius': scatter_radius_responsive}},
                    #    {'name': _('Goals'), 'zIndex': 5, 'color': shot_goal_color, 'data': data_dic[4], 'marker': {'symbol': 'circle', 'radius': scatter_radius_responsive}},
                    #],
                    'plotOptions':{'series': {'dataLabels': {'y': 10}}}
                    }
            }]
        }
    }
    return chart_options

