# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.functions.shot import shot_list_get, shotspermin_count, shotspermin_aggregate, shotspersec_count, shotstatus_count, shotstatus_aggregate
from rest.functions.shotcharts import shotsumchart_create, gameflowchart_create, shotstatussumchart_create
from rest.functions.shottables import shotsperiodtable_get, shotstatussumtable_get
from rest.functions.match import match_info_get
from rest.functions.periodevent import penaltyplotlines_get
from rest.functions.chartparameters import chart_color7

def matchstatistics_get(logger, request, fkey=None, fvalue=None):
    """ matchstatistics grouped by days """
    logger.debug('matchstatistics_get({0}:{1})'.format(fkey, fvalue))

    # we protect the REST and will not return anything without matchid
    if fkey:
        # we need some match_information
        matchinfo_dic = match_info_get(logger, fvalue, request.META)

        # get list of shots
        shot_list = shot_list_get(logger, fkey, fvalue, ['timestamp', 'match_shot_resutl_id', 'team_id', 'player__last_name'])
        result = []

        # create chart for shots per match
        # pylint: disable=E0602
        result.append(_gameshots_get(logger, _('Shots per minute'), request, fkey, fvalue, matchinfo_dic, shot_list))

        # create shotflowchart
        # pylint: disable=E0602
        result.append(_gameflow_get(logger, _('Gameflow'), request, fkey, fvalue, matchinfo_dic, shot_list))

        # create chart for shotstatus
        # pylint: disable=E0602
        result.append(_gameshootstatus_get(logger, _('Shots by Result'), request, fkey, fvalue, matchinfo_dic, shot_list))

    else:
        result = {'error': 'Please specify a matchid'}

    return result

def _gameflow_get(logger, title, request, fkey, fvalue, matchinfo_dic, shot_list):
    """ prepare shots per match chart """
    logger.debug('_shots_per_match_get({0}:{1})'.format(fkey, fvalue))

    shot_table = {}
    shot_chart = {}

    if shot_list:
        # get shots and goals per second
        (shotflow_dic, goal_dic) = shotspersec_count(logger, shot_list, matchinfo_dic)

        # create plotlines to be addedd to chart
        plotline_list = penaltyplotlines_get(logger, fvalue, chart_color7)

        # create the chart
        shot_chart = gameflowchart_create(logger, shotflow_dic, goal_dic, plotline_list, matchinfo_dic)

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'tabs': False
    }

    return stat_entry

def _gameshootstatus_get(logger, title, request, fkey, fvalue, matchinfo_dic, shot_list):
    """ shot status """
    logger.debug('_gameshootstatus_get({0}:{1})'.format(fkey, fvalue))

    shot_table = {}
    shot_chart = {}

    if shot_list:
        # get shots and goals per min
        (shotstatus_dic, goal_dic) = shotstatus_count(logger, shot_list, matchinfo_dic)

        # aggregate shots per min
        shotstatussum_dic = shotstatus_aggregate(logger, shotstatus_dic)

        # create chart
        shot_chart = [
            shotstatussumchart_create(logger, shotstatussum_dic, shotstatus_dic, goal_dic, 'home_team', matchinfo_dic),
            shotstatussumchart_create(logger, shotstatussum_dic, shotstatus_dic, goal_dic, 'visitor_team', matchinfo_dic),
        ]
        shot_table = [
            shotstatussumtable_get(logger, title, shotstatus_dic, 'home_team', matchinfo_dic),
            shotstatussumtable_get(logger, title, shotstatus_dic, 'visitor_team', matchinfo_dic)
        ]

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'tabs': True
    }

    return stat_entry

def _gameshots_get(logger, title, request, fkey, fvalue, matchinfo_dic, shot_list):
    """ prepare shots per match chart """
    logger.debug('_gameshots_get({0}:{1})'.format(fkey, fvalue))

    shot_table = {}
    shot_chart = {}

    if shot_list:

        # get shots and goals per min
        (shotmin_dic, goal_dic) = shotspermin_count(logger, shot_list, matchinfo_dic)

        # aggregate shots per min
        shotsum_dic = shotspermin_aggregate(logger, shotmin_dic)

        # create plotlines to be addedd to chart
        plotline_list = penaltyplotlines_get(logger, fvalue)

        shot_chart = shotsumchart_create(logger, shotsum_dic, shotmin_dic, goal_dic, plotline_list, matchinfo_dic)
        shot_table = shotsperiodtable_get(logger, title, shotmin_dic, matchinfo_dic)

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'tabs': False
    }

    return stat_entry
