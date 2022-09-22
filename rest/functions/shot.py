# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import math
from scipy.signal import savgol_filter
import django
django.setup()
from shapely.geometry import Point
from rest.models import Shot
from rest.functions.helper import maxval_get, list_sumup, period_get, sliding_window, date_to_uts_utc, deviation_avg_get
from rest.functions.chartparameters import chart_color2, chart_color3, title
import functions.rink_dimensions as rd

def _shoot_coordinates_convert(logger, coordinate_x, coordinate_y, new_format=False, shotmap=False):
    """ convert  arbitrary coordinates to actual coordinates in meters sourse: leaffan.net """

    if new_format:
        x_total = 61/2   # field length
        y_total = 30/2 # field width
        x_factor = 60 # assumed max on x
        y_factor = 50 # asusmed max on y
        meter_x = coordinate_x * x_total/x_factor
        meter_y = coordinate_y * y_total/y_factor
    else:
        try:
            if shotmap:
                x2m = 0.26
            else:
                x2m = 0.3048
            y2m = 0.1524
            meter_x = x2m * int(coordinate_x)
            meter_y = y2m * int(coordinate_y)
        except BaseException as err_:
            logger.critical('error in _shoot_coordinates_convert(): {0}'.format(err_))
            meter_x = 0
            meter_y = 0

    return(round(meter_x, 2), round(meter_y, 2))

def shot_list_get(logger, fkey=None, fvalue=None, vlist=('shot_id', 'match_shot_resutl_id', 'player_id', 'zone', 'timestamp')):
    """ query shot(s) from database based with optional filtering """
    try:
        if fkey:
            if len(vlist) == 1:
                shot_list = Shot.objects.filter(**{fkey: fvalue}).order_by('shot_id').values_list(vlist[0], flat=True)
            else:
                shot_list = Shot.objects.filter(**{fkey: fvalue}).order_by('shot_id').values(*vlist)
        else:
            if len(vlist) == 1:
                shot_list = Shot.objects.all().order_by('shot_id').values_list(vlist[0], flat=True)
            else:
                shot_list = Shot.objects.all().order_by('shot_id').values(*vlist)
    except BaseException as err_:
        logger.critical('error in shot_list_get(): {0}'.format(err_))
        shot_list = []

    return list(shot_list)

def shot_list_perplayer_get(logger, player_id=None, match_list=None, vlist=('shot_id', 'match_shot_resutl_id', 'player_id', 'zone', 'timestamp')):
    """ query shot(s) oer player per season with optional filtering """
    try:
        if match_list:
            if len(vlist) == 1:
                shot_list = Shot.objects.filter(player_id=player_id, match__in=match_list).order_by('shot_id').values_list(vlist[0], flat=True)
            else:
                shot_list = Shot.objects.filter(player_id=player_id, match__in=match_list).order_by('shot_id').values(*vlist)
        else:
            if len(vlist) == 1:
                shot_list = Shot.objects.filter(player_id=player_id).order_by('shot_id').values_list(vlist[0], flat=True)
            else:
                shot_list = Shot.objects.filter(player_id=player_id).order_by('shot_id').values(*vlist)
    except BaseException as err_:
        logger.critical('shot_list_perplayer_get(): {0}'.format(err_))
        shot_list = []

    return list(shot_list)

def shot_delete(logger, fkey, fvalue):
    """ add team to database """
    logger.debug('shot_add({0}:{1})'.format(fkey, fvalue))
    try:
        # delete shots for a certain filter
        Shot.objects.filter(**{fkey: fvalue}).delete()
    except BaseException as err_:
        logger.critical('error in shot_add(): {0}'.format(err_))

    logger.debug('shot_delete({0}:{1}) ended'.format(fkey, fvalue))

