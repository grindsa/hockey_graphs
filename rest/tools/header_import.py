#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import sys
import os
import json
sys.path.insert(0, '..')
from rest.functions.helper import logger_setup
from rest.functions.gameheader import gameheader_add

if __name__ == '__main__':

    DEBUG = True

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    DATA_PATH = '../data/2019/matches'

    for ele in os.listdir(DATA_PATH):
        MATCH_DIR = '{0}/{1}'.format(DATA_PATH, ele)
        # filter directories
        if os.path.isdir(MATCH_DIR):

            HEADER_FILE = '{0}/{1}'.format(MATCH_DIR, 'game-header.json')
            if os.path.isfile(HEADER_FILE):
                with open(HEADER_FILE, encoding='utf8') as header_file_obj:
                    header_dic = json.load(header_file_obj)
                    header_id = gameheader_add(LOGGER, 'match_id', int(ele), {'match_id': int(ele), 'gameheader': header_dic})
            else:
                print('NOT FOUND!', HEADER_FILE)
