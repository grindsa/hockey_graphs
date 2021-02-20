# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
import math
from rest.functions.chartparameters import chartstyle, credit, exporting, title, subtitle, chart_color4, legend, font_size, variables_get, text_color, plotlines_color, responsive_y1

def shiftsperplayerchart_create(logger, ctitle, csubtitle, ismobile, shift_dic, goal_dic, matchinfo_dic, color_dic):
    # pylint: disable=E0602, R0914
    """ create shift per player chart """
    logger.debug('shiftsperplayerchart_create()')

    variable_dic = variables_get(ismobile)

    if ismobile:
        img_width = 15
    else:
        img_width = 23

    # length of a match (will be used as range-end of x list)
    tst_end = 3600

    # list to store playernames
    playername_list = ['<span><img src="{0}" width="{1}" height="{1}" alt="{2}"></img></span>'.format(matchinfo_dic['home_team_logo'], img_width, matchinfo_dic['home_team__shortcut'])]
    # list to store shifts
    data_list = [{'start': 0, 'end': tst_end, 'y': 0, 'color': plotlines_color}]

    # counter line-numbers and list storing number changes
    line_number = 1
    y_plotlines = []

    # counter for player in both teams
    player_cnt = 1

    # plotlines for period ends
    x2_plotlines_list = [
        {'color': plotlines_color, 'width': 2, 'value': 1200},
        {'color': plotlines_color, 'width': 2, 'value': 2400},
    ]

    for team in shift_dic:
        # set color for shifts
        if team == 'home_team':
            series_color = color_dic['home_team_color_primary']
        else:
            series_color = color_dic['visitor_team_color_secondary']

        for player_id in sorted(shift_dic[team], key=lambda i: (shift_dic[team][i]['line_number'], -shift_dic[team][i]['role'], shift_dic[team][i]['position'])):
            # add playername to x_list
            # tooltip_string = '{0} ({1})'.format(shift_dic[team][player_id]['name'], shift_dic[team][player_id]['jersey'])
            tooltip_string = shift_dic[team][player_id]['name']
            if ismobile:
                player_string = shift_dic[team][player_id]['surname']
            else:
                player_string = tooltip_string

            # add player-name to x_list
            playername_list.append(player_string)

            # add plotline in case the line-number changes
            if shift_dic[team][player_id]['line_number'] != line_number:
                line_number = shift_dic[team][player_id]['line_number']
                y_plotlines.append({'color': plotlines_color, 'width': 2, 'value': player_cnt - 0.5})

            for sh_idx, shift in enumerate(shift_dic[team][player_id]['shifts']):

                # detect overtime shifts adjust timestamp and add plotline for end of 3rd period
                if shift['start'] > tst_end or shift['end'] > tst_end:
                    tst_end = 3900
                    x2_plotlines_list.append({'color': plotlines_color, 'width': 2, 'value': 3600})
                    # we need to manipulate the first dataframe (headline for hometeam)
                    data_list[0]['end'] = tst_end

                # add index, count and playername to shift
                shift['y'] = player_cnt
                shift['cnt'] = player_cnt + 1
                shift['playername'] = tooltip_string
                shift['start_human'] = '{0:02d}:{1:02d}'.format(*divmod(shift['start'], 60))
                shift['end_human'] = '{0:02d}:{1:02d}'.format(*divmod(shift['end'], 60))

                shift['color'] = series_color
                data_list.append(shift)

            player_cnt += 1

        # add team separator
        if player_cnt <= 25:
            playername_list.append('<span><img src="{0}" width="{1}" height="{1}" alt="{2}"></img></span>'.format(matchinfo_dic['visitor_team_logo'], img_width, matchinfo_dic['visitor_team__shortcut']))
            data_list.append({'start': 0, 'end': tst_end, 'y': player_cnt, 'color': plotlines_color})
            player_cnt += 1

    x_list = []
    x2_list = []
    for second in range(0, tst_end + 1):
        x_list.append(math.ceil(second/60))
        x2_list.append(second)

    # show game timestamps in 5min interval
    xtickposition_list = []
    for second in range(0, tst_end +1, 300):
        xtickposition_list.append(second)

    # goals ticks on 2nd x-bar
    x2_tickposition_list = []

    for team in goal_dic:
        # color
        if team == 'home_team':
            team_plotlines_color = color_dic['home_team_color_primary']
            logo = matchinfo_dic['home_team_logo']
            alt =  matchinfo_dic['home_team__shortcut']
        else:
            team_plotlines_color = color_dic['visitor_team_color_secondary']
            logo = matchinfo_dic['visitor_team_logo']
            alt = matchinfo_dic['visitor_team__shortcut']

        for goal in goal_dic[team]:
            x2_plotlines_list.append({'color': team_plotlines_color, 'width': 1, 'value': goal['time']})
            x2_tickposition_list.append(goal['time'])
            x2_list[goal['time']] = '<span><img src="{0}" width="{1}" height="{1}" alt="{2}"></img></span>'.format(logo, img_width, alt)

    chart_options = {
        'ctype': 'gantt',
        'chart': {
            'height': '110%',
            'alignTicks': 0,
            'style': chartstyle()
        },
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': {'enabled': 0},
        'exporting': exporting(filename=ctitle),
        'responsive': responsive_y1(),
        'plotOptions': {'series': {'states': {'inactive': {'opacity': 1}}}},

        'tooltip': {
            'useHTML': 0,
            'headerFormat': '',
            'pointFormat': '<b>{point.playername}</b><br>#{point.cnt} - {point.type}: {point.start_human}m - {point.end_human}m',
            'followPointer': 1,
        },

        'xAxis': [{
            'title': title(_('Game Time'), variable_dic['font_size']),
            'labels': {'align': 'center', 'style': {'fontSize': variable_dic['font_size']}},
            'categories': x_list,
            'tickPositions': xtickposition_list,
            'tickWidth': 1,
            'grid': {'enabled': 0},
            'opposite': 0,
            },{
            'title': title(_('Goals'), variable_dic['font_size'], offset=15),
            'labels': {'useHTML': 1, 'align': 'center'},
            'categories': x2_list,
            'tickPositions': x2_tickposition_list,
            'plotLines': x2_plotlines_list,
            'tickWidth': 0,
            'grid': {'enabled': 0},
            'opposite': 1,
            }],

        'yAxis': {
            'title': title('', font_size),
            'categories': playername_list,
            'labels': {'useHTML': 1, 'align': 'right', 'style': {'fontSize': variable_dic['font_size']}},
            'grid': {'enabled': 0},
            'plotLines': y_plotlines
            },

        'series': [
            {'name': ('Even Strength'), 'data': data_list, 'color': '#404040', 'marker': {'symbol': 'square'}},
        ]
    }
    return chart_options
