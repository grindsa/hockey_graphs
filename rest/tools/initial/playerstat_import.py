#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import sys
import os
import json
import requests
sys.path.insert(0, '..')
from rest.functions.helper import logger_setup
from rest.functions.playerstat import playerstat_add


if __name__ == '__main__':

    DEBUG = False

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    BASE_URL = 'https://www.del.org/live-ticker/matches/'
    DATA_PATH = '../data/2019/matches'

    for ele in os.listdir(DATA_PATH):

        #URL = '{0}/{1}'.format('https://www.del.org/live-ticker/matches', ele)
        #MATCH_DIR = '{0}/{1}'.format(DATA_PATH, ele)
        #for team in ['team-stats-home.json', 'team-stats-guest.json', 'player-stats-home.json', 'player-stats-guest.json']:
        #    download_url = '{0}/{1}'.format(URL, team)
        #    file = '{0}/{1}'.format(MATCH_DIR, team)
        #    response = requests.get(download_url)
        #    with open(file, 'w', encoding='utf8') as fso:
        #        fso.write(response.text)

        MATCH_DIR = '{0}/{1}'.format(DATA_PATH, ele)
        # filter directories
        if os.path.isdir(MATCH_DIR):
            HOME_FILE = '{0}/{1}'.format(MATCH_DIR, 'player-stats-home.json')
            VISITOR_FILE = '{0}/{1}'.format(MATCH_DIR, 'player-stats-guest.json')
            home_dic = {}
            visitor_dic = {}
            try:
                if os.path.isfile(HOME_FILE):
                    with open(HOME_FILE, encoding='utf8') as stat_file_obj:
                        home_dic = json.load(stat_file_obj)
                if os.path.isfile(VISITOR_FILE):
                    with open(VISITOR_FILE, encoding='utf8') as stat_file_obj:
                        visitor_dic = json.load(stat_file_obj)
                print('add for match_id: {0}'.format(ele))
                roster_id = playerstat_add(LOGGER, 'match_id', int(ele), {'match_id': int(ele), 'home': home_dic, 'visitor': visitor_dic})
            except BaseException:
                print('ERROR at match_id: {0}'.format(ele))
