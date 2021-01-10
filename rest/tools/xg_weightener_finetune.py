#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" checks in smaller steps around the values created by xg_weightener.py for finetuning """
import os
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from rest.functions.helper import config_load, logger_setup, json_load, json_store, uts_now
from rest.functions.shot import shot_list_get
from rest.functions.match import match_list_get
from rest.functions.xg import xgmodel_get, shotlist_process, xgf_calculate, xgscore_get

from pprint import pprint

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

def _dump_it(g_result_dic_, filename='result_finetune.json', limit=20):
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

def _shotstats_get(logger, match_list):
    """" gets shots per match """
    logger.debug('stats_get()')

    g_shotstat_dict = {}
    g_goal_dic_ = {}
    for match_id_ in match_list:

        # get list of shots
        vlist = ['shot_id', 'match_id', 'match_shot_resutl_id', 'player_id', 'player__first_name', 'player__last_name', 'player__jersey', 'player__stick', 'team_id', 'coordinate_x', 'coordinate_y', 'match__home_team_id', 'match__visitor_team_id', 'timestamp']
        shot_list = shot_list_get(LOGGER, 'match_id', match_id_, vlist)

        # convert shots and goals into structure we can process later on
        # we also need the XGMODEL_DIC to check if we have the shotcoordinates in our structure
        (shotstat_dic, goal_dic) = shotlist_process(LOGGER, shot_list, XGMODEL_DIC, REBOUND_INTERVAL, BREAK_INTERVAL)
        g_shotstat_dict[match_id_] = shotstat_dic
        g_goal_dic_[match_id_] = {'home': len(goal_dic['home']), 'visitor': len(goal_dic['visitor'])}

    return(g_shotstat_dict, g_goal_dic_)

def _loopranges_get(logger, quantifier_dic, deviation, step_size):
    """ get ranges """
    logger.debug('_loopranges_get()')

    # quantifier dictionary
    input_parameters_ = {
        'shots_pctg': {'start': quantifier_dic['shots_pctg'] - deviation, 'max': quantifier_dic['shots_pctg'] + deviation, 'step': step_size},
        'handness_pctg': {'start': quantifier_dic['handness_pctg'] - deviation, 'max': quantifier_dic['handness_pctg'] + deviation, 'step': step_size},
        'handness_shots_pctg': {'start': quantifier_dic['handness_shots_pctg'] - deviation, 'max': quantifier_dic['handness_shots_pctg'] + deviation, 'step': step_size},
        'rb_pctg': {'start': quantifier_dic['rb_pctg'] - deviation, 'max': quantifier_dic['rb_pctg'] + deviation, 'step': step_size},
        'rb_shots_pctg': {'start': quantifier_dic['rb_shots_pctg'] - deviation, 'max': quantifier_dic['rb_shots_pctg'] + deviation, 'step': step_size},
        'br_pctg': {'start': quantifier_dic['br_pctg'] - deviation, 'max': quantifier_dic['br_pctg'] + deviation, 'step': step_size},
        'br_shots_pctg': {'start': quantifier_dic['br_shots_pctg'] - deviation, 'max': quantifier_dic['br_shots_pctg'] + deviation, 'step': step_size}
    }
    return input_parameters_

def weights_finetune(logger, uts_start, result_file, g_result_dic, g_shotstat_dic, g_goal_dic, xgmodel_dic, rebound_interval, break_interval, loop_dic):
    """ this is the main finetuner """
    g_cnt = 0
    for shots_pctg in np.arange(loop_dic['shots_pctg']['start'], loop_dic['shots_pctg']['max'], loop_dic['shots_pctg']['step']):
        for handness_pctg in np.arange(loop_dic['handness_pctg']['start'], loop_dic['handness_pctg']['max'], loop_dic['handness_pctg']['step']):
            for handness_shots_pctg in np.arange(loop_dic['handness_shots_pctg']['start'], loop_dic['handness_shots_pctg']['max'], loop_dic['handness_shots_pctg']['step']):
                for rb_pctg in np.arange(loop_dic['rb_pctg']['start'], loop_dic['rb_pctg']['max'], loop_dic['rb_pctg']['step']):
                    for rb_shots_pctg in np.arange(loop_dic['rb_shots_pctg']['start'], loop_dic['rb_shots_pctg']['max'], loop_dic['rb_shots_pctg']['step']):
                        for br_pctg in np.arange(loop_dic['br_pctg']['start'], loop_dic['br_pctg']['max'], loop_dic['br_pctg']['step']):
                            for br_shots_pctg in np.arange(loop_dic['br_shots_pctg']['start'], loop_dic['br_shots_pctg']['max'], loop_dic['br_shots_pctg']['step']):
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

                                for match_id in g_shotstat_dic:
                                    match_cnt += 1
                                    playerxgf_dic = xgf_calculate(logger, g_shotstat_dic[match_id], quantifier_dic)
                                    xgf_dic = xgscore_get(logger, playerxgf_dic)
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

                print('{0}: {4}: dump shots_pctg: {1}, handness_pctg: {2}, handness_shots_pctg: {3}'.format(uts_now()-uts_start, round(shots_pctg, 1), round(handness_pctg, 1), round(handness_shots_pctg, 1), g_cnt))
                # dump here
                g_result_dic = _dump_it(g_result_dic, result_file)

    return g_result_dic

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

if __name__ == "__main__":

    # DEBUG mode on/off
    DEBUG = False

    MODEL_FILE = 'model_data.json'
    WEIGHT_FILE = 'xg_weighting/result-max3.0-step0.5.json'
    RESULT_FILE = 'result_finetune.json'
    TOP_NUM = 3

    STEP_SIZE = 0.1
    DEVIATION = 0.2

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # load rebound and break interval from config file
    (REBOUND_INTERVAL, BREAK_INTERVAL) = _config_load(LOGGER)

    # get model from database for file
    # XGMODEL_DIC = xgmodel_get(LOGGER)
    XGMODEL_DIC = json_load(MODEL_FILE)

    # load the dictinary created by weightener
    WEIGHT_DIC = json_load(WEIGHT_FILE)

    # get list of matches to investigate
    MATCH_LIST = match_list_get(LOGGER, 'season_id', 1, ['match_id'])

    # get global shot and goal stats
    (G_SHOTSTAT_DIC, G_GOAL_DIC) = _shotstats_get(LOGGER, MATCH_LIST)

    # set startpoint for measurement
    UTS_START = uts_now()
    G_RESULT_DIC = {'home_correct': [], 'visitor_correct': [], 'winloss_correct': [], 'result_correct': []}

    # iteratee over dictionary and take the TOPxxx
    for section in WEIGHT_DIC.keys():
        LOGGER.info('start processing section: {0}'.format(section))
        for parameter_set in WEIGHT_DIC[section][:2]:
            quantifier_dic = parameter_set['quantifier_dic']
            # calculate ranges to loop through
            loop_dic = _loopranges_get(LOGGER, quantifier_dic, DEVIATION, STEP_SIZE)
            G_RESULT_DIC = weights_finetune(LOGGER, UTS_START, RESULT_FILE, G_RESULT_DIC, G_SHOTSTAT_DIC, G_GOAL_DIC, XGMODEL_DIC, REBOUND_INTERVAL, BREAK_INTERVAL, loop_dic)
            # break
        # break
