#!/usr/bin/python
# -*- coding: utf-8 -*-
""" this is just a wrapper to help in development """
import sys
import os
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()

from rest.functions.helper import logger_setup
from rest.functions.matchstatistics import matchstatistics_get
from rest.functions.teamcomparison import teamcomparison_get
from rest.functions.playerstatistics import playerstatistics_fetch
from delapphelper import DelAppHelper
import gettext

en = gettext.translation('django', localedir='locale', languages=['en'])
en.install()


class Request:
    pass

if __name__ == '__main__':

    DEBUG = True
    LOGGER = logger_setup(DEBUG)

    request = Request()
    request.META = {'foo': 'bar'}

    SEASON_PK = 3
    PLAYER_PK = 6

    fkey = 'match_id'
    fvalue = 2584 # 2455 # 2206
    # game_id = 2578

    # result = playerstatistics_fetch(LOGGER, request, SEASON_PK, PLAYER_PK)
    result = matchstatistics_get(LOGGER, request, fkey, fvalue)
    # result = teamcomparison_get(LOGGER, request, fkey, fvalue)
    # from pprint import pprint
    # pprint(result)

    #team_name = 'EBB'
    #season_year = '2022'
    #league = 1
    #team_id = 2

    #with DelAppHelper(None, DEBUG) as del_app_helper:
    #    tournament_dic = del_app_helper.tournamentid_get()
    #    # result = del_app_helper.teammembers_get(team_name)
    #    result = del_app_helper.teamplayers_get(season_year, team_id, league)

        # result = del_app_helper.gamesituations_get(game_id)

    #from pprint import pprint
    #pprint(result)
