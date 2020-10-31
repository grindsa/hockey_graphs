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
from rest.functions.roster import roster_add
from rest.functions.periodevent import periodevent_add

if __name__ == '__main__':

    DEBUG = True

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    DATA_PATH = '../data/2019/matches'
    for ele in os.listdir(DATA_PATH):
        MATCH_DIR = '{0}/{1}'.format(DATA_PATH, ele)
        # filter directories
        if os.path.isdir(MATCH_DIR):
            ROSTER_FILE = '{0}/{1}'.format(MATCH_DIR, 'roster.json')

            if os.path.isfile(ROSTER_FILE):
                # print('process', ROSTER_FILE)
                with open(ROSTER_FILE, encoding='utf8') as roster_file_obj:
                    roster_dic = json.load(roster_file_obj)
                    roster_id = roster_add(LOGGER, 'match_id', int(ele), {'match_id': int(ele), 'roster': roster_dic})
                    print(roster_id)
            else:
                print('NOT FOUND!', ROSTER_FILE)
                roster_dic = {}
