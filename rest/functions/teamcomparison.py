# -*- coding: utf-8 -*-
""" list of functions for team comparison """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.functions.corsi import pace_data_get, pace_updates_get, shotrates_updates_get
from rest.functions.faceoff import faceoff_overview_get, faceoffs_updates_get
from rest.functions.faceoffcharts import faceoff_overview_chart
from rest.functions.helper import mobile_check, language_get
from rest.functions.comment import comment_get
from rest.functions.pdo import pdo_breakdown_data_get, pdo_overview_data_get, breakdown_updates_get, overview_updates_get
from rest.functions.pdocharts import pdo_breakdown_chart, pdo_overview_chart
from rest.functions.season import seasonid_get
from rest.functions.shotcharts import pace_chart_get, shotrates_chart_get, shotshare_chart_get, rebound_overview_chart, break_overview_chart
# from rest.functions.bananachart import banana_chart1_create, banana_chart2_create
from rest.functions.shot import rebound_overview_get, break_overview_get, rebound_updates_get
from rest.functions.team import team_dic_get
from rest.functions.teammatchstat import teammatchstats_get
from rest.functions.teamstat import teamstat_dic_get
from rest.functions.heatmap import teamcomparison_hmdata_get, teamcomparison_updates_get
from rest.functions.heatmapcharts import teamcomparison_chart_get

def teamcomparison_get(logger, request, fkey=None, fvalue=None):
    """ matchstatistics grouped by days """
    logger.debug('teamcomparison_get({0}:{1})'.format(fkey, fvalue))

    (_fkey, season_id) = seasonid_get(logger, request)

    # get teams and matchstatistics
    teams_dic = team_dic_get(logger, request.META)
    matchstat_list = teammatchstats_get(logger, 'match__season_id', season_id)

    ismobile = mobile_check(logger, request)
    language = language_get(logger, request)

    # stacked stats per team
    teamstat_dic = teamstat_dic_get(logger, matchstat_list)

    result = []

    result.append(_teamcomparison_heatmap_get(logger, ismobile, language, teamstat_dic, teams_dic))

    # create PDO breakdown chart
    result.extend(_pdo_breakdown_get(logger, ismobile, teamstat_dic, teams_dic))

    # 5on5 shotcharts
    result.extend(_5v5_pace_get(logger, ismobile, teamstat_dic, teams_dic))

    # faceoff wins
    result.append(_faceoff_pctg_get(logger, ismobile, teamstat_dic, teams_dic))

    # rebound efficentcy
    result.append(_rebound_pctg_get(logger, ismobile, teamstat_dic, teams_dic))

    # rebound efficentcy
    result.append(_break_pctg_get(logger, ismobile, teamstat_dic, teams_dic))

    return result

def _teamcomparison_heatmap_get(logger, ismobile, language, teamstat_dic, teams_dic):
    """ build structure for pace chart """
    logger.debug('_5v5_pace_get()')

    heatmap_data = teamcomparison_hmdata_get(logger, ismobile, teamstat_dic, teams_dic)

    # team heatmap
    # pylint: disable=E0602
    title = _('Team heatmaps')
    subtitle = _('A league-wide, at-a-glance look on Team performance. Red is bad, blue is good')

    stat_entry = {
        'title': title,
        'chart':  teamcomparison_chart_get(logger, title, subtitle, ismobile, heatmap_data[len(heatmap_data.keys())]),
        'updates': teamcomparison_updates_get(logger, title, ismobile, heatmap_data),
        'comment': comment_get(logger, 'name', 'teamcomparison_heatmap', [language])
    }

    return stat_entry