def shot_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('shot_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add authorization
        obj, _created = Shot.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.shot_id
    except BaseException as err_:
        logger.critical('error in shot_add(): {0}'.format(err_))
        result = None

    logger.debug('shot_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def shotside_get(shot_, home_id_, visitor_id_):
    """ guess side of the shot (left/right) """

    coordinate_y_ = shot_['coordinate_y']
    team_id = shot_['team_id']
    if team_id == home_id_:
        team_ = 'home'
        if coordinate_y_ < 0:
            side_ = 'right'
        else:
            side_ = 'left'
    elif team_id == visitor_id_:
        team_ = 'visitor'
        if coordinate_y_ < 0:
            side_ = 'left'
        else:
            side_ = 'right'
    else:
        team_ = None
        side_ = None

    return (team_, side_)

def zone_name_get(logger, coordinate_x, coordinate_y):
    """ get coordinates """
    (meter_x, meter_y) = _shoot_coordinates_convert(logger, coordinate_x, coordinate_y)
    # constructing shot location
    shot_pnt = Point(meter_x, meter_y)
    shot_zone = None
    # determining shot zone
    for poly_name, poly in rd.polygons:
        if poly.intersects(shot_pnt):
            shot_zone = poly_name[5:]
            break

    return shot_zone.lower()

def shot_dic_prep(logger, group_by=False, x_max=61):
    """ prepare shot stats """
    logger.debug('shot_dic_prep()')

    # list of zones
    zone_list = ('slot', 'left', 'right', 'blue_line', 'neutral_zone', 'behind_goal')

    # initialize dicionaries
    shot_min_dic = {'home_team': {}, 'visitor_team': {}}

    # initialize the different minutes)
    if group_by == 'match_shot_resutl_id':
        for ele in range(1, 6):
            shot_min_dic['home_team'][ele] = {}
            shot_min_dic['visitor_team'][ele] = {}

    for min_ in range(0, x_max):
        if group_by == 'match_shot_resutl_id':
            for ele in range(1, 6):
                shot_min_dic['home_team'][ele][min_] = 0
                shot_min_dic['visitor_team'][ele][min_] = 0
        elif group_by == 'zone':
            for zone  in zone_list:
                shot_min_dic['home_team'][zone] = {}
                shot_min_dic['visitor_team'][zone] = {}
                for period in (1, 2, 3, 4):
                    shot_min_dic['home_team'][zone][period] = 0
                    shot_min_dic['visitor_team'][zone][period] = 0
        else:
            shot_min_dic['home_team'][min_] = 0
            shot_min_dic['visitor_team'][min_] = 0

    return shot_min_dic

def shotstatus_count(logger, shot_list, matchinfo_dic):
    """ count shots per minutes """
    logger.debug('shotstatus_count()')

    # we need an x_max value for the chart and try to get it from shot_list
    x_max = maxval_get(shot_list, 'timestamp', 60, 1)

    # create empty structure of shots per team per minute
    shot_status_dic = shot_dic_prep(logger, 'match_shot_resutl_id', x_max)
    goal_dic = {'home_team': {}, 'visitor_team': {}}

    ot_reg = None
    for shot in shot_list:
        # get min out of seconds
        min_ = math.ceil(shot['timestamp']/60)

        # we need additional value in  x-bar if we go for overtime
        if min_ > 60 and ot_reg is None:
            # now we registered OT
            ot_reg = True
            for val in range(61, 66):
                for ele in range(1, 6):
                    shot_status_dic['home_team'][ele][val] = 0
                    shot_status_dic['visitor_team'][ele][val] = 0

        # we need to differenciate between home and visitor team
        if shot['team_id'] == matchinfo_dic['home_team_id']:
            team = 'home_team'
        else:
            team = 'visitor_team'

        # count shots
        shot_status_dic[team][shot['match_shot_resutl_id']][min_] += 1
        if shot['match_shot_resutl_id'] == 4:
            goal_dic[team][min_] = shot['player__last_name']

    return(shot_status_dic, goal_dic)

def shotspermin_count(logger, shot_list, matchinfo_dic):
    """ count shots per minutes """
    logger.debug('shotspermin_count()')

    # we need an x_max value for the chart and try to get it from shot_list
    x_max = maxval_get(shot_list, 'timestamp', 60, 1)

    # create empty structure of shots per team per minute
    # we are doing it upfront to cover scenarios with no shots per min
    shot_min_dic = shot_dic_prep(logger, 'min', x_max)
    goal_dic = {'home_team': {}, 'visitor_team': {}}

    ot_reg = None
    for shot in shot_list:
        # get min out of seconds
        min_ = math.ceil(shot['timestamp']/60)

        # we need additional value in  x-bar if we go for overtime
        if min_ > 60 and ot_reg is None:
            # now we registered OT
            ot_reg = True
            for val in range(61, 66):
                shot_min_dic['home_team'][val] = 0
                shot_min_dic['visitor_team'][val] = 0

        # we need to differenciate between home and visitor team
        if shot['team_id'] == matchinfo_dic['home_team_id']:
            team = 'home_team'
        else:
            team = 'visitor_team'

        # count shots and goals
        shot_min_dic[team][min_] += 1
        if shot['match_shot_resutl_id'] == 4:
            goal_dic[team][min_] = shot['player__last_name']

    return (shot_min_dic, goal_dic)

def shotpersecondlist_get(logger, matchinfo_dic, shot_list):
    """ count shots per second """
    logger.debug('shotpersecondlist_get()')

    shot_sec_dic = {'home_team': [], 'visitor_team': []}
    for shot in shot_list:
        # timestamp of shot
        sec_ = shot['timestamp']
        # we need to differenciate between home and visitor team
        if shot['team_id'] == matchinfo_dic['home_team_id']:
            team = 'home_team'
        else:
            team = 'visitor_team'

        shot_sec_dic[team].append(sec_)

    return shot_sec_dic

def shotspersec_count(logger, shot_list, matchinfo_dic):
    """ count shots per second """
    logger.debug('shotspermin_count()')

    # we need an x_max value for the chart and try to get it from shot_list
    x_max = maxval_get(shot_list, 'timestamp', 1, 1)

    shot_sec_dic = {'home_team': {}, 'visitor_team': {}}
    goal_dic = {'home_team': {}, 'visitor_team': {}}

    for shot in shot_list:

        # timestamp of shot
        sec_ = shot['timestamp']
        # get min out of seconds
        min_ = math.ceil(shot['timestamp']/60)

        # we need to differenciate between home and visitor team
        if shot['team_id'] == matchinfo_dic['home_team_id']:
            team = 'home_team'
        else:
            team = 'visitor_team'

        # count shots and goals but skip shots during the first second
        if sec_ != 0:
            shot_sec_dic[team][sec_] = 1

        if shot['match_shot_resutl_id'] == 4:
            goal_dic[team][min_] = shot['player__last_name']

    return (shot_sec_dic, goal_dic)

def shotspermin_combine(logger, shot_min_dic):
    """ sum up shots per minute """
    logger.debug('shotspermin_aggregate()')

    shotsum_dic = {}
    for team in shot_min_dic:
        for min_ in shot_min_dic[team]:
            if min_ not in shotsum_dic:
                shotsum_dic[min_] = 0
            shotsum_dic[min_] += shot_min_dic[team][min_]

    return shotsum_dic

def shotspermin_aggregate(logger, shot_min_dic):
    """ sum up shots per minute """
    logger.debug('shotspermin_aggregate()')

    # create empty dict
    shot_sum_dic = {}

    for key in shot_min_dic:
        # create subkey
        shot_sum_dic[key] = {}
        _value_list = list(shot_min_dic[key].values())

        for subkey in shot_min_dic[key]:
            shot_sum_dic[key][subkey] = sum(_value_list[:subkey])

    return shot_sum_dic

def shotstatus_aggregate(logger, shot_status_dic):
    """ sum up shots per minute """
    logger.debug('shotspermin_aggregate()')

    # aggregate shots per min
    shotsum_dic = {'home_team': {1:{}, 2:{}, 3:{}, 4:{}, 5:{}}, 'visitor_team': {1:{}, 2:{}, 3:{}, 4:{}, 5:{}}}
    for ele in range(1, 6):
        home_min_values = list(shot_status_dic['home_team'][ele].values())
        visitor_min_values = list(shot_status_dic['visitor_team'][ele].values())
        for min_ in shot_status_dic['home_team'][ele]:
            shotsum_dic['home_team'][ele][min_] = sum(home_min_values[:min_])
        for min_ in shot_status_dic['visitor_team'][ele]:
            shotsum_dic['visitor_team'][ele][min_] = sum(visitor_min_values[:min_])

    return shotsum_dic

def _period_split(_logger, shotflow_dic):
    # logger.debug('periods_split()')
    gameflow_dic = {'home_team': {}, 'visitor_team': {}}

    for team in shotflow_dic:
        for min_, value in shotflow_dic[team].items():
            # get period
            period = period_get(min_)
            # we need to separate the data by period
            if period not in gameflow_dic[team]:
                gameflow_dic[team][period] = {}
            # period beginning copy the first value at the beginning
            if min_ in (21, 41, 61):
                gameflow_dic[team][period][int(min_-1)] = value
            gameflow_dic[team][period][int(min_)] = value

    return gameflow_dic

def _p60_calculate(logger, shotperiod_dic, wsize=3):
    """ sum up shots per seconds """
    logger.debug('p60_calculate()')

    # this is the final flow dic
    shot_flow_dic = {}

    for team in ['home_team', 'visitor_team']:
        shot_flow_dic[team] = {}
        for period in shotperiod_dic[team]:
            shot_flow_dic[team][period] = {}
            minutes_list = list(shotperiod_dic[team][period].keys())
            # get list of minutes for sliding window per iteration
            (bw_min_list, _fw_min_list) = sliding_window(logger, minutes_list, wsize)

            # go over the list and calculate the 60 values based on windows size
            for min_list in bw_min_list:
                # the minute is the last element in list
                min_ = min_list[len(min_list)-1]

                tmp_shotcount = 0
                for _min in min_list:
                    tmp_shotcount = tmp_shotcount + shotperiod_dic[team][period][_min]

                shot_flow_dic[team][period][min_] = round(tmp_shotcount * 60/len(min_list), 0)

            # hack 0 values at the beginning of a period
            for min_ in shot_flow_dic[team][period]:
                # we need to set a value to avoid negative values during smoothing
                if shot_flow_dic[team][period][min_] == 0:
                    shot_flow_dic[team][period][min_] = 20

    return shot_flow_dic

def _gameflow_dic_smooth(logger, gameflow_dic, wsize=9, porder=3):
    """ sum up shots per seconds """
    logger.debug('_gameflow_dict_smooth({0}:{1})'.format(wsize, porder))

    # this is the smoothing part: we smooth across all values of a single period by using a Savitzky-Golay filter
    for team in ['home_team', 'visitor_team']:
        for period in gameflow_dic[team]:
            x_list = list(gameflow_dic[team][period].keys())
            if len(x_list) >= 9:
                y_list = savgol_filter(list(gameflow_dic[team][period].values()), 9, 3) # window size 9, polynomial order 3
                for idx, ele in enumerate(x_list):
                    gameflow_dic[team][period][int(ele)] = round(y_list[idx], 0)

    return gameflow_dic

def gameflow_get(logger, shotmin_dic):
    """ sum up shots per seconds """
    logger.debug('gameflow_get()')

    # split minute dic into periods and fix 0-values at the beginning of a period
    shotperiod_dic = _period_split(logger, shotmin_dic)

    # calculate 60 values with a sliding window - slideing window is one minute longer than specificied below
    gameflow_dic = _p60_calculate(logger, shotperiod_dic, wsize=4)

    # smooth dictionary by using a Savitzky-Golay filter with a windows size of 9 and an polynomical order of 3
    gameflow_dic = _gameflow_dic_smooth(logger, gameflow_dic, wsize=9, porder=3)

    return gameflow_dic

def shotsperzone_count(logger, shot_list, matchinfo_dic):
    """ shots per zone """
    logger.debug('shotsperzone_count()')

    # we need an x_max value for the chart and try to get it from shot_list
    x_max = maxval_get(shot_list, 'timestamp', 60, 1)

    # create empty structure of shots per zone per period
    shot_zone_dic = shot_dic_prep(logger, 'zone', x_max)

    for shot in shot_list:

        # get min out of seconds
        min_ = math.ceil(shot['timestamp']/60)
        # cornercase handling and period
        if min_ == 0:
            min_ = 1
        period = math.ceil(min_/20)

        # we need to differenciate between home and visitor team
        if shot['team_id'] == matchinfo_dic['home_team_id']:
            team = 'home_team'
        else:
            team = 'visitor_team'

        # cover situations in playoff with 2 or more OT
        if period not in shot_zone_dic[team][shot['zone']]:
            shot_zone_dic[team][shot['zone']][period] = 0

        #  count shots per zone per period
        shot_zone_dic[team][shot['zone']][period] += 1

    return shot_zone_dic

def shotsperzone_aggregate(logger, shotzone_dic, match_info_dic):
    """ reformat zone statistics for template processing """
    logger.debug('shotsperzone_aggregate()')
    shotzonesum_dic = {'home_team': {'logo': match_info_dic['home_team_logo']}, 'visitor_team': {'logo': match_info_dic['visitor_team_logo']}}

    # aggregate shots per zone
    for team in shotzone_dic:
        for zname in shotzone_dic[team]:
            if 'sum' not in shotzonesum_dic[team]:
                shotzonesum_dic[team]['sum'] = {}
                shotzonesum_dic[team]['sum']['count'] = 0
            if zname not in shotzonesum_dic[team]:
                shotzonesum_dic[team][zname] = {}
                shotzonesum_dic[team][zname]['count'] = 0
            for period in shotzone_dic[team][zname]:
                shotzonesum_dic[team][zname]['count'] += shotzone_dic[team][zname][period]
                shotzonesum_dic[team]['sum']['count'] += shotzone_dic[team][zname][period]

    # add percentage
    for team in shotzonesum_dic:
        for zone in shotzonesum_dic[team]:
            if zone != 'logo':
                if shotzonesum_dic[team]['sum']['count'] > 0:
                    shotzonesum_dic[team][zone]['roundpercent'] = round(shotzonesum_dic[team][zone]['count'] / shotzonesum_dic[team]['sum']['count'] * 100)
                else:
                    shotzonesum_dic[team][zone]['roundpercent'] = 0

    return shotzonesum_dic

def shot_dic_convert(logger, shot_dic, match_info_dic):
    """ convert shot coordinates for a list of matches and resturn them as both has and list """
    logger.debug('shot_dic_convert()')
    converted_shot_list = []
    converted_shot_dic = {}

    for match_id in shot_dic:
        shotmap_dic = shotcoordinates_get(logger, shot_dic[match_id], match_info_dic[match_id])
        if shotmap_dic['home_team']:
            converted_shot_dic[match_id] = shotmap_dic['home_team']
            converted_shot_list.extend(shotmap_dic['home_team'])
        else:
            converted_shot_dic[match_id] = shotmap_dic['visitor_team']
            converted_shot_list.extend(shotmap_dic['visitor_team'])

    logger.debug('shot_dic_convert() ended')
    return(converted_shot_list, converted_shot_dic)

def shotcoordinates_get(logger, shot_list, matchinfo_dic):
    """ get shootcoordindates """
    logger.debug('shotcoordinates_get()')
    shotmap_dic = {'home_team': [], 'visitor_team': []}

    shot_values_new_format = xml_check(logger, shot_list)

    for shot in shot_list:

        (m_x, m_y) = _shoot_coordinates_convert(logger, shot['coordinate_x'], shot['coordinate_y'], shot_values_new_format, shotmap=True)

        shot['meters_x'] = m_x
        shot['meters_y'] = m_y
        shot['minute'] = math.ceil(shot['timestamp']/60)

        if shot['team_id'] == matchinfo_dic['home_team_id']:
            team = 'home_team'
            # flip counter clockwise for home_game
            #shot['x'] = shot['coordinate_y'] * -1
            #shot['y'] = shot['coordinate_x']
        else:
            team = 'visitor_team'
            # flip clockwise for road_game
            #shot['x'] = shot['coordinate_y']
            #shot['y'] = shot['coordinate_x'] * -1

        shot['name'] = '{0} {1}'.format(shot['player__first_name'], shot['player__last_name'])

        # append to list
        shotmap_dic[team].append(shot)

    return shotmap_dic

def rebound_breaks_get(logger, shot_list, matchinfo_dic):
    """ detect and count rebounds """
    logger.debug('shotcoordinates_get()')

    # within this interval two shots from same team will be assumed as rebound
    reboud_interval = 3
    # within this interval two shots form different team will be assumed as break
    break_interval = 7

    data_dic = {'home': {'rebounds': 0, 'rebound_goals': 0, 'breaks': 0, 'break_goals': 0}, 'visitor': {'rebounds': 0, 'rebound_goals': 0, 'breaks': 0, 'break_goals': 0}}

    prev_team = None
    prev_time = 0
    for idx, shot in enumerate(shot_list):

       # time difference to previous shot
        shot_diff = abs(shot['timestamp'] - prev_time)

        # we need to differenciate between home and visitor team
        if shot['team_id'] == matchinfo_dic['home_team_id']:
            team = 'home'
        else:
            team = 'visitor'

        # rebound detection
        if shot['team_id'] == prev_team and shot_diff <= reboud_interval and idx != 0:
            # print('rebound', team)
            data_dic[team]['rebounds'] += 1
            if shot['match_shot_resutl_id'] == 4:
                data_dic[team]['rebound_goals'] += 1

        # break detection
        if shot['team_id'] != prev_team and shot_diff <= break_interval and idx != 0:
            # print('break', team)
            data_dic[team]['breaks'] += 1
            if shot['match_shot_resutl_id'] == 4:
                data_dic[team]['break_goals'] += 1

        # store term and timestamp for comparison in next interation
        prev_team = shot['team_id']
        prev_time = shot['timestamp']

    return data_dic

def _rebound_sumup(logger, teamstat_dic):
    """ sum up faceoff statistics """
    logger.debug('_faceoff_sumup()')

    update_amount = 0
    teamstat_sum_dic = {}

    for team_id in teamstat_dic:
        # sumup data per team
        teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'rebounds_for', 'rebounds_against', 'goals_rebound_for', 'goals_rebound_against'])
        # check how many items we have to create in update_dic
        if update_amount < len(teamstat_sum_dic[team_id]):
            update_amount = len(teamstat_sum_dic[team_id])

    return (teamstat_sum_dic, update_amount)

