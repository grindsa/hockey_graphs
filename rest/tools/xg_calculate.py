#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" calculate xg values """
import os
import sys
import argparse
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

# pylint: disable=E0401, C0413
from rest.functions.corsi import gameshots5v5_get, goals5v5_get
from rest.functions.helper import config_load, logger_setup, json_load
from rest.functions.match import match_info_get, match_list_get
from rest.functions.periodevent import periodevent_get
from rest.functions.shift import shift_get
from rest.functions.shot import shot_list_get
from rest.functions.xg import xgmodel_get, shotlist_process, xgf_calculate, xgscore_get

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='xg_calculate.py - xG calculator')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-m', '--model_file', help='file containing the model data', default=None)
    parser.add_argument('-q', '--quantifier_file', help='file containing weights for calculation', default=None)
    parser.add_argument('-o', '--output_file', help='report in markdown format')
    args = parser.parse_args()

    debug = args.debug
    model_file = args.model_file
    quantifier_file = args.quantifier_file
    output_file = args.output_file

    if not model_file:
        print('specify model file with "-m" parameter')
        sys.exit(0)

    if not quantifier_file:
        print('specify quantifier file with "-q" parameter')
        sys.exit(0)

    return(debug, model_file, quantifier_file, output_file)

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

def _markdown_write(logger, output_file, output_list, quantifier_dic):
    """ write a report """
    logger.debug('_markdown_write()')

    with open(output_file, 'w') as out_file:
        out_file.write('# xG report\n')
        out_file.write('## Parameter weighting\n')
        out_file.write('```json\n')
        json.dump(quantifier_dic, out_file, ensure_ascii=False, indent=4)
        out_file.write('\n```\n')

        out_file.write('## Match list\n')
        out_file.write('| date | home | visitor | result  | score  | xGscore  |\n')
        out_file.write('| :--- | :--- | :------ | :-----: | :----: | :------: |\n')

        for match in output_list:
            out_file.write('| {0} | {1} | {2} | {3} | {4} | {5} |\n'.format(match['date'], match['home'], match['visitor'], match['result'], match['score'], match['xg_score']))


if __name__ == "__main__":

    # get commandline arguments
    (DEBUG, MODEL_FILE, QUANTIFIER_FILE, OUTPUT_FILE) = arg_parse()

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
    MATCH_LIST = match_list_get(LOGGER, 'season_id', 3, ['match_id'])
    # MATCH_LIST = [1767]

    # define value list for match specific shot_dictionary
    VLIST = ['shot_id', 'match_id', 'match_shot_resutl_id', 'real_date', 'player_id', 'player__first_name', 'player__last_name', 'player__jersey', 'player__stick', 'team_id', 'coordinate_x', 'coordinate_y', 'match__home_team_id', 'match__visitor_team_id', 'timestamp']

    # empty output listg
    OUTPUT_LIST = []

    for match_id in MATCH_LIST:

        match_dic = match_info_get(LOGGER, match_id, None, ['date', 'home_team_id', 'home_team__shortcut', 'visitor_team_id', 'visitor_team__shortcut', 'result'])

        # get list of shots
        shot_list = shot_list_get(LOGGER, 'match_id', match_id, VLIST)
        shift_list = shift_get(logger, 'match_id', match_id, ['shift'])
        periodevent_list = periodevent_get(logger, 'match_id', match_id, ['period_event'])

        # get corsi statistics
        (shots_for_5v5, shots_against_5v5, shots_ongoal_for_5v5, shots_ongoal_against_5v5, shot_list_5v5) = gameshots5v5_get(LOGGER, match_id, match_dic, 'foo', shot_list, shift_list, periodevent_list)

        # 5v5 goals from periodevents
        goals5v5_dic = goals5v5_get(LOGGER, match_id, match_dic)

        # convert shots and goals into structure we can process later on
        # we also need the XGMODEL_DIC to check if we have the shotcoordinates in our structure
        (shotstat_dic, goal_dic) = shotlist_process(LOGGER, shot_list_5v5, XGMODEL_DIC, REBOUND_INTERVAL, BREAK_INTERVAL)

        # lets apply the magic algorithm to estimate xGF
        playerxgf_dic = xgf_calculate(LOGGER, shotstat_dic, QUANTIFIER_DIC)

        xgf_dic = xgscore_get(LOGGER, playerxgf_dic)

        MATCH_INFO = '{0}: {1} vs {2} ({3})'.format(match_dic['date'], match_dic['home_team__shortcut'], match_dic['visitor_team__shortcut'], match_dic['result'])
        result = match_dic['result']
        SCORE = '{0}:{1}'.format(goals5v5_dic['home'], goals5v5_dic['visitor'])
        XG_SCORE = '{0}:{1}'.format(xgf_dic['home'], xgf_dic['visitor'])

        if OUTPUT_FILE:
            # create list of dictionaries in case we have to write a output file
            OUTPUT_LIST.append({'date': match_dic['date'], 'home': match_dic['home_team__shortcut'], 'visitor': match_dic['visitor_team__shortcut'], 'result': match_dic['result'], 'score': SCORE, 'xg_score': XG_SCORE})

        print('{0} {1}|{2}'.format(MATCH_INFO, SCORE, XG_SCORE))

    if OUTPUT_FILE:
        _markdown_write(LOGGER, OUTPUT_FILE, OUTPUT_LIST, QUANTIFIER_DIC)
