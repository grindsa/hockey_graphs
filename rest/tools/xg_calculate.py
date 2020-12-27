#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" calculate xg values """
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from rest.functions.helper import config_load, logger_setup, json_load
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
    # MATCH_LIST = [1767]

    # quantifier dictionary
    QUANTIFIER_DIC = {
        'shots_pctg': 1,
        'handness_pctg': 1.5,
        'handness_shots_pctg': 1.0,
        'rb_pctg': 1,
        'rb_shots_pctg': 1.5,
        'br_pctg': 1,
        'br_shots_pctg': 1.5,
    }

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