def rebound_overview_get(logger, ismobile, teamstat_dic, teams_dic):
    """ collect data for rebound overview chart """
    logger.debug('rebound_overview_get()')

    if ismobile:
        img_width = 20
        img_height = 20
    else:
        img_width = 30
        img_height = 30

    # get summary
    (reboundsum_dic, update_amount) = _rebound_sumup(logger, teamstat_dic)

    # build temporary dictionary for date. we build the final sorted in next step
    rebound_lake = {}
    for ele in range(1, update_amount+1):
        rebound_lake[ele] = []

    for team_id in reboundsum_dic:
        # harmonize lengh by adding list elements at the beginning
        if len(reboundsum_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(reboundsum_dic[team_id])):
                reboundsum_dic[team_id].insert(0, reboundsum_dic[team_id][0])

        for idx, ele in enumerate(reboundsum_dic[team_id], 1):

            if ele['sum_rebounds_for']:
                goals_rebound_for_pctg = round(ele['sum_goals_rebound_for'] * 100 / ele['sum_rebounds_for'], 2)
            else:
                goals_rebound_for_pctg = 0.00
            if ele['sum_rebounds_against']:
                goals_rebound_against_pctg = round(ele['sum_goals_rebound_against'] * 100 / ele['sum_rebounds_against'], 2)
            else:
                goals_rebound_against_pctg = 0.00

            rebound_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'name': '<span><img src="{0}" alt="{1}" width="{2}" height="{3}"></span>'.format(teams_dic[team_id]['team_logo'], teams_dic[team_id]['shortcut'], img_width, img_height),
                'rebounds_for': ele['sum_rebounds_for'],
                'rebounds_against': ele['sum_rebounds_against'],
                'goals_rebound_for': ele['sum_goals_rebound_for'],
                'goals_rebound_against': ele['sum_goals_rebound_against'],
                'goals_rebound_for_pctg':  goals_rebound_for_pctg,
                'goals_rebound_against_pctg':  goals_rebound_against_pctg
            })

    # build final dictionary
    rebound_chartseries_dic = _rebound_chartseries_get(logger, rebound_lake)

    return rebound_chartseries_dic

