#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import sys
import os
import json
sys.path.insert(0, '..')
from rest.functions.player import player_list_get, player_add
from rest.functions.shift import shift_add
from rest.functions.team import team_list_get, team_add

def process_match(match_id, shift_dic):
    """ process match dictionary """

    for shift in shift_dic:
        # add match if not existing
        if int(shift['team']['id']) not in team_list:
            print('create team:', shift['team']['id'], shift['team']['name'])
            team_id = team_add('team_id', shift['team']['id'], {'team_id': shift['team']['id'], 'team_name': shift['team']['name']})
            team_list.append(team_id)

        # add player if not exists
        if shift['player']['id'] not in player_list:
            print('create_player:', shift['player']['id'])

        # add shift
        print('add_shift:', shift['id'], shift['player']['id'], shift['team']['id'], shift['startTime']['time'], shift['startTime']['realtime'], shift['endTime']['time'], shift['endTime']['realtime'])
        data_dic = {
            'shift_id': shift['id'],
            'player_id': shift['player']['id'],
            'team_id': shift['team']['id'],
            'match_id': match_id,
            'starttime_sec': shift['startTime']['time'],
            'starttime_realtime': shift['startTime']['realtime'],
            'endtime_sec': shift['endTime']['time'],
            'endtime_realtime': shift['endTime']['realtime']
        }
        shift_id = shift_add('shift_id', shift['id'], data_dic)


if __name__ == '__main__':

    # IN_FILE = '../data/2019/matches'
    data_path = '../data/2019/matches'

    # get team_list
    team_list = team_list_get(None, None, ['team_id'])

    # get list of players
    player_list = player_list_get(None, None, ['player_id'])

    ele_cnt = 0
    match_cnt = 0
    for ele in os.listdir(data_path):
        ele_cnt += 1
        match_dir = '{0}/{1}'.format(data_path, ele)
        # filter directories
        if os.path.isdir(match_dir):
            in_file = '{0}/{1}'.format(match_dir, 'shifts.json')
            match_cnt += 1
            with open(in_file, encoding='utf8') as json_file:
                match_dic = json.load(json_file)
                process_match(ele, match_dic)
        sys.exit(0)

    print('counter:', ele_cnt, match_cnt)
