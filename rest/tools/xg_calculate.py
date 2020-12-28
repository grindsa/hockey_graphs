#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" calculate xg values """
import os
import sys
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from rest.functions.helper import config_load, logger_setup, json_load
from rest.functions.shot import shot_list_get
from rest.functions.match import match_info_get, match_list_get
from rest.functions.xg import xgmodel_get, shotlist_process, xgf_calculate, xgscore_get

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='xg_calculate.py - xG calculator')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-m', '--model_file', help='file containing the model data', default=None)
    parser.add_argument('-q', '--quantifier_file', help='file containing weights for calculation', default=None)
    args = parser.parse_args()

    debug = args.debug
    model_file = args.model_file
    quantifier_file = args.quantifier_file

    if not model_file:
        print('specify model file with "-m" parameter')
        sys.exit(0)

    if not quantifier_file:
        print('specify quantifier file with "-q" parameter')
        sys.exit(0)

    return(debug, model_file, quantifier_file)

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

if __name__ == "__main__":

    # get commandline arguments
    (DEBUG, MODEL_FILE, QUANTIFIER_FILE) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # load rebound and break interval from config file
    (REBOUND_INTERVAL, BREAK_INTERVAL) = _config_load(LOGGER)

    # get model from database
    # XGMODEL_DIC = xgmodel_get(LOGGER)
    XGMODEL_DIC = json_load(MODEL_FILE)

    # quantifier dictionary
    QUANTIFIER_DIC = json_load(QUANTIFIER_FILE)

    # get list of matches to investigate
    MATCH_LIST = match_list_get(LOGGER, 'season_id', 1, ['match_id'])
    # MATCH_LIST = [1767]

    # define value list for match specific shot_dictionary
    VLIST = ['shot_id', 'match_id', 'match_shot_resutl_id', 'player_id', 'player__first_name', 'player__last_name', 'player__jersey', 'player__stick', 'team_id', 'coordinate_x', 'coordinate_y', 'match__home_team_id', 'match__visitor_team_id', 'timestamp']

    for match_id in MATCH_LIST:

        match_dic = match_info_get(LOGGER, match_id, None, ['date', 'home_team__shortcut', 'visitor_team__shortcut', 'result'])

        # get list of shots
        shot_list = shot_list_get(LOGGER, 'match_id', match_id, VLIST)

        # convert shots and goals into structure we can process later on
        # we also need the XGMODEL_DIC to check if we have the shotcoordinates in our structure
        (shotstat_dic, goal_dic) = shotlist_process(LOGGER, shot_list, XGMODEL_DIC, REBOUND_INTERVAL, BREAK_INTERVAL)

        # lets apply the magic algorithm to estimate xGF
        playerxgf_dic = xgf_calculate(LOGGER, shotstat_dic, QUANTIFIER_DIC)

        xgf_dic = xgscore_get(LOGGER, playerxgf_dic)

        match_info = '{0}: {1} vs {2} ({3})'.format(match_dic['date'], match_dic['home_team__shortcut'], match_dic['visitor_team__shortcut'], match_dic['result'])
        result = match_dic['result']
        score = '{0}:{1}'.format(len(goal_dic['home']), len(goal_dic['visitor']))
        xg_score = '{0}:{1}'.format(xgf_dic['home'], xgf_dic['visitor'])

        print('{0} {1}|{2}'.format(match_info, score, xg_score))




        # from pprint import pprint
        # pprint(playerxgf_dic)
