#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import sys
import os
import json
sys.path.insert(0, '..')
from rest.functions.helper import logger_setup
from rest.functions.match import match_list_get, match_add
from rest.functions.player import player_list_get, player_add
from rest.functions.season import season_latest_get
from rest.functions.shot import shot_add, zone_name_get
from rest.functions.team import team_list_get, team_add

def process_match(logger, match_dic):
    """ process match dictionary """
    # add teams if not existing
    if match_dic['home_id'] not in team_list:
        team_id = team_add(logger, 'team_id', match_dic['home_id'], {'team_id': match_dic['home_id'], 'team_name': match_dic['home_name'], 'shortcut': match_dic['home_shortcut']})
        team_list.append(team_id)
    if match_dic['visitor_id'] not in team_list:
        team_id = team_add(logger, 'team_id', match_dic['visitor_id'], {'team_id': match_dic['visitor_id'], 'team_name': match_dic['visitor_name'], 'shortcut': match_dic['visitor_shortcut']})
        team_list.append(team_id)

    # add match if not existing
    if int(match_dic['id']) not in match_list:
        print('create match:', match_dic['date'], match_dic['id'], match_dic['home_id'], match_dic['visitor_id'])
        match_id = match_add(logger, 'match_id', match_dic['id'], {'match_id': match_dic['id'], 'date': match_dic['date'], 'home_team_id': match_dic['home_id'], 'visitor_team_id':  match_dic['visitor_id'], 'season_id': season_id})
        match_list.append(match_id)

    for shot in match_dic['shots']:
        # add player if not exists
        if shot['player_id'] not in player_list:
            print('create_player:', shot['player_id'], shot['first_name'], shot['last_name'], shot['jersey'])
            player_id = player_add(logger, 'player_id', shot['player_id'], {'player_id': shot['player_id'], 'first_name': shot['first_name'], 'last_name': shot['last_name'], 'jersey': shot['jersey']})
            player_list.append(player_id)

        # add shot
        zone = zone_name_get(logger, shot['coordinate_x'], shot['coordinate_y'])
        print('add_shot:', shot['id'], shot['player_id'], shot['team_id'], shot['match_shot_resutl_id'], shot['time'], shot['coordinate_x'], shot['coordinate_y'], shot['real_date'], shot['polygon'], zone)
        data_dic = {
            'shot_id': shot['id'],
            'player_id': shot['player_id'],
            'team_id': shot['team_id'],
            'match_id': match_dic['id'],
            'match_shot_resutl_id': shot['match_shot_resutl_id'],
            'timestamp': shot['time'],
            'coordinate_x': shot['coordinate_x'],
            'coordinate_y': shot['coordinate_y'],
            'real_date': shot['real_date'],
            'polygon': shot['polygon'],
            'zone': zone,
        }
        shot_id = shot_add(logger, 'shot_id', shot['id'], data_dic)

if __name__ == '__main__':

    DEBUG = True

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # IN_FILE = '../data/2019/matches'
    data_path = '../data/2019/matches'

    # get season_id
    season_id = season_latest_get(LOGGER)

    # get team_list
    team_list = team_list_get(LOGGER, None, None, ['team_id'])

    # get list of matches
    match_list = match_list_get(LOGGER, None, None, ['match_id'])
    print(match_list)
    sys.exit(0)

    # get list of players
    player_list = player_list_get(LOGGER, None, None, ['player_id'])

    ele_cnt = 0
    match_cnt = 0
    for ele in os.listdir(data_path):
        ele_cnt += 1
        match_dir = '{0}/{1}'.format(data_path, ele)
        # filter directories
        if os.path.isdir(match_dir):
            in_file = '{0}/{1}'.format(match_dir, 'shots.json')
            match_cnt += 1
            with open(in_file, encoding='utf8') as json_file:
                match_dic = json.load(json_file)['match']
                process_match(LOGGER, match_dic)

    print('counter:', ele_cnt, match_cnt)
