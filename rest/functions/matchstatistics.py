# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.functions.shot import shot_list_get, shotspermin_count, shotspermin_aggregate, shotspersec_count, gameflow_aggregate
from rest.functions.shotcharts import shotsumchart_create, gameflowchart_create
from rest.functions.shottables import shotsperiodtable_get
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
        result = []

        # ceate chart for shots per match
        # result.append(_shotspermatch_get(logger, _('Shots per minute'), request, fkey, fvalue, matchinfo_dic))

        # create shotflowchart
        result.append(_gameflow_get(logger, _('Gameflow'), request, fkey, fvalue, matchinfo_dic))

    else:
        result = {'error': 'Please specify a matchid'}

    return result

def _gameflow_get(logger, title, request, fkey, fvalue, matchinfo_dic):
    """ prepare shots per match chart """
    logger.debug('_shots_per_match_get({0}:{1})'.format(fkey, fvalue))

    # list of shots
    shot_list = shot_list_get(logger, fkey, fvalue, ['timestamp', 'match_shot_resutl_id', 'team_id', 'player__last_name'])
    shot_table = {}
    shot_chart = {}

    if shot_list:
        # get shots and goals per second
        (shot_flow_dic, goal_dic) = shotspersec_count(logger, shot_list, matchinfo_dic)

        # create plotlines to be addedd to chart
        plotline_list = penaltyplotlines_get(logger, fvalue, chart_color7)

        # create the chart
        shot_chart = gameflowchart_create(logger, shot_flow_dic, goal_dic, plotline_list, matchinfo_dic)

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'display': True,
        'tabs': False
    }

    return stat_entry


def _shotspermatch_get(logger, title, request, fkey, fvalue, matchinfo_dic):
    """ prepare shots per match chart """
    logger.debug('_shots_per_match_get({0}:{1})'.format(fkey, fvalue))

    # list of shots
    shot_list = shot_list_get(logger, fkey, fvalue, ['timestamp', 'match_shot_resutl_id', 'team_id', 'player__last_name'])
    shot_table = {}
    shot_chart = {}

    if shot_list:

        # get shots and goals per min
        (shot_min_dic, goal_dic) = shotspermin_count(logger, shot_list, matchinfo_dic)

        # aggregate shots per min
        shot_sum_dic = shotspermin_aggregate(logger, shot_min_dic)

        # create plotlines to be addedd to chart
        plotline_list = penaltyplotlines_get(logger, fvalue)

        shot_chart = shotsumchart_create(logger, shot_sum_dic, shot_min_dic, goal_dic, plotline_list, matchinfo_dic)
        shot_table = shotsperiodtable_get(logger, title, shot_min_dic, matchinfo_dic)

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'display': True,
        'tabs': False
    }

    return stat_entry