def _rebound_chartseries_get(logger, data_dic):
    """ build structure for chart series """
    logger.debug('_rebound_chartseries_get()')
    chartseries_dic = {}
    for ele in data_dic:
        chartseries_dic[ele] = {'x_category': [], 'goals_rebound_for_pctg': [], 'goals_rebound_against_pctg': []}
        for datapoint in sorted(data_dic[ele], key=lambda i: i['goals_rebound_for_pctg'], reverse=True):
            chartseries_dic[ele]['x_category'].append(datapoint['name'])
            chartseries_dic[ele]['goals_rebound_for_pctg'].append(datapoint['goals_rebound_for_pctg'])
            chartseries_dic[ele]['goals_rebound_against_pctg'].append(datapoint['goals_rebound_against_pctg'])

    return chartseries_dic

def break_overview_get(logger, ismobile, teamstat_dic, teams_dic):
    """ collect data for break overview chart """
    logger.debug('break_overview_get()')

    if ismobile:
        img_width = 20
        img_height = 20
    else:
        img_width = 30
        img_height = 30

    # get summary
    (breaksum_dic, update_amount) = _break_sumup(logger, teamstat_dic)

    # build temporary dictionary for date. we build the final sorted in next step
    break_lake = {}
    for ele in range(1, update_amount+1):
        break_lake[ele] = []

    for team_id in breaksum_dic:
        # harmonize lengh by adding list elements at the beginning
        if len(breaksum_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(breaksum_dic[team_id])):
                breaksum_dic[team_id].insert(0, breaksum_dic[team_id][0])

        for idx, ele in enumerate(breaksum_dic[team_id], 1):

            if ele['sum_breaks_for']:
                goals_break_for_pctg = round(ele['sum_goals_break_for'] * 100 / ele['sum_breaks_for'], 2)
            else:
                goals_break_for_pctg = 0.00
            if ele['sum_breaks_against']:
                goals_break_against_pctg = round(ele['sum_goals_break_against'] * 100 / ele['sum_breaks_against'], 2)
            else:
                goals_break_against_pctg = 0.00

            break_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'name': '<span><img src="{0}" alt="{1}" width="{2}" height="{3}"></span>'.format(teams_dic[team_id]['team_logo'], teams_dic[team_id]['shortcut'], img_width, img_height),
                'breaks_for': ele['sum_breaks_for'],
                'breaks_against': ele['sum_breaks_against'],
                'goals_break_for': ele['sum_goals_break_for'],
                'goals_break_against': ele['sum_goals_break_against'],
                'goals_break_for_pctg':  goals_break_for_pctg,
                'goals_break_against_pctg':  goals_break_against_pctg
            })

    # build final dictionary
    break_chartseries_dic = _break_chartseries_get(logger, break_lake)

    return break_chartseries_dic

