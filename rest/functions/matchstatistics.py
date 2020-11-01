# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.functions.corsi import gamecorsi_get
from rest.functions.shot import shot_list_get, shotspermin_count, shotspermin_aggregate, shotspersec_count, shotstatus_count, shotstatus_aggregate, shotsperzone_count, shotsperzone_aggregate, shotcoordinates_get
from rest.functions.shotcharts import shotsumchart_create, gameflowchart_create, shotstatussumchart_create, shotmapchart_create, gamecorsichart_create, gamecorsippctgchart_create, puckpossessionchart_create
from rest.functions.shottables import shotsperiodtable_get, shotstatussumtable_get, shotzonetable_get, gamecorsi_table
from rest.functions.match import match_info_get
from rest.functions.shift import shift_get
from rest.functions.roster import roster_get
from rest.functions.periodevent import periodevent_get, penaltyplotlines_get
from rest.functions.chartparameters import chart_color7
from rest.functions.helper import url_build

def matchstatistics_get(logger, request, fkey=None, fvalue=None):
    """ matchstatistics grouped by days """
    logger.debug('matchstatistics_get({0}:{1})'.format(fkey, fvalue))

    # we protect the REST and will not return anything without matchid
    if fkey:
        # we need some match_information
        matchinfo_dic = match_info_get(logger, fvalue, request.META)

        # get list of shots
        shot_list = shot_list_get(logger, fkey, fvalue, ['timestamp', 'match_shot_resutl_id', 'team_id', 'player__first_name', 'player__last_name', 'zone', 'coordinate_x', 'coordinate_y', 'player__jersey'])

        # get list of shifts
        shift_list = shift_get(logger, fkey, fvalue, ['shift'])

        # get period events
        periodevent_list = periodevent_get(logger, fkey, fvalue, ['period_event'])

        # get rosters
        roster_list = roster_get(logger, fkey, fvalue, ['roster'])

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

        # create shotzone chart
        # pylint: disable=E0602
        result.append(_gamezoneshots_get(logger, _('Shots per Zone'), request, fkey, fvalue, matchinfo_dic, shot_list))

        # shotmap
        # pylint: disable=E0602
        result.append(_gameshotmap_get(logger, _('Game Shotmap'), request, fkey, fvalue, matchinfo_dic, shot_list))

        # player corsi
        # pylint: disable=E0602
        result.extend(_gamecorsi_get(logger, request, fkey, fvalue, matchinfo_dic, shot_list, shift_list, periodevent_list, roster_list))

        # puck possession
        # pylint: disable=E0602
        result.append(_gamepuckpossession_get(logger, _('Puck possession'), request, fkey, fvalue, matchinfo_dic, shot_list))

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
        plotline_list = penaltyplotlines_get(logger, fkey, fvalue, chart_color7)

        # create the chart
        shot_chart = gameflowchart_create(logger, shotflow_dic, goal_dic, plotline_list, matchinfo_dic)

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'tabs': False
    }

    return stat_entry

def _gamepuckpossession_get(logger, title, request, fkey, fvalue, matchinfo_dic, shot_list):
    """ create chart for puck possession """
    logger.debug('_gamepuckpossession_get({0}:{1})'.format(fkey, fvalue))

    shot_table = {}
    shot_chart = {}

    if shot_list:

        # get shots and goals per min
        (shotmin_dic, goal_dic) = shotspermin_count(logger, shot_list, matchinfo_dic)

        # aggregate shots per min
        shotsum_dic = shotspermin_aggregate(logger, shotmin_dic)

        shot_chart = puckpossessionchart_create(logger, shotsum_dic, goal_dic, matchinfo_dic)
        # pylint: disable=E0602
        shot_table = shotsperiodtable_get(logger, _('Shots per period'), shotmin_dic, matchinfo_dic)

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
        plotline_list = penaltyplotlines_get(logger, fkey, fvalue)

        shot_chart = shotsumchart_create(logger, shotsum_dic, shotmin_dic, goal_dic, plotline_list, matchinfo_dic)
        # pylint: disable=E0602
        shot_table = shotsperiodtable_get(logger, _('Shots per period'), shotmin_dic, matchinfo_dic)

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'tabs': False
    }

    return stat_entry

def _gamezoneshots_get(logger, title, request, fkey, fvalue, matchinfo_dic, shot_list):
    """ shots per zone """
    logger.debug('_gamezoneshots_get({0}:{1})'.format(fkey, fvalue))

    shot_table = {}
    shot_chart = {}

    if shot_list:
        # get shots and goals per zone
        shotzone_dic = shotsperzone_count(logger, shot_list, matchinfo_dic)
        shot_chart = shotsperzone_aggregate(logger, shotzone_dic, matchinfo_dic)
        shot_chart['background_image'] = '{0}{1}{2}'.format(url_build(request.META), settings.STATIC_URL, 'img/shot_zones.png')
        shot_table = shotzonetable_get(logger, shotzone_dic, matchinfo_dic)

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'tabs': False
    }

    return stat_entry

def _gameshotmap_get(logger, title, request, fkey, fvalue, matchinfo_dic, shot_list):
    """ get gameshotmap """
    logger.debug('_gameshotmap_get({0}:{1})'.format(fkey, fvalue))

    shot_table = [None, None]
    shot_chart = []

    if shot_list:
        # get shots and goals per min
        shotmap_dic = shotcoordinates_get(logger, shot_list, matchinfo_dic)

        shot_chart = [
            shotmapchart_create(logger, shotmap_dic['home_team']),
            shotmapchart_create(logger, shotmap_dic['visitor_team'])
        ]

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'tabs': True
    }

    return stat_entry

def _gamecorsi_get(logger, request, fkey, fvalue, matchinfo_dic, shot_list, shift_list, periodevent_list, roster_list):
    """ get corsi """
    logger.debug('_gamecorsi_get({0}:{1})'.format(fkey, fvalue))

    stat_entry_list = []

    if shot_list:
        # get corsi values per player for a certain match
        game_corsi_dic = gamecorsi_get(logger, shot_list, shift_list, periodevent_list, matchinfo_dic, roster_list)

        # corsi absolute chart and table
        corsi_chart_abs = [
            gamecorsichart_create(logger, game_corsi_dic['home_team']),
            gamecorsichart_create(logger, game_corsi_dic['visitor_team'])
        ]
        corsi_table_abs = [
            gamecorsi_table(logger, game_corsi_dic['home_team'], 'home_team', matchinfo_dic),
            gamecorsi_table(logger, game_corsi_dic['visitor_team'], 'visitor_team', matchinfo_dic)
        ]
        # pylint: disable=E0602
        stat_entry_list.append({
            'title': _('Shot attempts at even strength (CF, CA)'),
            'chart': corsi_chart_abs,
            'table': corsi_table_abs,
            'tabs': True
        })

        # corsi percentage chart and table
        corsi_chart_pctg = [
            gamecorsippctgchart_create(logger, game_corsi_dic['home_team']),
            gamecorsippctgchart_create(logger, game_corsi_dic['visitor_team'])
        ]
        corsi_table_pctg = [
            gamecorsi_table(logger, game_corsi_dic['home_team'], 'home_team', matchinfo_dic, 'cf_pctg'),
            gamecorsi_table(logger, game_corsi_dic['visitor_team'], 'visitor_team', matchinfo_dic, 'cf_pctg')
        ]
        # pylint: disable=E0602
        stat_entry_list.append({
            'title': '{0} %'.format(_('Shot attempts at even strength (CF, CA)')),
            'chart': corsi_chart_pctg,
            'table': corsi_table_pctg,
            'tabs': True
        })

    return stat_entry_list
