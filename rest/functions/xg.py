# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, R0914
import sys

from rest.functions.helper import pctg_float_get
from rest.functions.shot import shotside_get
from rest.models import Xg
from sklearn.neighbors import NearestNeighbors, BallTree
import numpy as np

def _surrondingpoints_get(logger, x_point, y_point):
    # logger.debug('_surrondingpoints_get([{0}, {1}])'.format(x_point, y_point))
    surroundingpoint_list = []
    for x_num in range(x_point-1, x_point+2):
        for y_num in range(y_point-1, y_point+2):
            if not bool(x_num == x_point and y_num == y_point):
                surroundingpoint_list.append([x_num, y_num])

    return surroundingpoint_list

def _surroundingpointval_avg_get(logger, x_point, y_point, model_tree, stick, depth=0):
    # logger.debug('_surroundingpointval_avg_get({0}, {1}) depth: {2}'.format(x_point, y_point, depth))

    shot_pctg_list = []
    handness_shot_pctg_list = []

    if depth <= 5:
        # get surrounding points
        point_list = _surrondingpoints_get(logger, x_point, y_point)

        for x_val, y_val in point_list:
            # convert to strings as keys in model-dic are stored as strings
            x_ele = str(x_val)
            y_ele = str(y_val)

            # check if we have the point in model
            if x_ele in model_tree and y_ele in model_tree[x_ele]:
                # print('yeap')
                (point_shot_pctg, point_handness_shots_pctg) = _coordinates_pctg_get(logger, x_ele, y_ele, model_tree, stick)
                shot_pctg_list.append(point_shot_pctg)
                handness_shot_pctg_list.append(point_handness_shots_pctg)
            else:
                (point_shot_pctg, point_handness_shots_pctg) = _surroundingpointval_avg_get(logger, x_val, y_val, model_tree, stick, depth+1)

    shot_pctg = 0
    handness_shot_pctg = 0
    if len(shot_pctg_list) != 0:
        shot_pctg = round(np.mean(shot_pctg_list), 0)
    if len(handness_shot_pctg_list) != 0:
        handness_shot_pctg = round(np.mean(handness_shot_pctg_list), 0)

    return (shot_pctg, handness_shot_pctg)

def _coordinates_pctg_get(logger, x_point, y_point, model_tree, stick):
    # logger.debug('_coordinates_pctg_get({0}, {1})'.format(x_point, y_point))

    # add shot percentage for this specific coordinate
    shot_pctg = model_tree[x_point][y_point]['shots_pctg']

    # depending of player handness add hadness specific shoot percentage
    # add shot percentage for this specific coordinate
    shot_pctg = model_tree[x_point][y_point]['shots_pctg']

    # depending of player handness add hadness specific shoot percentage
    if stick == 'left':
        handness_shots_pctg = model_tree[x_point][y_point]['lh_shots_pctg']
    elif stick == 'right':
        handness_shots_pctg = model_tree[x_point][y_point]['rh_shots_pctg']

    return (shot_pctg, handness_shots_pctg)

