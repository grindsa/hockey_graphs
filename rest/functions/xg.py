# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, R0914
from rest.functions.helper import pctg_float_get
from rest.functions.shot import shotside_get
from rest.models import Xg

def xg_add(logger, fkey, fvalue, data_dic):
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

def model_build(logger, shot_list, player_dic, rebound_interval=5, break_interval=5):
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
