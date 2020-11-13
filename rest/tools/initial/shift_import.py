#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import sys
import os
import json
sys.path.insert(0, '..')
from rest.functions.helper import logger_setup
from rest.functions.shift import shift_add
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
            SHIFT_FILE = '{0}/{1}'.format(MATCH_DIR, 'shifts.json')
            if os.path.isfile(SHIFT_FILE):
                #print('process', shift_file)
                with open(SHIFT_FILE, encoding='utf8') as shift_file_obj:
                    shift_dic = json.load(shift_file_obj)
                    shift_id = shift_add(LOGGER, 'match_id', int(ele), {'match_id': int(ele), 'shift': shift_dic})
            else:
                print('NOT FOUND!', SHIFT_FILE)
                shift_dic = {}

            EVENT_FILE = '{0}/{1}'.format(MATCH_DIR, 'period-events.json')
            if os.path.isfile(EVENT_FILE):
                with open(EVENT_FILE, encoding='utf8') as event_file_obj:
                    event_dic = json.load(event_file_obj)
                    event_id = periodevent_add(LOGGER, 'match_id', int(ele), {'match_id': int(ele), 'period_event': event_dic})
            else:
                print('NOT FOUND!', EVENT_FILE)