def _break_sumup(logger, teamstat_dic):
    """ sum up faceoff statistics """
    logger.debug('_faceoff_sumup()')

    update_amount = 0
    teamstat_sum_dic = {}

    for team_id in teamstat_dic:
        # sumup data per team
        teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'breaks_for', 'breaks_against', 'goals_break_for', 'goals_break_against'])
        # check how many items we have to create in update_dic
        if update_amount < len(teamstat_sum_dic[team_id]):
            update_amount = len(teamstat_sum_dic[team_id])

    return (teamstat_sum_dic, update_amount)

def _break_chartseries_get(logger, data_dic):
    """ build structure for chart series """
    logger.debug('_break_chartseries_get()')
    chartseries_dic = {}
    for ele in data_dic:
        chartseries_dic[ele] = {'x_category': [], 'goals_break_for_pctg': [], 'goals_break_against_pctg': []}
        for datapoint in sorted(data_dic[ele], key=lambda i: i['goals_break_for_pctg'], reverse=True):
            chartseries_dic[ele]['x_category'].append(datapoint['name'])
            chartseries_dic[ele]['goals_break_for_pctg'].append(datapoint['goals_break_for_pctg'])
            chartseries_dic[ele]['goals_break_against_pctg'].append(datapoint['goals_break_against_pctg'])

    return chartseries_dic

