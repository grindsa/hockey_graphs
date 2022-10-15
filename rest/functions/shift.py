# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Shift
from rest.functions.chartparameters import plotlines_color, variables_get, title
from rest.functions.helper import period_get, periodseconds_get

def shift_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('shift_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add shift
        obj, _created = Shift.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in shift_add(): {0}'.format(err_))
        result = None
    logger.debug('shift_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def shift_get(logger, fkey, fvalue, vlist=('match_id', 'shift')):
    """ get info for a specifc match_id """
    logger.debug('shift_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            shift_dic = list(Shift.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            shift_dic = Shift.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except BaseException:
        shift_dic = {}

    return shift_dic

def toifromshifts_get(logger, matchinfo_dic, shift_list, key='name'):
    """ get time on ice per player"""
    logger.debug('toifromshifts_get()')

    # inititialize dictionaries to store the data
    shift_dic = {'home_team': {1: {}, 2: {}, 3: {}, 4: {}}, 'visitor_team': {1: {}, 2: {}, 3: {}, 4: {}}}

    for shift in shift_list:
        if shift['team']['id'] == matchinfo_dic['home_team_id']:
            team_name = 'home_team'
        else:
            team_name = 'visitor_team'

        # get the shift data we need
        player_name = shift['player'][key]
        period = math.ceil(shift['endTime']['time']/1200)
        shift_duration = (shift['endTime']['time'] - shift['startTime']['time'])

        # create entry if does not exist and add sum
        if period not in shift_dic[team_name]:
            shift_dic[team_name][period] = {}

        if player_name not in shift_dic[team_name][period]:
            shift_dic[team_name][period][player_name] = 0

        shift_dic[team_name][period][player_name] += shift_duration

    return shift_dic

def _shifttype_get(_logger, team, start_time, end_time, penalty_dic):
    """ get type thype of a shift (pp, pk, normal) """
    # pylint: disable=E0602
    # logger.debug('_shifttype_get()')

    # home penalty during this shift
    # pylint: disable=R1703
    if start_time in penalty_dic['home_team'] or end_time in penalty_dic['home_team']:
        home_penalty = True
    else:
        home_penalty = False

    # visitor penalty during this shift
    if start_time in penalty_dic['visitor_team'] or end_time in penalty_dic['visitor_team']:
        visitor_penalty = True
    else:
        visitor_penalty = False

    # decide on PP/PK
    if home_penalty != visitor_penalty:
        if home_penalty:
            if team == 'home_team':
                shift_type = _('PK')
            else:
                shift_type = _('PP')
        else:
            if team == 'home_team':
                shift_type = _('PP')
            else:
                shift_type = _('PK')
    else:
        shift_type = _('Even Strength')

    return shift_type

def shiftsperplayer_get(logger, matchinfo_dic, shift_list, roster_list, penalty_dic):
    """  shifts per player """
    logger.debug('shiftsperplayer_get()')

    shift_dic = {'home_team': {}, 'visitor_team': {}}
    for shift in shift_list:

        # we need to differenciate between home and visitor team
        if shift['team']['id'] == matchinfo_dic['home_team_id']:
            team = 'home_team'
        else:
            team = 'visitor_team'

        # we need the type of the shift to set the right color in the chart
        shift_type = _shifttype_get(logger, team, shift['startTime']['time'], shift['endTime']['time'], penalty_dic)

        if shift['player']['id'] not in shift_dic[team]:
            shift_dic[team][shift['player']['id']] = {'shifts': [], 'name': shift['player']['name']}

        shift_dic[team][shift['player']['id']]['shifts'].append({'start': shift['startTime']['time'], 'end': shift['endTime']['time'], 'type': shift_type})

    #  add roster information
    for selector in roster_list:
        team = '{0}_team'.format(selector)
        for player in roster_list[selector]:
            if roster_list[selector][player]['position'] != 'GK':
                pid = roster_list[selector][player]['playerId']
                if pid in shift_dic[team]:
                    shift_dic[team][pid]['role'] = int(roster_list[selector][player]['roster'][0])
                    shift_dic[team][pid]['line_number'] = int(roster_list[selector][player]['roster'][1])
                    shift_dic[team][pid]['position'] = int(roster_list[selector][player]['roster'][2])
                    shift_dic[team][pid]['surname'] = roster_list[selector][player]['surname']
                    shift_dic[team][pid]['jersey'] = roster_list[selector][player]['jersey']


    # consistency check to cover cornercases where a player is not in roster list
    new_shift_dic = {}
    for team in shift_dic:
        new_shift_dic[team] = {}
        for player_id in shift_dic[team]:
            if 'line_number' in shift_dic[team][player_id]:
                new_shift_dic[team][player_id] = shift_dic[team][player_id]

    return new_shift_dic

def _datastructure_create(logger, period, tst_end, matchinfo_dic, img_width):
    """ create datastructure """
    logger.debug('_datastructure_create({0})'.format(period))

    # calculate seconds belong to a period
    (start_val, end_val) = periodseconds_get(logger, period, tst_end)

    result = {
        # player list contaimg playernames - first entry is the hometeam name
        'playername_list': ['<span><img src="{0}" width="{1}" height="{1}" alt="{2}"></img></span>'.format(matchinfo_dic['home_team_logo'], img_width, matchinfo_dic['home_team__shortcut'])],

        # list containing the shifts
        'shifts_list': [{'start': start_val, 'end': end_val, 'y': 0, 'color': plotlines_color}],

        # plotlines for period ends
        'x2_plotlines_list': [],

        # plotlines for y axis
        'y_plotlines_list': [],

        # list of x-values
        'x_list': [],
        'x2_list': [],

        # tick positions on xbars (5min interval and goals)
        'xtickposition_list': [],
        'x2_tickposition_list': []
    }

    if period == 5:
        result['x2_plotlines_list'].append({'color': plotlines_color, 'width': 2, 'value': 1200000})
        result['x2_plotlines_list'].append({'color': plotlines_color, 'width': 2, 'value': 2400000})

    return result

def shiftchartdata_get(logger, ismobile, shift_dic, goal_dic, matchinfo_dic, plotbands_list, color_dic):
    """  aggregate shiftdate to create chart input """
    logger.debug('shiftsperplayer_get()')

    if ismobile:
        img_width = 15
    else:
        img_width = 23


    # length of a match (will be used as range-end of x list)
    tst_end = 3600000

    # global data_dic
    data_dic = {5: {}, 1: {}, 2: {}, 3: {}}

    # create data_dic for output
    for period in data_dic:
        data_dic[period] = _datastructure_create(logger, period, tst_end, matchinfo_dic, img_width)

    # counter line-numbers and list storing number changes
    line_number = 1
    # counter for player in both teams
    player_cnt = 1

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

            # add player-name to x_list for 0 - subtree
            data_dic[5]['playername_list'].append(player_string)

            # add plotline in case the line-number changes
            if shift_dic[team][player_id]['line_number'] != line_number:
                line_number = shift_dic[team][player_id]['line_number']
                data_dic[5]['y_plotlines_list'].append({'color': plotlines_color, 'width': 2, 'value': player_cnt - 0.5})

            # enumerate shifts
            for _sh_idx, shift in enumerate(shift_dic[team][player_id]['shifts']):

                # get period of the shift
                shift_period = period_get(shift['end'], 'sec')
                if shift_period < 0:
                    # detect overtime shifts adjust timestamp and add plotline for end of 3rd period
                    if shift['start'] * 1000 > tst_end or shift['end'] * 1000 > tst_end:
                        tst_end = 3900000
                        data_dic[4] = _datastructure_create(logger, period, tst_end, matchinfo_dic, img_width)
                        for period in data_dic:
                            # add plotline after 3rd period
                            if period == 5:
                                data_dic[period]['x2_plotlines_list'].append({'color': plotlines_color, 'width': 2, 'value': 3600000})
                                # we need to manipulate the first dataframe (headline for hometeam)
                                data_dic[period]['shifts_list'][0]['end'] = tst_end
                            if period == 4:
                                # set x_scale for OT
                                data_dic[period]['shifts_list'][0]['start'] = 3600000
                                data_dic[period]['shifts_list'][0]['end'] = 3900000

                    # add index, count and playername to shift
                    shift['y'] = player_cnt
                    shift['cnt'] = player_cnt + 1
                    shift['playername'] = tooltip_string
                    shift['start'] = shift['start'] * 1000
                    shift['end'] = shift['end'] * 1000
                    shift['start_human'] = '{0:02d}:{1:02d}'.format(*divmod(shift['start'], 60))
                    shift['end_human'] = '{0:02d}:{1:02d}'.format(*divmod(shift['end'], 60))
                    shift['color'] = series_color

                    # add shifts to data_dic
                    data_dic[5]['shifts_list'].append(shift)
                    data_dic[shift_period]['shifts_list'].append(shift)

            # player change
            player_cnt += 1

        # add team separator
        if player_cnt <= 25:
            # empty line for visiting team
            data_dic[5]['playername_list'].append('<span><img src="{0}" width="{1}" height="{1}" alt="{2}"></img></span>'.format(matchinfo_dic['visitor_team_logo'], img_width, matchinfo_dic['visitor_team__shortcut']))
            # add pseudo shift for every period
            for period in data_dic:
                # calculate seconds belong to a period
                (start_val, end_val) = periodseconds_get(logger, period, tst_end)
                # add pseudoshift bcs of team change
                data_dic[period]['shifts_list'].append({'start': start_val, 'end': end_val, 'y': player_cnt, 'color': plotlines_color})

            player_cnt += 1

    # fill x_lists
    for period in data_dic:

        # add plotband containing penalty
        data_dic[period]['plotbands_list'] = plotbands_list

        # calculate seconds belong to a period
        (start_val, end_val) = periodseconds_get(logger, period, tst_end)

        # add 5min ticks to 1st xbar
        for second in range(start_val, end_val +1, 300):
            data_dic[period]['xtickposition_list'].append(second)

    for team in goal_dic:
        # color
        if team == 'home_team':
            team_plotlines_color = color_dic['home_team_color_primary']
            logo = matchinfo_dic['home_team_logo']
            alt = matchinfo_dic['home_team__shortcut']
        else:
            team_plotlines_color = color_dic['visitor_team_color_secondary']
            logo = matchinfo_dic['visitor_team_logo']
            alt = matchinfo_dic['visitor_team__shortcut']

        for goal in goal_dic[team]:
            # get period of the shift
            goal_period = period_get(goal['time'], 'sec')

            for ele in (5, goal_period):
                # add goal in overall tree an into period subtree
                data_dic[ele]['x2_plotlines_list'].append({'color': team_plotlines_color, 'width': 2, 'value': goal['time'] * 1000, 'zIndex': 5, 'dashStyle': 'Dash', 'label': {'text': '<span><img src="{0}" width="{1}" height="{1}" alt="{2}"></img></span>'.format(logo, img_width, alt), 'align': 'center', 'verticalAlign': 'top', 'textAlign': 'center', 'useHTML': 1, 'rotation': 360, 'x': -1, 'y': -13}})
    return data_dic

def _goalposition_get(period, timestamp):
    """ get postion of goals in dictionary """
    if period == 5:
        position = timestamp
    else:
        position = timestamp - ((period-1) * 1200)

    return position

def shiftsupdates_get(logger, subtitle, ismobile, chart_data):
    """ get updates for shiftchart """
    logger.debug('shiftsupdates_get()')
    # pylint: disable=E0602
    variable_dic = variables_get(ismobile)

    # this is a dictionary containing period names
    periodname_dic = {1: '1st', 2: '2nd', 3: '3rd', 4: 'OT', 5: 'Full Game'}

    updates_dic = {}
    for period in chart_data:
        # create structure to store the updates
        updates_dic[period] = {'name': periodname_dic[period], 'data': {}}
        # update chart-title
        updates_dic[period]['data']['subtitle'] = {'text': '{0} - {1}'.format(subtitle, periodname_dic[period])}

        # update series
        updates_dic[period]['data']['series'] = [{'name': ('Even Strength'), 'data': chart_data[period]['shifts_list'], 'color': '#404040', 'marker': {'symbol': 'square'}}]

        updates_dic[period]['data']['xAxis'] = [{
            'title': title(_('Game Time'), variable_dic['font_size']),
            'labels': {'align': 'center', 'style': {'fontSize': variable_dic['font_size']}},
            #'categories': chart_data[period]['x_list'],
            'type': 'datetime',
            'tickInterval': 300000,
            #'tickPositions': chart_data[period]['xtickposition_list'],
            'tickWidth': 1,
            'grid': {'enabled': 0},
            'opposite': 0,
        }, {
            'title': title(_('Goals'), variable_dic['font_size'], offset=15),
            'labels': {'useHTML': 1, 'align': 'center'},
            'tickPositions': [],
            'plotLines': chart_data[period]['x2_plotlines_list'],
            'plotBands': chart_data[period]['plotbands_list'],
            'tickWidth': 0,
            'grid': {'enabled': 0},
            'opposite': 1,
        }]

    # default checked value in chart
    updates_dic[5]['checked'] = True

    return updates_dic