def _5v5_pace_get(logger, ismobile, teamstat_dic, teams_dic):
    """ build structure for pace chart """
    logger.debug('_5v5_pace_get()')

    # create empty list returning data
    stat_entry_list = []

    # two different data series
    (pace_dic, shotrates_dic, shotshares_dic) = pace_data_get(logger, ismobile, teamstat_dic, teams_dic)

    # 5v5 pace chart
    # pylint: disable=E0602
    title = _('5v5 "Pace" (Cf/60 + Ca/60)')
    subtitle = _('Combined shots on own and other goal during 5-on-5 play (on 60min adjusted)')
    stat_entry = {
        'title': title,
        'chart':  pace_chart_get(logger, title, subtitle, ismobile, pace_dic[len(pace_dic.keys())]),
        'updates': pace_updates_get(logger, pace_dic, title)
    }
    stat_entry_list.append(stat_entry)

    # shotrates
    title = _('5v5 Shot rates Cf/60 vs Ca/60')
    subtitle = _('Shots generated during 5-on-5 play (on 60min adjusted)')
    stat_entry = {
        'title': title,
        'chart':  shotrates_chart_get(logger, title, subtitle, ismobile, shotrates_dic[len(shotrates_dic.keys())]),
        'updates': shotrates_updates_get(logger, shotrates_dic)
    }
    stat_entry_list.append(stat_entry)

    # shotshare
    # pylint: disable=E0602
    title = _('5v5 Shot share C/60')
    subtitle = _('Each team’s share of shots taken in their games')
    stat_entry = {
        'title': title,
        'chart':  shotshare_chart_get(logger, title, subtitle, subtitle, shotshares_dic[len(shotshares_dic.keys())]),
        'updates': pace_updates_get(logger, shotshares_dic, title)
    }
    stat_entry_list.append(stat_entry)


    return stat_entry_list

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
    subtitle = _('5v5 shooting percentage and save percentage')
    stat_entry = {
        'title': title,
        'chart':  pdo_overview_chart(logger, title, subtitle, ismobile, overview_dic[len(overview_dic.keys())]),
        'updates': overview_updates_get(logger, overview_dic),
    }
    stat_entry_list.append(stat_entry)

    # pdo breakdown chart
    # pylint: disable=E0602
    title = _('PDO breakdown')
    subtitle = _('luck and fun across the league')
    stat_entry = {
        'title': title,
        'chart':  pdo_breakdown_chart(logger, title, subtitle, ismobile, breakdown_dic[len(breakdown_dic.keys())]),
        'updates': breakdown_updates_get(logger, breakdown_dic),
    }
    stat_entry_list.append(stat_entry)

    return stat_entry_list

def _faceoff_pctg_get(logger, ismobile, teamstat_dic, teams_dic):
    """ faceoff wins """
    logger.debug('_faceoff_pctg_get()')

    faceoff_dic = faceoff_overview_get(logger, ismobile, teamstat_dic, teams_dic)

    # pylint: disable=E0602
    title = _('Faceoff win rate')
    stat_entry = {
        'title': title,
        'chart': faceoff_overview_chart(logger, title, ismobile, faceoff_dic[len(faceoff_dic.keys())]),
        'updates': faceoffs_updates_get(logger, title, faceoff_dic)
    }

    return stat_entry

def _rebound_pctg_get(logger, ismobile, teamstat_dic, teams_dic):
    """ faceoff wins """
    logger.debug('_rebound_pctg_get()')

    rebound_dic = rebound_overview_get(logger, ismobile, teamstat_dic, teams_dic)

    # pylint: disable=E0602
    title = _('Rebound success rate')
    subtitle = _('Percentage of rebounds leading to a goal')
    stat_entry = {
        'title': title,
        'chart': rebound_overview_chart(logger, title, subtitle, ismobile, rebound_dic[len(rebound_dic.keys())]),
        'updates': rebound_updates_get(logger, title, rebound_dic, 'goals_rebound_for_pctg', 'goals_rebound_against_pctg'),
    }

    return stat_entry

def _break_pctg_get(logger, ismobile, teamstat_dic, teams_dic):
    """ faceoff wins """
    logger.debug('_break_pctg_get()')

    break_dic = break_overview_get(logger, ismobile, teamstat_dic, teams_dic)

    # pylint: disable=E0602
    title = _('Break success rate')
    subtitle = _('Percentage of breaks leading to a goal')
    stat_entry = {
        'title': title,
        'chart': break_overview_chart(logger, title, subtitle, ismobile, break_dic[len(break_dic.keys())]),
        'updates': rebound_updates_get(logger, title, break_dic, 'goals_break_for_pctg', 'goals_break_against_pctg'),
    }

    return stat_entry