def rebound_updates_get(logger, _ctitle, data_dic, key1, key2):
    """ build structure for chart updates """
    logger.debug('rebound_updates_get()')

    updates_dic = {}
    for ele in data_dic:
        updates_dic[ele] = {
            'chartoptions':  {
                'xAxis': {'categories': data_dic[ele]['x_category'], 'title': title(''), 'maxPadding': 0.1, 'labels': {'useHTML': 1, 'align': 'center'}},
                'series': [
                    # pylint: disable=E0602
                    {'index': 0, 'name': _('leading to own goal'), 'data': data_dic[ele][key1], 'color': chart_color3},
                    {'index': 1, 'name': _('leading to goal against'), 'data': data_dic[ele][key2], 'color': chart_color2},
                ]
            }
        }

    return updates_dic

def shottime2date_map(logger, shot_list):
    """ create a dictionary including a mapping between gametime and realtime (uts) - this is needed to map the tweets """
    logger.debug('shottime2date_map()')

    # mapping from match-minute to game time
    mindate_dic = {}

    prev_tst = 0
    prev_uts = 0
    max_min = 60
    for shot in shot_list:
        #  convert date from shot into a unit-timestamp #?????????
        uts = date_to_uts_utc(shot['real_date']) - 3600
        # we only count if timestamp increases as well as unix timestamp (we ignore manual corrections at the end of the file)
        if prev_tst <= shot['timestamp'] and prev_uts <= uts:
            # get min out of seconds
            min_ = math.ceil(shot['timestamp']/60)
            mindate_dic[min_] = uts
            # ovetime detection
            if shot['timestamp'] > 3600:
                max_min = 65

    # fill empty min artifically (no shots during this minute)
    for min_ in  range(1, max_min+1):
        if min_ not in mindate_dic:
            mindate_dic[min_] = mindate_dic[min_-1] + 60

    return mindate_dic

def xml_check(logger, shot_list):
    """ check xml mode (legacy or new) to adapt calculation of shots """
    logger.debug('xml_check()')
    deviation_dic = deviation_avg_get(logger, shot_list, ['coordinate_x', 'coordinate_y'])

    new_format = True
    if deviation_dic['coordinate_x']['max'] > 50 and deviation_dic['coordinate_x']['min'] < -50:
        new_format = False

    logger.debug('xml_check() returned {0}'.format(new_format))
    return new_format