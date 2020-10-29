# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import math
import django
django.setup()
from shapely.geometry import Point
from rest.models import Shot
from rest.functions.helper import maxval_get
import functions.rink_dimensions as rd

def _shoot_coordinates_convert(logger, coordinate_x, coordinate_y):
    """ convert  arbitrary coordinates to actual coordinates in meters sourse: leaffan.net """
    try:
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
        for ele in range(1, 5):
            shot_min_dic['home_team'][ele] = {}
            shot_min_dic['visitor_team'][ele] = {}

    for min_ in range(0, x_max):
        if group_by == 'match_shot_resutl_id':
            for ele in range(1, 5):
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
                for ele in range(1, 5):
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

    shot_flow_dic = gameflow_aggregate(logger, shot_sec_dic, x_max)

    return (shot_flow_dic, goal_dic)

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
    shotsum_dic = {'home_team': {1:{}, 2:{}, 3:{}, 4:{},}, 'visitor_team': {1:{}, 2:{}, 3:{}, 4:{},}}
    for ele in range(1, 5):
        home_min_values = list(shot_status_dic['home_team'][ele].values())
        visitor_min_values = list(shot_status_dic['visitor_team'][ele].values())
        for min_ in shot_status_dic['home_team'][ele]:
            shotsum_dic['home_team'][ele][min_] = sum(home_min_values[:min_])
        for min_ in shot_status_dic['visitor_team'][ele]:
            shotsum_dic['visitor_team'][ele][min_] = sum(visitor_min_values[:min_])

    return shotsum_dic

def gameflow_aggregate(logger, shot_sec_dic, x_max):
    """ sum up shots per seconds """
    logger.debug('shotspersec_aggregate()')

    shot_flow_dic = {'home_team': {}, 'visitor_team': {}}

    divisor = 0
    home_team_cnt = 0
    visitor_team_cnt = 0

    for sec_ in range(0, x_max):

        # reset counter during period start
        if sec_ in [1201, 2401, 3601]:
            home_team_cnt = 0
            visitor_team_cnt = 0
            divisor = 0

        # increase divisor
        divisor += 1

        # increase counter in case there is a shot
        if sec_ in shot_sec_dic['home_team'] and bool(shot_sec_dic['home_team'][sec_]):
            home_team_cnt += 1
        if sec_ in shot_sec_dic['visitor_team'] and bool(shot_sec_dic['visitor_team'][sec_]):
            visitor_team_cnt += 1

        # store counters but only the minute interval
        if sec_ % 60 == 0:
            min_ = sec_/60
            div_ = divisor/60
            shot_flow_dic['home_team'][min_] = round(home_team_cnt * 60/div_, 0)
            shot_flow_dic['visitor_team'][min_] = round(visitor_team_cnt * 60/div_, 0)

    # calculate last second
    shot_flow_dic['home_team'][math.ceil(x_max/60)] = round(home_team_cnt * 60/div_, 0)
    shot_flow_dic['visitor_team'][math.ceil(x_max/60)] = round(visitor_team_cnt * 60/div_, 0)

    return shot_flow_dic

def shotsperzone_count(logger, shot_list, matchinfo_dic):
    """ shots per zone """
    logger.debug('shotsperzone_count()')

    # we need an x_max value for the chart and try to get it from shot_list
    x_max = maxval_get(shot_list, 'timestamp', 60, 1)

    # create empty structure of shots per zone per period
    shot_zone_dic = shot_dic_prep(logger, 'zone', x_max)

    for shot in shot_list:

        # timestamp of shot
        sec_ = shot['timestamp']
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

        #  count shots per zone per period
        shot_zone_dic[team][shot['zone']][period] += 1

    return shot_zone_dic

def shotsperzone_aggregate(logger, shotzone_dic, match_info_dic):
    """ reformat zone statistics for template processing """

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
