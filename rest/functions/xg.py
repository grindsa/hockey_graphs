# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, R0914
import numpy as np
from rest.functions.helper import pctg_float_get
from rest.functions.shot import shotside_get
from rest.models import Xg

def _surrondingpoints_get(_logger, x_point, y_point):
    """ get points around a x/y value """
    # logger.debug('_surrondingpoints_get([{0}, {1}])'.format(x_point, y_point))
    surroundingpoint_list = []
    for x_num in range(x_point-1, x_point+2):
        for y_num in range(y_point-1, y_point+2):
            if not bool(x_num == x_point and y_num == y_point):
                surroundingpoint_list.append([x_num, y_num])

    return surroundingpoint_list

def _shotlists_get(logger, model_tree, point_list, depth):
    """ get value lists """
    shot_pctg_list = []
    lh_shots_pctg_list = []
    rh_shots_pctg_list = []
    rb_shots_pctg_list = []
    br_shots_pctg_list = []

    for x_val, y_val in point_list:
        # convert to strings as keys in model-dic are stored as strings
        x_ele = str(x_val)
        y_ele = str(y_val)

        # check if we have the point in model
        if x_ele in model_tree and y_ele in model_tree[x_ele]:
            if 'tmp' in model_tree[x_ele][y_ele]:
                logger.debug('reuse formerly created: {0}:{1}, depth: {2}'.format(x_ele, y_ele, depth))
            (point_shot_pctg, point_lh_shots_pctg, point_rh_shots_pctg, point_rb_shots_pctg, point_br_shots_pctg) = _coordinates_pctg_get(logger, model_tree, x_ele, y_ele)
            shot_pctg_list.append(point_shot_pctg)
            lh_shots_pctg_list.append(point_lh_shots_pctg)
            rh_shots_pctg_list.append(point_rh_shots_pctg)
            rb_shots_pctg_list.append(point_rb_shots_pctg)
            br_shots_pctg_list.append(point_br_shots_pctg)
        else:
            model_tree = _surroundingpointval_avg_get(logger, x_val, y_val, model_tree, depth+1)

    return (depth, shot_pctg_list, lh_shots_pctg_list, rh_shots_pctg_list, rb_shots_pctg_list, br_shots_pctg_list)

def _surroundingpointval_avg_get(logger, x_point, y_point, model_tree, depth=0):
    """ main function to fill missing data with data from surrounding points """
    # logger.debug('_surroundingpointval_avg_get({0}, {1}) depth: {2}'.format(x_point, y_point, depth))

    if depth <= 5:
        # get surrounding points
        point_list = _surrondingpoints_get(logger, x_point, y_point)

        # get the lists of shots to calculate percentage values
        (depth, shot_pctg_list, lh_shots_pctg_list, rh_shots_pctg_list, rb_shots_pctg_list, br_shots_pctg_list) = _shotlists_get(logger, model_tree, point_list, depth)

        # calcuate average value from list
        shot_pctg = _avg_calculate(shot_pctg_list, 0)
        lh_shots_pctg = _avg_calculate(lh_shots_pctg_list, 0)
        rh_shots_pctg = _avg_calculate(rh_shots_pctg_list, 0)
        rb_shots_pctg = _avg_calculate(rb_shots_pctg_list, 0)
        br_shots_pctg = _avg_calculate(br_shots_pctg_list, 0)

        # store data in model to speedup later processing
        model_tree = _model_update(logger, model_tree, x_point, y_point, shot_pctg, lh_shots_pctg, rh_shots_pctg, rb_shots_pctg, br_shots_pctg, depth)

    return model_tree

def _avg_calculate(input_list, decimals=1):
    avg_value = 0
    if len(input_list) != 0:
        avg_value = round(np.mean(input_list), decimals)
    return avg_value

def _model_update(logger, model_tree, x_point, y_point, shot_pctg, lh_shot_pctg, rh_shot_pctg, rb_shots_pctg, br_shots_pctg, depth):
    # logger.debug('_model_update({0}:{1}) depth: {2}'.format(x_point, y_point, depth))
    # x/y points must be stored as strings
    if str(x_point) not in model_tree:
        logger.debug('create x: {0}, depth: {1}'.format(x_point, depth))
        model_tree[str(x_point)] = {}
    if str(y_point) not in model_tree[str(x_point)]:
        logger.debug('create [x, y]: [{0},{1}], depth: {2}'.format(x_point, y_point, depth))
        model_tree[str(x_point)][str(y_point)] = {}
        # create this entry to check reuse
        model_tree[str(x_point)][str(y_point)]['tmp'] = True

    # update model
    model_tree[str(x_point)][str(y_point)]['shots_pctg'] = shot_pctg
    model_tree[str(x_point)][str(y_point)]['rb_shots_pctg'] = rb_shots_pctg
    model_tree[str(x_point)][str(y_point)]['br_shots_pctg'] = br_shots_pctg
    model_tree[str(x_point)][str(y_point)]['lh_shots_pctg'] = lh_shot_pctg
    model_tree[str(x_point)][str(y_point)]['rh_shots_pctg'] = rh_shot_pctg

    return model_tree

def _coordinates_pctg_get(_logger, model_tree, x_point, y_point):
    # logger.debug('_coordinates_pctg_get({0}, {1})'.format(x_point, y_point))
    # add shot percentage for this specific coordinate
    shot_pctg = model_tree[x_point][y_point]['shots_pctg']

    # depending of player handness add hadness specific shoot percentage
    # add shot percentage for this specific coordinate
    shot_pctg = model_tree[x_point][y_point]['shots_pctg']

    # rb and br percentage (only needed for entries we calculate based on surroundings)
    #  print(model_tree[x_point][y_point])
    rb_shots_pctg = model_tree[x_point][y_point]['rb_shots_pctg']
    br_shots_pctg = model_tree[x_point][y_point]['br_shots_pctg']
    lh_shots_pctg = model_tree[x_point][y_point]['lh_shots_pctg']
    rh_shots_pctg = model_tree[x_point][y_point]['rh_shots_pctg']

    return (shot_pctg, lh_shots_pctg, rh_shots_pctg, rb_shots_pctg, br_shots_pctg)

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

