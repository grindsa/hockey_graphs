# -*- coding: utf-8 -*-
""" helper functions """
import logging
from rest.models import Match, Player, Season, Team

def testdata_load(debug=False):
    """ load testdata for unittests """
    Season.objects.create(name="Season-1")
    Season.objects.create(name="Season-2")
    Team.objects.create(team_id=1, team_name="Team-1", shortcut="T1")
    Team.objects.create(team_id=2, team_name="Team-2", shortcut="T2")
    Match.objects.create(match_id=1, season_id=1, date="2020-12-01", date_uts=1606807800, home_team_id=1, visitor_team_id=2, result='2:1')
    Match.objects.create(match_id=2, season_id=1, date="2020-12-02", date_uts=1606894200, home_team_id=2, visitor_team_id=1, result='1:2')
    Player.objects.create(player_id=1, first_name="first_name_1", last_name="last_name_1", jersey=1)
    Player.objects.create(player_id=2, first_name="first_name_2", last_name="last_name_2", jersey=2)

def logger_setup(debug):
    """ setup logger """
    if debug:
        log_mode = logging.DEBUG
    else:
        log_mode = logging.INFO

    # log_formet = '%(message)s'
    log_format = '%(asctime)s - hockey_graphs - %(levelname)s - %(message)s'
    logging.basicConfig(
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        level=log_mode)
    logger = logging.getLogger('hockey_graph')
    return logger
