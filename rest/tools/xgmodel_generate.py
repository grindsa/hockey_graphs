#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import xg modelstats to database """
# pylint: disable=E0401, C0413
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from rest.functions.helper import logger_setup, json_store
from rest.functions.player import player_dic_get
from rest.functions.shot import shot_list_get
from rest.functions.xg import model_build, pctg_calculate, xg_add

if __name__ == "__main__":

    # within this interval two shots from same team will be assumed as rebound
    REBOUND_INTERVAL = 3
    # within this interval two shots from different teams will be assumed as break
    BREAK_INTERVAL = 7

    # DEBUG mode on/off
    DEBUG = True

    # get season_id to analyse
    SEASON_ID = 1

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # get list of shots from 2019/2020 season - they will be used as base for our model
    # MATCH_LIST = match_list_get(LOGGER, 'season_id', SEASON_ID, ['match_id'])
    VLIST = ['shot_id', 'match_id', 'match_shot_resutl_id', 'player_id', 'team_id', 'coordinate_x', 'coordinate_y', 'match__home_team_id', 'match__visitor_team_id', 'timestamp']
    SHOT_LIST = shot_list_get(LOGGER, 'match__season_id', SEASON_ID, VLIST)

    # get player_dictionary to determine left/right hand player
    PLAYER_DIC = player_dic_get(LOGGER)

    # build the model
    MODEL_DIC = model_build(LOGGER, SHOT_LIST, PLAYER_DIC, REBOUND_INTERVAL, BREAK_INTERVAL)
    # add percentage values to model
    MODEL_DIC = pctg_calculate(MODEL_DIC)

    result = xg_add(LOGGER, 'id', 1, {'xg_data': MODEL_DIC})
    print(result)
    # json_store('model_data.json', MODEL_DIC)
