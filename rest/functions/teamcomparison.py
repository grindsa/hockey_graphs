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
from rest.functions.bananachart import banana_chart1_create, banana_chart2_create
from rest.functions.team import team_dic_get
from rest.functions.teammatchstat import teammatchstats_get
from rest.functions.teamstat import teamstat_dic_get
from rest.functions.pdo import pdo_breakdown_data_get, pdo_overview_data_get, breakdown_updates_get, overview_updates_get
from rest.functions.pdocharts import pdo_breakdown_chart, pdo_overview_chart

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

    # result.append(banana_chart1_create(logger, 'foo1'))
    # result.append(banana_chart2_create(logger, 'foo2'))

    return result

def _pdo_breakdown_get(logger, ismobile, teamstat_dic, teams_dic):
    """ pdo breakdown """
    logger.debug('_pdo_breakdown_get()')

    # get data for breakdown chart
    breakdown_dic = pdo_breakdown_data_get(logger, ismobile, teamstat_dic, teams_dic)
    # we need the breakdown data as input thus it must run first
    overview_dic = pdo_overview_data_get(logger, ismobile, breakdown_dic)

    stat_entry_list = []

    # pdo overview
    title =  _('PDO overview')
    stat_entry = {
        'title': title,
        'chart':  pdo_overview_chart(logger, title, overview_dic[len(overview_dic.keys())]),
        'updates': overview_updates_get(logger, overview_dic),
    }
    stat_entry_list.append(stat_entry)

    # pdo breakdown chart
    title =  _('PDO breakdown')

    stat_entry = {
        'title': title,
        'chart':  pdo_breakdown_chart(logger, title, breakdown_dic[len(breakdown_dic.keys())]),
        'updates': breakdown_updates_get(logger, breakdown_dic),
    }
    stat_entry_list.append(stat_entry)


    return stat_entry_list
