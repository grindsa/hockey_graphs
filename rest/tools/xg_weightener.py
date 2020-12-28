#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" calculate xg values """
import os
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from rest.functions.helper import config_load, logger_setup, json_load, json_store, uts_now
from rest.functions.shot import shot_list_get
from rest.functions.match import match_info_get, match_list_get
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

def dump_it(g_result_dic, filename='result.json', limit=20):

    ele_list = ['home_correct', 'visitor_correct', 'winloss_correct', 'result_correct']

    # new_result_dic = {'home_correct': {}, 'visitor_correct': {}, 'winloss_correct': {}, 'result_correct': {}}
    new_result_dic = {}

    for ele in ele_list:
        new_result_dic[ele] = []
        cnt = 0
        for result in sorted(g_result_dic[ele], key=lambda i: (i[ele], i['result_correct'], i['winloss_correct'], i['g_cnt']), reverse=True):
            cnt += 1
            new_result_dic[ele].append(result)
            if cnt >= limit:
                break

    # dump dictionary to store data
    # print('########## dump-disabled ##############')
    json_store(filename, new_result_dic)

    return new_result_dic

if __name__ == "__main__":

    # DEBUG mode on/off
    DEBUG = False

    MODEL_FILE = 'model_data.json'

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

    START_VAL = 0.5
    MAX_VAL = 2.5
    STEP = 0.5

    # START_VAL = 1.0
    # MAX_VAL = 1.1
    # STEP = 0.1

    # quantifier dictionary
    input_parameters = {
        'shot_pctg': {'start': START_VAL, 'max': MAX_VAL, 'step': STEP},
        'handness_pctg': {'start': START_VAL, 'max': MAX_VAL, 'step': STEP},
        'handness_shots_pctg': {'start': START_VAL, 'max': MAX_VAL, 'step': STEP},
        'rb_pctg': {'start': START_VAL, 'max': MAX_VAL, 'step': STEP},
        'rb_shots_pctg': {'start': START_VAL, 'max': MAX_VAL, 'step': STEP},
        'br_pctg': {'start': START_VAL, 'max': MAX_VAL, 'step': STEP},
        'br_shots_pctg': {'start': START_VAL, 'max': MAX_VAL, 'step': STEP},
    }

    g_shotstat_dict = {}
    g_goal_dic = {}
    for match_id in MATCH_LIST:

        match_dic = match_info_get(LOGGER, match_id, None, ['date', 'home_team__shortcut', 'visitor_team__shortcut', 'result'])

        # get list of shots
        VLIST = ['shot_id', 'match_id', 'match_shot_resutl_id', 'player_id', 'player__first_name', 'player__last_name', 'player__jersey', 'player__stick', 'team_id', 'coordinate_x', 'coordinate_y', 'match__home_team_id', 'match__visitor_team_id', 'timestamp']
        shot_list = shot_list_get(LOGGER, 'match_id', match_id, VLIST)

        # convert shots and goals into structure we can process later on
        # we also need the XGMODEL_DIC to check if we have the shotcoordinates in our structure
        (shotstat_dic, goal_dic) = shotlist_process(LOGGER, shot_list, XGMODEL_DIC, REBOUND_INTERVAL, BREAK_INTERVAL)
        g_shotstat_dict[match_id] = shotstat_dic
        g_goal_dic[match_id] = {'home': len(goal_dic['home']), 'visitor': len(goal_dic['visitor'])}


    # g_result_dic = {'home_correct': [], 'visitor_correct': [], 'winloss_correct': [], 'result_correct': []}
    # load result dic from file to continue on a certain point
    g_result_dic = json_load('result.json')

    # set startpoint for measurement
    uts_start = uts_now()

    # initialze counter
    g_cnt = 0

    for shots_pctg in np.arange(input_parameters['shot_pctg']['start'], input_parameters['shot_pctg']['max'] + input_parameters['shot_pctg']['step'], input_parameters['shot_pctg']['step']):
        for handness_pctg in np.arange(input_parameters['handness_pctg']['start'], input_parameters['handness_pctg']['max'] + input_parameters['handness_pctg']['step'], input_parameters['handness_pctg']['step']):
            for handness_shots_pctg in np.arange(input_parameters['handness_shots_pctg']['start'], input_parameters['handness_shots_pctg']['max'] + input_parameters['handness_shots_pctg']['step'], input_parameters['handness_shots_pctg']['step']):
                for rb_pctg in np.arange(input_parameters['rb_pctg']['start'], input_parameters['rb_pctg']['max'] + input_parameters['rb_pctg']['step'], input_parameters['rb_pctg']['step']):
                    for rb_shots_pctg in np.arange(input_parameters['rb_shots_pctg']['start'], input_parameters['rb_shots_pctg']['max'] + input_parameters['rb_shots_pctg']['step'], input_parameters['rb_shots_pctg']['step']):
                        for br_pctg in np.arange(input_parameters['br_pctg']['start'], input_parameters['br_pctg']['max'] + input_parameters['br_pctg']['step'], input_parameters['br_pctg']['step']):
                            for br_shots_pctg in np.arange(input_parameters['br_shots_pctg']['start'], input_parameters['br_shots_pctg']['max'] + input_parameters['br_shots_pctg']['step'], input_parameters['br_shots_pctg']['step']):
                                g_cnt += 1
                                # print(round(shots_pctg, 1), round(handness_pctg, 1), round(handness_shots_pctg, 1), round(rb_pctg, 1), round(rb_shots_pctg, 1), round(br_pctg, 1), round(br_shots_pctg, 1))
                                quantifier_dic = {
                                    'shots_pctg': round(shots_pctg, 1),
                                    'handness_pctg': round(handness_pctg, 1),
                                    'handness_shots_pctg': round(handness_shots_pctg, 1),
                                    'rb_pctg': round(rb_pctg, 1),
                                    'rb_shots_pctg': round(rb_shots_pctg, 1),
                                    'br_pctg': round(br_pctg, 1),
                                    'br_shots_pctg': round(br_shots_pctg, 1),
                                }

                                match_cnt = 0
                                home_correct = 0
                                visitor_correct = 0
                                winloss_correct = 0
                                result_correct = 0

                                for match_id in g_shotstat_dict:
                                    match_cnt += 1
                                    playerxgf_dic = xgf_calculate(LOGGER, shotstat_dic, quantifier_dic)
                                    xgf_dic = xgscore_get(LOGGER, playerxgf_dic)
                                    # print(xgf_dic['home'], xgf_dic['visitor'], g_goal_dic[match_id]['home'], g_goal_dic[match_id]['visitor'])

                                    # check homescore
                                    if xgf_dic['home'] == g_goal_dic[match_id]['home']:
                                        home_correct += 1
                                    # check visitor score
                                    if xgf_dic['visitor'] == g_goal_dic[match_id]['visitor']:
                                        visitor_correct += 1

                                    # check full score
                                    if xgf_dic['home'] == g_goal_dic[match_id]['home'] and xgf_dic['visitor'] == g_goal_dic[match_id]['visitor']:
                                        result_correct += 1

                                    # check for winloss
                                    if xgf_dic['home'] < xgf_dic['visitor'] and g_goal_dic[match_id]['home'] < g_goal_dic[match_id]['visitor']:
                                        winloss_correct += 1
                                    elif xgf_dic['home'] > xgf_dic['visitor'] and g_goal_dic[match_id]['home'] > g_goal_dic[match_id]['visitor']:
                                        winloss_correct += 1
                                    elif xgf_dic['home'] == xgf_dic['visitor'] and g_goal_dic[match_id]['home'] == g_goal_dic[match_id]['visitor']:
                                        winloss_correct += 1

                                tmp_dic = {'g_cnt': g_cnt, 'match_cnt': match_cnt, 'home_correct': home_correct, 'visitor_correct': visitor_correct, 'winloss_correct': winloss_correct, 'result_correct': result_correct, 'quantifier_dic': quantifier_dic}
                                # store results in different trees
                                g_result_dic['home_correct'].append(tmp_dic)
                                g_result_dic['visitor_correct'].append(tmp_dic)
                                g_result_dic['winloss_correct'].append(tmp_dic)
                                g_result_dic['result_correct'].append(tmp_dic)
                        print('{0}: dump shot_pctg: {1}, handness_pctg: {2}, handness_shots_pctg: {3}'.format(uts_now()-uts_start, round(shots_pctg, 1), round(handness_pctg, 1), round(handness_shots_pctg, 1)))
                        # dump here
                        g_result_dic = dump_it(g_result_dic)
                # print status
                print('g_cnt', g_cnt, 'match_cnt', match_cnt, 'home_correct', home_correct, 'visitor_correct', visitor_correct, 'winloss_correct', winloss_correct, 'result_correct', result_correct)
        # dump with uts at the end
        uts = uts_now()
        g_result_dic = dump_it(g_result_dic, 'result_handness_{0}.json'.format(uts))
