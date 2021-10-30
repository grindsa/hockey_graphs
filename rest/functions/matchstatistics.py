# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413, R0914
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.functions.corsi import gamecorsi_get, gameplayercorsi_get, gameshots5v5_get
from rest.functions.socialnetworkeventcharts import chatterchart_create
from rest.functions.socialnetworkevent import socialnetworkevent_get, eventspermin_combine
from rest.functions.shot import shot_list_get, shotspermin_count, shotspermin_aggregate, shotstatus_count, shotstatus_aggregate, shotsperzone_count, shotsperzone_aggregate, shotcoordinates_get, gameflow_get
from rest.functions.shotcharts import shotsumchart_create, gameflowchart_create, shotstatussumchart_create, shotmapchart_create, gamecorsichart_create, gameplayercorsichart_create, gamecorsippctgchart_create, puckpossessionchart_create, shotzonechart_create
from rest.functions.toicharts import gametoichart_create, gametoipppkchart_create
from rest.functions.heatmapcharts import gamematchupchart_create
from rest.functions.heatmap import gameheatmapdata_get
from rest.functions.shottables import shotsperiodtable_get, shotstatussumtable_get, shotzonetable_get, gamecorsi_table
from rest.functions.toitables import gametoi_table, toi_chk
from rest.functions.match import match_info_get, matchstats_get
from rest.functions.shift import shift_get, toifromshifts_get, shiftsperplayer_get, shiftchartdata_get, shiftsupdates_get
from rest.functions.shiftcharts import shiftsperplayerchart_create
from rest.functions.roster import roster_get
from rest.functions.periodevent import periodevent_get, penaltyplotlines_get, goalsfromevents_get, goalplotlines_get, penaltiesfromevents_get
from rest.functions.playerstat import playerstat_get, toifromplayerstats_get, matchupmatrix_get, toipppk_get
from rest.functions.chartparameters import chart_colors_get
from rest.functions.helper import url_build, mobile_check

