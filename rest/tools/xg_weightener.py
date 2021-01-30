#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" calculate estimate xg values for a range if weightening parameters and dumps the best estimates into json files """
import os
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

# pylint: disable=E0401, C0413
from rest.functions.corsi import goals5v5_get, gameshots5v5_get
from rest.functions.helper import config_load, logger_setup, json_load, json_store, uts_now
from rest.functions.match import match_info_get, match_list_get
from rest.functions.periodevent import periodevent_get
from rest.functions.shift import shift_get
from rest.functions.shot import shot_list_get
from rest.functions.xg import xgmodel_get, shotlist_process, xgf_calculate, xgscore_get

def _config_load(logger, cfg_file=os.path.dirname(__file__)+'/'+'hockeygraphs.cfg'):
    """" load config from file """
    logger.debug('_config_load()')

    rebound_interval = 0
    break_interval = 0
    config_dic = config_load(cfg_file=cfg_file)
    if 'Shots' in config_dic:
        if 'rebound_interval' in config_dic['Shots']:
            rebound_interval = int(config_dic['Shots']['rebound_interval'])
        if 'break_interval' in config_dic['Shots']:
            break_interval = int(config_dic['Shots']['break_interval'])
    logger.debug('_config_load() ended.')

    return (rebound_interval, break_interval)

def dump_it(g_result_dic_, filename='result.json', limit=20):
    """ dump and shrink result dictionary """
    ele_list = ['home_correct', 'visitor_correct', 'winloss_correct', 'result_correct']

    # new_result_dic = {'home_correct': {}, 'visitor_correct': {}, 'winloss_correct': {}, 'result_correct': {}}
    new_result_dic = {}

    for ele in ele_list:
        new_result_dic[ele] = []
        cnt = 0
        # pylint: disable=W0640
        for result in sorted(g_result_dic_[ele], key=lambda i: (i[ele], i['result_correct'], i['winloss_correct'], i['g_cnt']), reverse=True):
            cnt += 1
            new_result_dic[ele].append(result)
            if cnt >= limit:
                break

    # dump dictionary to store data
    # print('########## dump-disabled ##############')
    json_store(filename, new_result_dic)

    return new_result_dic

def _inputparameters_get(logger, parameter_file, start_val, max_val, step):
    """" load config from file """
    logger.debug('inputparameters_get()')

    # quantifier dictionary
    input_parameters_ = {
        'shots_pctg': {'start': start_val, 'max': max_val, 'step': step},
        'handness_pctg': {'start': start_val, 'max': max_val, 'step': step},
        'handness_shots_pctg': {'start': start_val, 'max': max_val, 'step': step},
        'rb_pctg': {'start': start_val, 'max': max_val, 'step': step},
        'rb_shots_pctg': {'start': start_val, 'max': max_val, 'step': step},
        'br_pctg': {'start': start_val, 'max': max_val, 'step': step},
        'br_shots_pctg': {'start': start_val, 'max': max_val, 'step': step}
    }

    # process parameters file if exists
    if os.path.exists(parameter_file):
        # load start values from file
        parameter_dic = json_load(parameter_file)

        # overwrite start_value we have it in parameter file
        for parameter in input_parameters_:
            if parameter in parameter_dic:
                input_parameters_[parameter]['start'] = parameter_dic[parameter]

    return input_parameters_

def shotstats_get(logger, match_list):
    """" gets shots per match """
    logger.debug('stats_get()')

    g_shotstat_dict = {}
    g_goal_dic_ = {}

    for match_id_ in match_list:

        # get match information
        match_dic = match_info_get(LOGGER, match_id_, None, ['date', 'home_team_id', 'home_team__shortcut', 'visitor_team_id', 'visitor_team__shortcut', 'result'])

        # get list of shots
        vlist = ['shot_id', 'match_id', 'match_shot_resutl_id', 'player_id', 'player__first_name', 'player__last_name', 'player__jersey', 'player__stick', 'team_id', 'coordinate_x', 'coordinate_y', 'match__home_team_id', 'match__visitor_team_id', 'timestamp', 'real_date']
        shot_list = shot_list_get(LOGGER, 'match_id', match_id_, vlist)
        shift_list = shift_get(logger, 'match_id', match_id, ['shift'])
        periodevent_list = periodevent_get(logger, 'match_id', match_id, ['period_event'])

        # get corsi statistics
        (shots_for_5v5, shots_against_5v5, shots_ongoal_for_5v5, shots_ongoal_against_5v5, shot_list_5v5) = gameshots5v5_get(logger, match_id_, match_dic, 'home', shot_list, shift_list, periodevent_list)

        # 5v5 goals from periodevents
        goals5v5_dic = goals5v5_get(logger, match_id_, match_dic)

        # convert shots and goals into structure we can process later on
        # we also need the XGMODEL_DIC to check if we have the shotcoordinates in our structure
        (shotstat_dic, goal_dic) = shotlist_process(LOGGER, shot_list_5v5, XGMODEL_DIC, REBOUND_INTERVAL, BREAK_INTERVAL)
        g_shotstat_dict[match_id_] = shotstat_dic

        # g_goal_dic_[match_id_] = {'home': len(goal_dic['home']), 'visitor': len(goal_dic['visitor'])}
        # we need to compare against 5v5 goals
        g_goal_dic_[match_id_] = {'home': goals5v5_dic['home'], 'visitor': goals5v5_dic['visitor']}

    return(g_shotstat_dict, g_goal_dic_)