def xgmodel_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('xg_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add authorization
        obj, _created = Xg.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in xg_add(): {0}'.format(err_))
        result = None

    logger.debug('xg_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def xgmodel_get(logger, fkey='id', fvalue=1, vlist=['xg_data']):
    """ get info for a specifc match_id """
    logger.debug('xgmodel_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            xgmodel_dic = list(Xg.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            xgmodel_dic = Xg.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except BaseException:
        xgmodel_dic = {}

    return xgmodel_dic

def _handness_pctg_get(shot_tree_dic):
    """ calculate handness percentage """

    for team_ in shot_tree_dic['shots']:
        for y_val in shot_tree_dic['handness'][team_]:
            shot_tree_dic['handness'][team_][y_val]['left']['shots_pctg'] = pctg_float_get(shot_tree_dic['handness'][team_][y_val]['left']['goals'], shot_tree_dic['handness'][team_][y_val]['left']['shots'], 1)
            shot_tree_dic['handness'][team_][y_val]['right']['shots_pctg'] = pctg_float_get(shot_tree_dic['handness'][team_][y_val]['right']['goals'], shot_tree_dic['handness'][team_][y_val]['right']['shots'], 1)

    return shot_tree_dic

def _shot_percentage_get(shot_tree_dic):
    """ calculate percentage values """
    for team_ in shot_tree_dic['shots']:
        for x_val in shot_tree_dic['shots'][team_]:
            for y_val in shot_tree_dic['shots'][team_][x_val]:
                # score pctg
                shot_tree_dic['shots'][team_][x_val][y_val]['shots_pctg'] = pctg_float_get(shot_tree_dic['shots'][team_][x_val][y_val]['goals'], shot_tree_dic['shots'][team_][x_val][y_val]['shots'], 1)

                # left hand goal percentage
                shot_tree_dic['shots'][team_][x_val][y_val]['lh_shots_pctg'] = pctg_float_get(shot_tree_dic['shots'][team_][x_val][y_val]['lh_goals'], shot_tree_dic['shots'][team_][x_val][y_val]['lh_shots'], 1)

                #  right hand goal percentage
                shot_tree_dic['shots'][team_][x_val][y_val]['rh_shots_pctg'] = pctg_float_get(shot_tree_dic['shots'][team_][x_val][y_val]['rh_goals'], shot_tree_dic['shots'][team_][x_val][y_val]['rh_shots'], 1)

                # rebound pctg
                shot_tree_dic['shots'][team_][x_val][y_val]['rb_shots_pctg'] = pctg_float_get(shot_tree_dic['shots'][team_][x_val][y_val]['rb_goals'], shot_tree_dic['shots'][team_][x_val][y_val]['rb_shots'], 1)

                # break pctg
                shot_tree_dic['shots'][team_][x_val][y_val]['br_shots_pctg'] = pctg_float_get(shot_tree_dic['shots'][team_][x_val][y_val]['br_goals'], shot_tree_dic['shots'][team_][x_val][y_val]['br_shots'], 1)

    return shot_tree_dic

def pctg_calculate(tree_dic):
    """ enrich dictionary with percentage """

    # calculate rebound percentage
    for ele in tree_dic['rebounds']:
        tree_dic['rebounds'][ele]['shots_pctg'] = pctg_float_get(tree_dic['rebounds'][ele]['goals'], tree_dic['rebounds'][ele]['shots'], 1)

    # calculate break percentage
    for ele in tree_dic['breaks']:
        tree_dic['breaks'][ele]['shots_pctg'] = pctg_float_get(tree_dic['breaks'][ele]['goals'], tree_dic['breaks'][ele]['shots'], 1)

    # calcolate percentage for coordinates
    tree_dic = _shot_percentage_get(tree_dic)

    # calculate persentate for lef/righthand data
    tree_dic = _handness_pctg_get(tree_dic)

    return tree_dic

def _handness_get(shot, player_dic):
    """ get handness """
    if shot['player_id'] in player_dic:
        handness = player_dic[shot['player_id']]['stick']
    else:
        handness = 'left'
    return handness

def xgmodel_build(logger, shot_list, player_dic, rebound_interval=5, break_interval=5):
    """ build the xg model tree """
    logger.debug('model_build()')

    # initialize empty dictionary storing the model
    model_tree = {'shots': {'home':  {}, 'visitor': {}}, 'rebounds': {}, 'breaks': {}, 'handness': {'home': {}, 'visitor': {}}}

    # clear variables before starting shot processing
    prev_match_id = 0
    prev_team = None
    prev_time = 0

    for shot in shot_list:

        # reset counters in case of match changes
        # this is to avoid that we fuckup rebout and break detection
        if prev_match_id != shot['match_id']:
            #logger.debug('match_rollover {0}'.format(shot['match_id']))
            prev_match_id = shot['match_id']
            prev_team = None
            prev_time = 0

        # we need the shot_side and the team for later processing
        (team, side) = shotside_get(shot, shot['match__home_team_id'], shot['match__visitor_team_id'])

        if team and side:
            # handness of shooter
            handness = _handness_get(shot, player_dic)

            # store get coordinates for better readability
            coordinate_x = shot['coordinate_x']
            coordinate_y = shot['coordinate_y']

            # handness shot success of left/right hand player
            if coordinate_y not in model_tree['handness'][team]:
                model_tree['handness'][team][coordinate_y] = {'side': side, 'left': {'shots': 0, 'goals': 0}, 'right': {'shots': 0, 'goals': 0}}
            model_tree['handness'][team][coordinate_y][handness]['shots'] += 1
            if shot['match_shot_resutl_id'] == 4:
                model_tree['handness'][team][coordinate_y][handness]['goals'] += 1

            # create subtree(s) for x and y values if not existing
            if coordinate_x not in model_tree['shots'][team]:
                model_tree['shots'][team][coordinate_x] = {}
            if coordinate_y not in model_tree['shots'][team][coordinate_x]:
                model_tree['shots'][team][coordinate_x][coordinate_y] = {'side': side, 'shots': 0, 'goals': 0, 'lh_shots': 0, 'lh_goals': 0, 'rh_shots': 0, 'rh_goals': 0, 'rb_shots': 0, 'rb_goals': 0, 'br_shots': 0, 'br_goals': 0}

            # count shots
            model_tree['shots'][team][coordinate_x][coordinate_y]['shots'] += 1
            # count handness
            if handness == 'left':
                model_tree['shots'][team][coordinate_x][coordinate_y]['lh_shots'] += 1
            else:
                model_tree['shots'][team][coordinate_x][coordinate_y]['rh_shots'] += 1

            # count goals
            if shot['match_shot_resutl_id'] == 4:
                model_tree['shots'][team][coordinate_x][coordinate_y]['goals'] += 1
                # count handness
                if handness == 'left':
                    model_tree['shots'][team][coordinate_x][coordinate_y]['lh_goals'] += 1
                else:
                    model_tree['shots'][team][coordinate_x][coordinate_y]['rh_goals'] += 1

            # rebound detection
            rb_diff = abs(shot['timestamp'] - prev_time)
            if team == prev_team and abs(shot['timestamp'] - prev_time) <= rebound_interval:
                # this is a rebound
                model_tree['shots'][team][coordinate_x][coordinate_y]['rb_shots'] += 1
                if rb_diff not in model_tree['rebounds']:
                    # create entry in rebounds tree
                    model_tree['rebounds'][rb_diff] = {'shots': 0, 'goals': 0}

                # store entry in tree
                model_tree['rebounds'][rb_diff]['shots'] += 1
                if shot['match_shot_resutl_id'] == 4:
                    # this rebound leads to a goal
                    model_tree['shots'][team][coordinate_x][coordinate_y]['rb_goals'] += 1
                    model_tree['rebounds'][rb_diff]['goals'] += 1

            # break detection
            br_diff = abs(shot['timestamp'] - prev_time)
            if team != prev_team and abs(prev_time - shot['timestamp']) <= break_interval:
                # this is a break
                model_tree['shots'][team][coordinate_x][coordinate_y]['br_shots'] += 1
                if br_diff not in model_tree['breaks']:
                    model_tree['breaks'][br_diff] = {'shots': 0, 'goals': 0}

                # store entry in tree
                model_tree['breaks'][br_diff]['shots'] += 1
                if shot['match_shot_resutl_id'] == 4:
                    # this break leads to a goal
                    model_tree['shots'][team][coordinate_x][coordinate_y]['br_goals'] += 1
                    model_tree['breaks'][br_diff]['goals'] += 1

            # store team and timestamp for comparison in next interation
            prev_team = team
            prev_time = shot['timestamp']

    return model_tree

def shotlist_process(logger, shot_list, model_tree, rebound_interval, break_interval):
    """ process shot_dic """
    logger.debug('shot_dic_process()')

    # create dictionaries and variables we need
    shotsum_dic = {'home': {}, 'visitor': {}}
    goal_dic = {'home': [], 'visitor': []}
    prev_team = None
    prev_time = 0

    for shot in shot_list:
        # check if shot comes from home or visitor that we can lookup the right part of the model
        if shot['team_id'] == shot['match__home_team_id']:
            team = 'home'
        else:
            team = 'visitor'

        # add goals to dictionary
        if shot['match_shot_resutl_id'] == 4:
            goal_dic[team].append('{0} {1} ({2})'.format(shot['player__first_name'], shot['player__last_name'], shot['timestamp']))

        # create playerspecific subtree in shotsum_dic if does not exist
        if shot['player_id'] not in shotsum_dic[team]:
            shotsum_dic[team][shot['player_id']] = {'jersey': shot['player__jersey'], 'name': '{0} {1}'.format(shot['player__first_name'], shot['player__last_name']), 'handness': shot['player__stick'], 'shots': []}

        # create a temporary dictionary to be added to player specific shot list
        tmp_dic = {}

        if str(shot['coordinate_y']) in model_tree['handness'][team]:
            # add left/right hand percentage for this specific y-coordinate
            tmp_dic['handness_pctg'] = model_tree['handness'][team][str(shot['coordinate_y'])][shot['player__stick']]['shots_pctg']

        if str(shot['coordinate_y']) in model_tree['shots'][team][str(shot['coordinate_x'])]:
            (tmp_dic['shots_pctg'], tmp_dic['handness_shots_pctg']) = _coordinates_pctg_get(logger, str(shot['coordinate_x']), str(shot['coordinate_y']), model_tree['shots'][team], shot['player__stick'])
        else:
            (tmp_dic['shots_pctg'], tmp_dic['handness_shots_pctg']) = _surroundingpointval_avg_get(logger, shot['coordinate_x'], shot['coordinate_y'], model_tree['shots'][team], shot['player__stick'])

        # time difference to previous shot
        shot_diff = abs(shot['timestamp'] - prev_time)

        # rebound detection
        if shot['team_id'] == prev_team and shot_diff <= rebound_interval:
            # add sucess percentage for rebound timeframe
            tmp_dic['rb_pctg'] = model_tree['rebounds'][str(shot_diff)]['shots_pctg']
            if str(shot['coordinate_y']) in model_tree['shots'][team][str(shot['coordinate_x'])]:
                # add rebound success percentage for this particular shoot-position
                tmp_dic['rb_shots_pctg'] = model_tree['shots'][team][str(shot['coordinate_x'])][str(shot['coordinate_y'])]['rb_shots_pctg']

        # break detection
        if shot['team_id'] != prev_team and shot_diff <= break_interval:
            # add sucess percentage for break timeframe
            tmp_dic['br_pctg'] = model_tree['breaks'][str(shot_diff)]['shots_pctg']
            if str(shot['coordinate_y']) in model_tree['shots'][team][str(shot['coordinate_x'])]:
                # add break success percentage for this particular shoot-position
                tmp_dic['br_shots_pctg'] = model_tree['shots'][team][str(shot['coordinate_x'])][str(shot['coordinate_y'])]['br_shots_pctg']

        # store shot in list
        shotsum_dic[team][shot['player_id']]['shots'].append(tmp_dic)

        # store term and timestamp for comparison in next interation
        prev_team = shot['team_id']
        prev_time = shot['timestamp']

    return (shotsum_dic, goal_dic)


# def xgf_calculate(logger, shot)
