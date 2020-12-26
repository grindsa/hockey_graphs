#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" calculate xg values """
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from rest.functions.helper import config_load, logger_setup
from rest.functions.shot import shot_list_get
from rest.functions.xg import xgmodel_get, shotlist_process

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
    DEBUG = True

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # load rebound and break interval from config file
    (REBOUND_INTERVAL, BREAK_INTERVAL) = _config_load(LOGGER)

    # get model from database
    XGMODEL_DIC = xgmodel_get(LOGGER)

    MATCH_LIST = [1820]

    # quantifier dictionary
    QUANTIFIER_DIC = {
        'shot_pctg': 1,
        'handness_pctg': 1.5,
        'handnesshot_pctg': 1.0,
        'rb_pctg': 1,
        'rbshoot_pctg': 1.5,
        'br_pctg': 1,
        'brshoot_pctg': 1.5,
    }

    # define value list for match specific shot_dictionary
    VLIST = ['shot_id', 'match_id', 'match_shot_resutl_id', 'player_id', 'player__first_name', 'player__last_name', 'player__jersey', 'player__stick', 'team_id', 'coordinate_x', 'coordinate_y', 'match__home_team_id', 'match__visitor_team_id', 'timestamp']

    for match_id in MATCH_LIST:
        # get list of shots
        shot_list = shot_list_get(LOGGER, 'match_id', match_id, VLIST)

        # convert shots and goals into structure we can process later on
        # we also need the XGMODEL_DIC to check if we have the shotcoordinates in our structure
        (shotstat_dic, goal_dic) = shotlist_process(LOGGER, shot_list, XGMODEL_DIC, REBOUND_INTERVAL, BREAK_INTERVAL)

        from pprint import pprint
        pprint(shotstat_dic)

        # lets apply the magic algorithm to estimate xGF
        # playerxgf_dic = xgf_calculate(shotstat_dic, QUANTIFIER_DIC)