# pylint: disable=W0102
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
    # pylint: disable=R0915
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

        if str(shot['coordinate_x']) not in model_tree['shots'][team] or str(shot['coordinate_y']) not in model_tree['shots'][team][str(shot['coordinate_x'])]:
            model_tree['shots'][team] = _surroundingpointval_avg_get(logger, shot['coordinate_x'], shot['coordinate_y'], model_tree['shots'][team])

        (tmp_dic['shots_pctg'], rh_shots_pctg, lh_shots_pctg, rb_shots_pctg, br_shots_pctg) = _coordinates_pctg_get(logger, model_tree['shots'][team], str(shot['coordinate_x']), str(shot['coordinate_y']))

        if shot['player__stick'] == 'left':
            tmp_dic['handness_shots_pctg'] = lh_shots_pctg
        else:
            tmp_dic['handness_shots_pctg'] = rh_shots_pctg

        # time difference to previous shot
        shot_diff = abs(shot['timestamp'] - prev_time)

        # rebound detection
        if shot['team_id'] == prev_team and shot_diff <= rebound_interval:
            # add sucess percentage for rebound timeframe
            tmp_dic['rb_pctg'] = model_tree['rebounds'][str(shot_diff)]['shots_pctg']
            tmp_dic['rb_shots_pctg'] = rb_shots_pctg

        # break detection
        if shot['team_id'] != prev_team and shot_diff <= break_interval:
            # add sucess percentage for break timeframe
            tmp_dic['br_pctg'] = model_tree['breaks'][str(shot_diff)]['shots_pctg']
            tmp_dic['br_shots_pctg'] = br_shots_pctg

        # store shot in list
        shotsum_dic[team][shot['player_id']]['shots'].append(tmp_dic)

        # store term and timestamp for comparison in next interation
        prev_team = shot['team_id']
        prev_time = shot['timestamp']

    return (shotsum_dic, goal_dic)


def xgf_calculate(logger, shot_stat_dic, quantifier_dic):
    """ calculate xgf per player """
    logger.debug('xgf_calculate()')

    player_xgf_dic = {}

    for team in shot_stat_dic:
        player_xgf_dic[team] = {}

        for player_id_ in shot_stat_dic[team]:

            player_xgf_dic[team][player_id_] = {'jersey': shot_stat_dic[team][player_id_]['jersey'], 'name': shot_stat_dic[team][player_id_]['name'], 'shot_weight_sum': 0, 'shot_weight_sum_list': []}
            # interate shots
            for shot in shot_stat_dic[team][player_id_]['shots']:

                if shot['shots_pctg'] > 0:
                    # add shot
                    shot_sum = shot['shots_pctg'] * quantifier_dic['shots_pctg']
                    shot_divisor = 1

                    # consider hadness (if greater than 0)
                    if shot['handness_pctg'] > 0:
                        shot_sum = shot_sum + shot['handness_pctg'] * quantifier_dic['handness_pctg']
                        shot_divisor += 1

                    # consider shot specific handness (if greater than 0)
                    if shot['handness_shots_pctg'] > 0:
                        shot_sum = shot_sum + shot['handness_shots_pctg'] * quantifier_dic['handness_shots_pctg']
                        shot_divisor += 1

                    # consider rebounds (if avaialble)
                    if 'rb_pctg' in shot:
                        shot_sum = shot_sum + shot['rb_pctg'] * quantifier_dic['rb_pctg']
                        shot_divisor += 1
                        # consider rebounds per coordinate if greater than 0
                        if shot['rb_shots_pctg'] > 0:
                            shot_sum = shot_sum + shot['rb_shots_pctg'] * quantifier_dic['rb_shots_pctg']
                            shot_divisor += 1

                    # consider breaks (if avaialble)
                    if 'br_pctg' in shot:
                        shot_sum = shot_sum + shot['br_pctg'] * quantifier_dic['br_pctg']
                        shot_divisor += 1
                        # consider brigger per coordinate if greater than 0
                        if shot['br_shots_pctg'] > 0:
                            shot_sum = shot_sum + shot['br_shots_pctg'] * quantifier_dic['br_shots_pctg']
                            shot_divisor += 1

                    # calculate shot likelyhood
                    shot_weight = round(shot_sum/shot_divisor, 1)

                    player_xgf_dic[team][player_id_]['shot_weight_sum_list'].append(shot_weight)

                    # sum up shot_weight
                    player_xgf_dic[team][player_id_]['shot_weight_sum'] = player_xgf_dic[team][player_id_]['shot_weight_sum'] + shot_weight

    return player_xgf_dic

def xgscore_get(logger, playerxgf_dic):
    """ calculate xgf per player """
    logger.debug('xgscore_get()')

    xgf_dic = {'home': 0, 'visitor': 0}
    for team in playerxgf_dic:
        for player_id in playerxgf_dic[team]:
            xgf = round(playerxgf_dic[team][player_id]['shot_weight_sum']/100, 0)
            if xgf >= 1:
                # print(player_id, playerxgf_dic[team][player_id]['jersey'], playerxgf_dic[team][player_id]['name'], round(playerxgf_dic[team][player_id]['shot_weight_sum']/100, 0), playerxgf_dic[team][player_id]['shot_weight_sum'])
                xgf_dic[team] += int(xgf)

    return xgf_dic
