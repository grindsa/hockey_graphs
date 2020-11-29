#!/usr/bin/python
# -*- coding: utf-8 -*-
""" script for initial teamsmatchstat load """
import sys
import os
import django
# we need this to load the django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
django.setup()

# import project settings
from rest.functions.helper import logger_setup
from rest.functions.teamstat import teamstat_get
from rest.functions.teammatchstat import teammatchstat_add

if __name__ == '__main__':

    DEBUG = True
    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # get list of matches
    match_list = teamstat_get(LOGGER)
    for match in match_list:
        # if match['match_id'] == 1795:
        # if match['match_id'] == 1570:
        # get matchid and add data add function
        teammatchstat_add(LOGGER, match)