def matchstatistics_get(logger, request, fkey=None, fvalue=None):
    """ matchstatistics grouped by days """
    logger.debug('matchstatistics_get({0}:{1})'.format(fkey, fvalue))

    ismobile = mobile_check(logger, request)

    # fkey = 'match_id'
    # fvalue = 1804

    # we protect the REST and will not return anything without matchid
    if fkey:
        # we need some match_information
        matchinfo_dic = match_info_get(logger, fvalue, request.META)

        # get colors to be used
        color_dic = chart_colors_get(logger, matchinfo_dic)

        # pylint: disable=E0602
        vs_name = _('vs.')
        subtitle = '{0} {2} {1}'.format(matchinfo_dic['home_team__team_name'], matchinfo_dic['visitor_team__team_name'], vs_name)

        # get list of shots
        shot_list = shot_list_get(logger, fkey, fvalue, ['timestamp', 'match_shot_resutl_id', 'real_date', 'team_id', 'player__first_name', 'player__last_name', 'zone', 'coordinate_x', 'coordinate_y', 'player__jersey'])

        # get list of shifts
        shift_list = shift_get(logger, fkey, fvalue, ['shift'])

        # get period events
        periodevent_list = periodevent_get(logger, fkey, fvalue, ['period_event'])

        # get rosters
        roster_list = roster_get(logger, fkey, fvalue, ['roster'])

        # create plotlines to be addedd to chart
        # plotbands_list = penaltyplotlines_get(logger, fkey, fvalue, color_dic['home_team_color_penalty_primary'], color_dic['visitor_team_color_penalty_secondary'])
        plotbands_list = penaltyplotlines_get(logger, fkey, fvalue, color_dic['visitor_team_color_penalty_secondary'], color_dic['home_team_color_penalty_primary'])

        (_sf_5v5, _sa_5v5, _sogf_5v5, _soga_5v5, shot_list_5v5) = gameshots5v5_get(logger, matchinfo_dic, 'foo', shot_list, shift_list, periodevent_list)

        result = []

        # get matchstatistics
        result.append(matchstats_get(logger, fvalue))

        # create chart for shots per match
        # pylint: disable=E0602
        result.append(_gameshots_get(logger, _('Shots per minute'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list, color_dic))

        # create shotflowchart
        # pylint: disable=E0602
        result.append(_gameflow_get(logger, _('Gameflow'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list, color_dic))

        # create chart for shotstatus
        # pylint: disable=E0602
        result.append(_gameshootstatus_get(logger, _('Shots by Result'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list))

        # create shotzone chart
        # pylint: disable=E0602
        result.append(_gamezoneshots_get(logger, _('Shots per Zone'), subtitle, ismobile, request, matchinfo_dic, shot_list))

        # shotmap
        # pylint: disable=E0602
        result.append(_gameheatmap_get(logger, _('Shot attempts 5v5'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list_5v5))

        # shotmap
        # pylint: disable=E0602
        result.append(_gameshotmap_get(logger, _('Game Shotmap'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list))

        # player corsi
        # pylint: disable=E0602
        result.extend(_gamecorsi_get(logger, subtitle, ismobile, request, matchinfo_dic, shot_list, shot_list_5v5, shift_list, periodevent_list, roster_list, plotbands_list, color_dic))

        # puck possession
        # pylint: disable=E0602
        result.append(_gamepuckpossession_get(logger, _('Puck possession'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list, color_dic))

        # time on ice per player
        # pylint: disable=E0602
        result.extend(_gametoi_get(logger, _('Time on Ice per Player'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shift_list))

        # pylint: disable=E0602
        result.append(_shiftchart_get(logger, _('Shift Chart'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shift_list, roster_list, periodevent_list, color_dic))

        # pylint: disable=E0602
        result.append(_gamematchup_get(logger, _('5v5 Matchup'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list, shift_list, roster_list, periodevent_list))

        # pylint: disable=E0602
        result.append(_chatterchart_get(logger, _('Real-Time Fan Reactions'), subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list, periodevent_list, color_dic))

    else:
        result = {'error': 'Please specify a matchid'}

    return result

def _gameflow_get(logger, title, subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list, color_dic):
    """ prepare shots per match chart """
    logger.debug('_shots_per_match_get({0}:{1})'.format(fkey, fvalue))

    stat_entry = {}

    if shot_list:
        # get shots and goals per min
        (shotmin_dic, goal_dic) = shotspermin_count(logger, shot_list, matchinfo_dic)

        gameflow_dic = gameflow_get(logger, shotmin_dic)

        # create plotlines to be addedd to chart
        plotline_list = penaltyplotlines_get(logger, fkey, fvalue, color_dic['visitor_team_color_penalty_secondary'], color_dic['home_team_color_penalty_primary'])

        # create the chart
        shot_chart = gameflowchart_create(logger, title, subtitle, ismobile, gameflow_dic, goal_dic, plotline_list, matchinfo_dic, color_dic)

        stat_entry = {
            'title': title,
            'chart': shot_chart,
            'tabs': False
        }

    return stat_entry

def _gamepuckpossession_get(logger, title, subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list, color_dic):
    """ create chart for puck possession """
    logger.debug('_gamepuckpossession_get({0}:{1})'.format(fkey, fvalue))

    shot_table = {}
    shot_chart = {}

    if shot_list:

        # get shots and goals per min
        (shotmin_dic, goal_dic) = shotspermin_count(logger, shot_list, matchinfo_dic)

        # aggregate shots per min
        shotsum_dic = shotspermin_aggregate(logger, shotmin_dic)

        shot_chart = puckpossessionchart_create(logger, title, subtitle, ismobile, shotsum_dic, goal_dic, matchinfo_dic, color_dic)

        # pylint: disable=E0602
        shot_table = shotsperiodtable_get(logger, _('Shots per period'), shotmin_dic, matchinfo_dic)

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'tabs': False
    }

    return stat_entry

def _gameshootstatus_get(logger, title, subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list):
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
            shotstatussumchart_create(logger, '{1} - {0}'.format(title, matchinfo_dic['home_team__shortcut']), subtitle, ismobile, shotstatussum_dic, shotstatus_dic, goal_dic, 'home_team', matchinfo_dic),
            shotstatussumchart_create(logger, '{1} - {0}'.format(title, matchinfo_dic['visitor_team__shortcut']), subtitle, ismobile, shotstatussum_dic, shotstatus_dic, goal_dic, 'visitor_team', matchinfo_dic),
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

def _gameshots_get(logger, title, subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list, color_dic):
    """ prepare shots per match chart """
    logger.debug('_gameshots_get({0}:{1})'.format(fkey, fvalue))

    stat_entry = {}
    if shot_list:

        # get shots and goals per min
        (shotmin_dic, goal_dic) = shotspermin_count(logger, shot_list, matchinfo_dic)

        # aggregate shots per min
        shotsum_dic = shotspermin_aggregate(logger, shotmin_dic)

        # create plotlines to be addedd to chart
        plotline_list = penaltyplotlines_get(logger, fkey, fvalue, color_dic['visitor_team_color_penalty_secondary'], color_dic['home_team_color_penalty_primary'])

        # pylint: disable=E0602
        stat_entry = {
            'title': title,
            'chart': shotsumchart_create(logger, title, subtitle, ismobile, shotsum_dic, shotmin_dic, goal_dic, plotline_list, matchinfo_dic, color_dic),
            'table': shotsperiodtable_get(logger, _('Shots per period'), shotmin_dic, matchinfo_dic),
            'tabs': False
        }

    return stat_entry

def _gamezoneshots_get(logger, title, subtitle, ismobile, request, matchinfo_dic, shot_list):
    """ shots per zone """
    logger.debug('_gamezoneshots_get()')

    bg_image = '{0}{1}{2}'.format(url_build(request.META), settings.STATIC_URL, 'img/shot_zones.png')

    if shot_list:
        # get shots and goals per zone
        shotzone_dic = shotsperzone_count(logger, shot_list, matchinfo_dic)
        shotzoneagg_dic = shotsperzone_aggregate(logger, shotzone_dic, matchinfo_dic)

        stat_entry = {
            'title': title,
            'chart': shotzonechart_create(logger, title, subtitle, ismobile, request, shotzoneagg_dic, bg_image),
            'table': shotzonetable_get(logger, shotzone_dic, matchinfo_dic),
            'tabs': False
        }
    else:
        stat_entry = {}

    return stat_entry

def _gameheatmap_get(logger, title, subtitle, _ismobile, request, fkey, fvalue, matchinfo_dic, shot_list):
    """ get gameshotmap """
    logger.debug('_gameheatmap_get({0}:{1})'.format(fkey, fvalue))

    shot_table = None
    shotmap_dic = {}

    if shot_list:
        # get shots and goals per min
        shotmap_dic = gameheatmapdata_get(logger, title, subtitle, _ismobile, matchinfo_dic, shot_list)

    stat_entry = {
        'title': title,
        'chart': shotmap_dic,
        'table': shot_table,
        'tabs': False
    }

    return stat_entry

def _gameshotmap_get(logger, title, subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list):
    """ get gameshotmap """
    logger.debug('_gameshotmap_get({0}:{1})'.format(fkey, fvalue))

    shot_table = [None, None]
    shot_chart = []

    if shot_list:
        # get shots and goals per min
        shotmap_dic = shotcoordinates_get(logger, shot_list, matchinfo_dic)

        shot_chart = [
            shotmapchart_create(logger, '{0} {1}'.format(title, matchinfo_dic['home_team__shortcut']), subtitle, ismobile, shotmap_dic['home_team']),
            shotmapchart_create(logger, '{0} {1}'.format(title, matchinfo_dic['visitor_team__shortcut']), subtitle, ismobile, shotmap_dic['visitor_team'])
        ]

    stat_entry = {
        'title': title,
        'chart': shot_chart,
        'table': shot_table,
        'tabs': True
    }

    return stat_entry

def _gamecorsi_get(logger, subtitle, ismobile, request, matchinfo_dic, shot_list, shot_list_5v5, shift_list, periodevent_list, roster_list, plotbands_list, color_dic):
    """ get corsi """
    # pylint: disable=R0913, R0914
    logger.debug('_gamecorsi_get()')

    stat_entry_list = []

    if shot_list_5v5:
        game_corsi_dic = gamecorsi_get(logger, shot_list, shot_list_5v5, matchinfo_dic, color_dic)

        # pylint: disable=E0602
        title = _('Shot attempt differential (Corsi)')

        stat_entry_list.append({
            'title': title,
            'chart': gamecorsichart_create(logger, title, subtitle, ismobile, game_corsi_dic, plotbands_list, matchinfo_dic, color_dic),
            'table': [],
            'tabs': False
        })

    if shot_list:

        # get corsi values per player for a certain match
        game_playercorsi_dic = gameplayercorsi_get(logger, shot_list, shift_list, periodevent_list, matchinfo_dic, roster_list)

        # pylint: disable=E0602
        title = _('Shot attempts at even strength (CF, CA)')
        ctitle = _('Shot attempts at even strength')

        if game_playercorsi_dic:
            # corsi absolute chart and table
            corsi_chart_abs = [
                gameplayercorsichart_create(logger, '{1} - {0}'.format(ctitle, matchinfo_dic['home_team__shortcut']), subtitle, ismobile, game_playercorsi_dic['home_team']),
                gameplayercorsichart_create(logger, '{1} - {0}'.format(ctitle, matchinfo_dic['visitor_team__shortcut']), subtitle, ismobile, game_playercorsi_dic['visitor_team'])
            ]
            corsi_table_abs = [
                gamecorsi_table(logger, ismobile, game_playercorsi_dic['home_team'], matchinfo_dic),
                gamecorsi_table(logger, ismobile, game_playercorsi_dic['visitor_team'], matchinfo_dic)
            ]
        else:
            corsi_chart_abs = [{}, {}]
            corsi_table_abs = []

        # pylint: disable=E0602
        stat_entry_list.append({
            'title': title,
            'chart': corsi_chart_abs,
            'table': corsi_table_abs,
            'tabs': True
        })

        title = _('Shot attempts at even strength (CF, CA)')
        if game_playercorsi_dic:
            # corsi percentage chart and table
            corsi_chart_pctg = [
                gamecorsippctgchart_create(logger, '{1} - {0}'.format(ctitle, matchinfo_dic['home_team__shortcut']), subtitle, ismobile, game_playercorsi_dic['home_team']),
                gamecorsippctgchart_create(logger, '{1} - {0}'.format(ctitle, matchinfo_dic['visitor_team__shortcut']), subtitle, ismobile, game_playercorsi_dic['visitor_team'])
            ]
            corsi_table_pctg = [
                gamecorsi_table(logger, ismobile, game_playercorsi_dic['home_team'], matchinfo_dic, 'cf_pctg'),
                gamecorsi_table(logger, ismobile, game_playercorsi_dic['visitor_team'], matchinfo_dic, 'cf_pctg')
            ]
        else:
            corsi_chart_pctg = [{}, {}]
            corsi_table_pctg = [{}, {}]

        # pylint: disable=E0602
        stat_entry_list.append({
            'title': '{0} %'.format(title),
            'chart': corsi_chart_pctg,
            'table': corsi_table_pctg,
            'tabs': True
        })

    return stat_entry_list

def _gametoi_get(logger, title, subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shift_list):
    """ get corsi """
    logger.debug('_gametoi_get({0}:{1})'.format(fkey, fvalue))

    stat_entry_list = []

    playerstat_dic = playerstat_get(logger, fkey, fvalue, ['home', 'visitor'])
    # get time_on_ice stats for powerplay and penalty killing
    toipppk_dic = toipppk_get(logger, matchinfo_dic, playerstat_dic)

    # toi chart and table
    toi_table = [None, None]
    toi_chart = []

    if shift_list:
        # get time-on-ice based on shifts
        toi_dic = toifromshifts_get(logger, matchinfo_dic, shift_list)
        toi_check = True
    else:
        # get time-on-ice based on playerstats - THIS IS UNTESTED
        toi_dic = toifromplayerstats_get(logger, matchinfo_dic, playerstat_dic)
        # check toi for
        toi_check = toi_chk(logger, toi_dic)

    if toi_dic:
        # create chart and table
        toi_chart = [
            gametoichart_create(logger, '{1} - {0}'.format(title, matchinfo_dic['home_team__shortcut']), subtitle, ismobile, toi_dic['home_team'], matchinfo_dic['home_team__color_primary'], matchinfo_dic['home_team__color_secondary'], matchinfo_dic['home_team__color_tertiary'], matchinfo_dic['home_team__color_quaternary'], toi_check),
            gametoichart_create(logger, '{1} - {0}'.format(title, matchinfo_dic['visitor_team__shortcut']), subtitle, ismobile, toi_dic['visitor_team'], matchinfo_dic['visitor_team__color_primary'], matchinfo_dic['visitor_team__color_secondary'], matchinfo_dic['visitor_team__color_tertiary'], matchinfo_dic['visitor_team__color_quaternary'], toi_check),
        ]
        if toi_check:
            toi_table = [
                gametoi_table(logger, toi_dic['home_team']),
                gametoi_table(logger, toi_dic['visitor_team']),
            ]
        else:
            toi_table = []
        stat_entry = {
            'title': title,
            'chart': toi_chart,
            'table': toi_table,
            'tabs': True
        }
        stat_entry_list.append(stat_entry)

    if toipppk_dic:
        # pylint: disable=E0602
        title = _('Time on Ice during PP and PK')
        toippk_chart = [
            gametoipppkchart_create(logger, '{1} - {0}'.format(title, matchinfo_dic['home_team__shortcut']), subtitle, ismobile, toipppk_dic['home_team'], matchinfo_dic['home_team__color_primary'], matchinfo_dic['home_team__color_secondary']),
            gametoipppkchart_create(logger, '{1} - {0}'.format(title, matchinfo_dic['visitor_team__shortcut']), subtitle, ismobile, toipppk_dic['visitor_team'], matchinfo_dic['visitor_team__color_primary'], matchinfo_dic['visitor_team__color_secondary']),
        ]

        stat_entry = {
            'title': title,
            'chart': toippk_chart,
            'table': [],
            'tabs': True
        }
        stat_entry_list.append(stat_entry)

    return stat_entry_list

def _gamematchup_get(logger, title, subtitle, ismobile, request, _fkey, _fvalue, matchinfo_dic, shot_list, shift_list, roster_list, periodevent_list):
    """ game matchup """
    logger.debug('_gamematchup_get()')

    stat_entry = {'title': title, 'table': {}, 'tabs': False, 'chart': {}}
    if shift_list:

        # get matrix showing the different player relations
        (lineup_dic, matchup_matrix, plotline_dic) = matchupmatrix_get(logger, matchinfo_dic, shot_list, shift_list, roster_list, periodevent_list)

        stat_entry = {
            'title': title,
            'chart': gamematchupchart_create(logger, title, subtitle, ismobile, lineup_dic, matchup_matrix, plotline_dic, matchinfo_dic),
            'table': {},
            'tabs': False
        }

    return stat_entry

def _chatterchart_get(logger, title, subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shot_list, periodevent_list, color_dic):
    # pylint: disable=R0913
    """ chatter chart """
    logger.debug('_chatterchart_get()')
    stat_entry = {'title': title, 'table': {}, 'tabs': False, 'chart': {}}

    if shot_list:
        # get shots and goals per min
        goal_dic = goalsfromevents_get(logger, periodevent_list)

        # get social network events per match
        socialnetworkevents_dic = socialnetworkevent_get(logger, fkey, fvalue)
        events_dic = eventspermin_combine(logger, socialnetworkevents_dic, matchinfo_dic['home_team__twitter_name'], matchinfo_dic['visitor_team__twitter_name'])

        #plotline_list = []
        (plotline_list, events_dic) = goalplotlines_get(logger, events_dic, goal_dic, matchinfo_dic['home_team__shortcut'], color_dic['home_team_color_primary'], matchinfo_dic['visitor_team__shortcut'], color_dic['visitor_team_color_secondary'])

        stat_entry = {
            'title': title,
            'chart': chatterchart_create(logger, title, subtitle, ismobile, events_dic, plotline_list),
            'table': {},
            'tabs': False
        }

    return stat_entry

def _shiftchart_get(logger, title, subtitle, ismobile, request, fkey, fvalue, matchinfo_dic, shift_list, roster_list, periodevent_list, color_dic):
    """ game matchup """
    # pylint: disable=R0913
    logger.debug('_shiftchart_get()')

    shift_chart = {}
    shift_updates = {}

    # stat_entry = {'title': title, 'table': {}, 'tabs': False, 'chart': {}}
    if shift_list:

        # get list of penalties
        penalty_dic = penaltiesfromevents_get(logger, periodevent_list)
        # plotlbands_list = penaltyplotlines_get(logger, fkey, fvalue, color_dic['home_team_color_penalty_primary'], color_dic['visitor_team_color_penalty_secondary'], scale='millisecond')
        plotlbands_list = penaltyplotlines_get(logger, fkey, fvalue, color_dic['visitor_team_color_penalty_secondary'], color_dic['home_team_color_penalty_primary'])

        # get matrix showing the different player relations
        (shiftsperplayer_dic) = shiftsperplayer_get(logger, matchinfo_dic, shift_list, roster_list, penalty_dic)
        goal_dic = goalsfromevents_get(logger, periodevent_list)

        # get chartdata
        chart_data = shiftchartdata_get(logger, ismobile, shiftsperplayer_dic, goal_dic, matchinfo_dic, plotlbands_list, color_dic)
        # create updates
        shift_updates = shiftsupdates_get(logger, subtitle, ismobile, chart_data)

        # create chart
        shift_chart = shiftsperplayerchart_create(logger, title, subtitle, ismobile, chart_data[5])

    stat_entry = {
        'title': title,
        'chart': shift_chart,
        'updates': shift_updates,

        'table': {},
        'tabs': False
    }

    return stat_entry