if __name__ == "__main__":

    # DEBUG mode on/off
    DEBUG = False

    MODEL_FILE = 'model_data.json'
    PARAMETER_FILE = 'model_parameters.json'
    RESULT_FILE = 'result.json'

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # load rebound and break interval from config file
    (REBOUND_INTERVAL, BREAK_INTERVAL) = _config_load(LOGGER)

    # get model from database
    # XGMODEL_DIC = xgmodel_get(LOGGER)
    XGMODEL_DIC = json_load(MODEL_FILE)

    # get list of matches to investigate
    MATCH_LIST = match_list_get(LOGGER, 'season_id', 1, ['match_id'])
    # MATCH_LIST = [1820]

    START_VAL = 1.0
    MAX_VAL = 3.5
    STEP = 0.5

    # START_VAL = 1.0
    # MAX_VAL = 1.1
    # STEP = 0.1

    # quantifier dictionary
    input_parameters = _inputparameters_get(LOGGER, PARAMETER_FILE, START_VAL, MAX_VAL, STEP)

    from pprint import pprint
    pprint(input_parameters)

    # get global shot and goal stats
    (g_shotstat_dic, g_goal_dic) = shotstats_get(LOGGER, MATCH_LIST)

    # load result dic from file to continue on a certain point
    if os.path.exists(RESULT_FILE):
        g_result_dic = json_load(RESULT_FILE)
    else:
        g_result_dic = {'home_correct': [], 'visitor_correct': [], 'winloss_correct': [], 'result_correct': []}

    # set startpoint for measurement
    uts_start = uts_now()

    # initialze counter
    G_CNT = 0
    for shots_pctg in np.arange(START_VAL, input_parameters['shots_pctg']['max'] + input_parameters['shots_pctg']['step'], input_parameters['shots_pctg']['step']):
        if shots_pctg < input_parameters['shots_pctg']['start']:
            continue
        else:
            input_parameters['shots_pctg']['start'] = START_VAL

        for handness_pctg in np.arange(START_VAL, input_parameters['handness_pctg']['max'] + input_parameters['handness_pctg']['step'], input_parameters['handness_pctg']['step']):
            if handness_pctg < input_parameters['handness_pctg']['start']:
                continue
            else:
                input_parameters['handness_pctg']['start'] = START_VAL

            for handness_shots_pctg in np.arange(START_VAL, input_parameters['handness_shots_pctg']['max'] + input_parameters['handness_shots_pctg']['step'], input_parameters['handness_shots_pctg']['step']):
                if handness_shots_pctg < input_parameters['handness_shots_pctg']['start']:
                    continue
                else:
                    input_parameters['handness_shots_pctg']['start'] = START_VAL

                for rb_pctg in np.arange(START_VAL, input_parameters['rb_pctg']['max'] + input_parameters['rb_pctg']['step'], input_parameters['rb_pctg']['step']):
                    if rb_pctg < input_parameters['rb_pctg']['start']:
                        continue
                    else:
                        input_parameters['rb_pctg']['start'] = START_VAL

                    for rb_shots_pctg in np.arange(START_VAL, input_parameters['rb_shots_pctg']['max'] + input_parameters['rb_shots_pctg']['step'], input_parameters['rb_shots_pctg']['step']):
                        if rb_shots_pctg < input_parameters['rb_shots_pctg']['start']:
                            continue
                        else:
                            input_parameters['rb_shots_pctg']['start'] = START_VAL

                        for br_pctg in np.arange(START_VAL, input_parameters['br_pctg']['max'] + input_parameters['br_pctg']['step'], input_parameters['br_pctg']['step']):
                            if br_pctg < input_parameters['br_pctg']['start']:
                                continue
                            else:
                                input_parameters['br_pctg']['start'] = START_VAL

                            for br_shots_pctg in np.arange(START_VAL, input_parameters['br_shots_pctg']['max'] + input_parameters['br_shots_pctg']['step'], input_parameters['br_shots_pctg']['step']):
                                if br_shots_pctg < input_parameters['br_shots_pctg']['start']:
                                    continue
                                else:
                                    input_parameters['br_shots_pctg']['start'] = START_VAL

                                G_CNT += 1
                                # print(round(shots_pctg, 1), round(handness_pctg, 1), round(handness_shots_pctg, 1), round(rb_pctg, 1), round(rb_shots_pctg, 1), round(br_pctg, 1), round(br_shots_pctg, 1))
                                quantifier_dic = {
                                    'home': {
                                        'shots_pctg': round(shots_pctg, 1),
                                        'handness_pctg': round(handness_pctg, 1),
                                        'handness_shots_pctg': round(handness_shots_pctg, 1),
                                        'rb_pctg': round(rb_pctg, 1),
                                        'rb_shots_pctg': round(rb_shots_pctg, 1),
                                        'br_pctg': round(br_pctg, 1),
                                        'br_shots_pctg': round(br_shots_pctg, 1),
                                    },
                                    'visitor': {
                                        'shots_pctg': round(shots_pctg, 1),
                                        'handness_pctg': round(handness_pctg, 1),
                                        'handness_shots_pctg': round(handness_shots_pctg, 1),
                                        'rb_pctg': round(rb_pctg, 1),
                                        'rb_shots_pctg': round(rb_shots_pctg, 1),
                                        'br_pctg': round(br_pctg, 1),
                                        'br_shots_pctg': round(br_shots_pctg, 1),
                                    }
                                }

                                MATCH_CNT = 0
                                HOME_CORRECT = 0
                                VISITOR_CORRECT = 0
                                WINLOSS_CORRECT = 0
                                RESULT_CORRECT = 0

                                for match_id in g_shotstat_dic:
                                    MATCH_CNT += 1

                                    playerxgf_dic = xgf_calculate(LOGGER, g_shotstat_dic[match_id], quantifier_dic)
                                    xgf_dic = xgscore_get(LOGGER, playerxgf_dic)
                                    # convert xg to make them comparable with 5v5 goals
                                    xgf_dic['home'] = int(round(xgf_dic['home'], 0))
                                    xgf_dic['visitor'] = int(round(xgf_dic['visitor'], 0))
                                    # print(xgf_dic['home'], xgf_dic['visitor'], g_goal_dic[match_id]['home'], g_goal_dic[match_id]['visitor'])

                                    # check homescore
                                    if xgf_dic['home'] == g_goal_dic[match_id]['home']:
                                        HOME_CORRECT += 1
                                    # check visitor score
                                    if xgf_dic['visitor'] == g_goal_dic[match_id]['visitor']:
                                        VISITOR_CORRECT += 1

                                    # check full score
                                    if xgf_dic['home'] == g_goal_dic[match_id]['home'] and xgf_dic['visitor'] == g_goal_dic[match_id]['visitor']:
                                        RESULT_CORRECT += 1

                                    # check for winloss
                                    if xgf_dic['home'] < xgf_dic['visitor'] and g_goal_dic[match_id]['home'] < g_goal_dic[match_id]['visitor']:
                                        WINLOSS_CORRECT += 1
                                    elif xgf_dic['home'] > xgf_dic['visitor'] and g_goal_dic[match_id]['home'] > g_goal_dic[match_id]['visitor']:
                                        WINLOSS_CORRECT += 1
                                    elif xgf_dic['home'] == xgf_dic['visitor'] and g_goal_dic[match_id]['home'] == g_goal_dic[match_id]['visitor']:
                                        WINLOSS_CORRECT += 1

                                tmp_dic = {'g_cnt': G_CNT, 'match_cnt': MATCH_CNT, 'home_correct': HOME_CORRECT, 'visitor_correct': VISITOR_CORRECT, 'winloss_correct': WINLOSS_CORRECT, 'result_correct': RESULT_CORRECT, 'quantifier_dic': quantifier_dic}
                                # store results in different trees
                                g_result_dic['home_correct'].append(tmp_dic)
                                g_result_dic['visitor_correct'].append(tmp_dic)
                                g_result_dic['winloss_correct'].append(tmp_dic)
                                g_result_dic['result_correct'].append(tmp_dic)

                        print('{0}/{4}: dump shots_pctg: {1}, handness_pctg: {2}, handness_shots_pctg: {3}'.format(uts_now()-uts_start, round(shots_pctg, 1), round(handness_pctg, 1), round(handness_shots_pctg, 1), G_CNT))
                        # dump here
                        g_result_dic = dump_it(g_result_dic, RESULT_FILE)
                        # store quantifier dic
                        json_store(PARAMETER_FILE, quantifier_dic['home'])

                # print status
                print('g_cnt', G_CNT, 'match_cnt', MATCH_CNT, 'home_correct', HOME_CORRECT, 'visitor_correct', VISITOR_CORRECT, 'winloss_correct', WINLOSS_CORRECT, 'result_correct', RESULT_CORRECT)
        # dump with uts at the end
        uts = uts_now()
        g_result_dic = dump_it(g_result_dic, 'result_handness_{0}.json'.format(uts))
