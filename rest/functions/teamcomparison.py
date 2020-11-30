# -*- coding: utf-8 -*-
""" list of functions for team comparison """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.functions.helper import mobile_check
from rest.functions.season import seasonid_get
# from rest.functions.bananachart import banana_chart1_create, banana_chart2_create
from rest.functions.team import team_dic_get
from rest.functions.teammatchstat import teammatchstats_get
from rest.functions.teamstat import teamstat_dic_get
from rest.functions.pdo import pdo_breakdown_data_get, pdo_overview_data_get, breakdown_updates_get, overview_updates_get
from rest.functions.pdocharts import pdo_breakdown_chart, pdo_overview_chart
from rest.functions.corsi import pace_data_get, pace_updates_get
from rest.functions.shotcharts import pace_chart_get

def teamcomparison_get(logger, request, fkey=None, fvalue=None):
    """ matchstatistics grouped by days """
    logger.debug('teamcomparison_get({0}:{1})'.format(fkey, fvalue))

    (_fkey, season_id) = seasonid_get(logger, request)

    # get teams and matchstatistics
    teams_dic = team_dic_get(logger, request.META)
    matchstat_list = teammatchstats_get(logger, 'match__season_id', season_id)

    ismobile = mobile_check(logger, request)

    # stacked stats per team
    teamstat_dic = teamstat_dic_get(logger, matchstat_list)

    result = []

    # create PDO breakdown chart
    # pylint: disable=E0602
    result.extend(_pdo_breakdown_get(logger, ismobile, teamstat_dic, teams_dic))

    # pylint: disable=E0602
    result.append(_5v5_pace_get(logger, _('5v5 Pace (CF60 + CA60)'), ismobile, teamstat_dic, teams_dic))

    return result

def _5v5_pace_get(logger, title, ismobile, teamstat_dic, teams_dic):
    """ build structure for pace chart """
    logger.debug('_5v5_pace_get()')

    pace_dic = pace_data_get(logger, ismobile, teamstat_dic, teams_dic)

    stat_entry = {
        'title': title,
        'chart':  pace_chart_get(logger, title, pace_dic[len(pace_dic.keys())]),
        'updates': pace_updates_get(logger, pace_dic)
    }

    return stat_entry

def _pdo_breakdown_get(logger, ismobile, teamstat_dic, teams_dic):
    """ pdo breakdown """
    logger.debug('_pdo_breakdown_get()')

    # get data for breakdown chart
    breakdown_dic = pdo_breakdown_data_get(logger, ismobile, teamstat_dic, teams_dic)
    # we need the breakdown data as input thus it must run first
    overview_dic = pdo_overview_data_get(logger, ismobile, breakdown_dic)

    stat_entry_list = []

    # pdo overview
    # pylint: disable=E0602
    title = _('PDO overview')
    stat_entry = {
        'title': title,
        'chart':  pdo_overview_chart(logger, title, overview_dic[len(overview_dic.keys())]),
        'updates': overview_updates_get(logger, overview_dic),
    }
    stat_entry_list.append(stat_entry)

    # pdo breakdown chart
    # pylint: disable=E0602
    title = _('PDO breakdown')

    stat_entry = {
        'title': title,
        'chart':  pdo_breakdown_chart(logger, title, breakdown_dic[len(breakdown_dic.keys())]),
        'updates': breakdown_updates_get(logger, breakdown_dic),
    }
    stat_entry_list.append(stat_entry)


    return stat_entry_list
