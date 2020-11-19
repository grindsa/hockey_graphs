#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from rest.functions.gameheader import gameheader_add
from rest.functions.helper import logger_setup, uts_now
from rest.functions.match import openmatch_list_get, match_add
from rest.functions.periodevent import periodevent_add
from rest.functions.player import player_list_get, player_add
from rest.functions.playerstat import playerstat_add, playerstat_get
from rest.functions.roster import roster_add
from rest.functions.season import season_latest_get
# from rest.functions.shift import shift_add
from rest.functions.shot import shot_add, zone_name_get
from rest.functions.teamstat import teamstat_add
from delapphelper import DelAppHelper

def _playerstats_process(logger, match_id, period, home_dic, visitor_dic):
    """ update match with result and finish flag """
    playerstat_list = playerstat_get(logger, 'match_id', match_id)

    # filter only allowed periods
    periods_allowed = ['1', '2', '3', 'P']
    if period in periods_allowed:

        if 'home' in playerstat_list:
            homestat_dic = playerstat_list['home']
        else:
            homestat_dic = {}
        if 'visitor' in playerstat_list:
            visitorstat_dic = playerstat_list['visitor']
        else:
            visitorstat_dic = {}
        homestat_dic[period] = home_dic
        visitorstat_dic[period] = visitor_dic
        playerstat_add(LOGGER, 'match_id', match_id, {'match_id': match_id, 'home': homestat_dic, 'visitor': visitorstat_dic})


def _match_update(logger, match_id_, header_dic):
    """ update match with result and finish flag """
    data_dic = {'match_id': match_id_}
    if 'results' in header_dic and 'score' in header_dic['results'] and 'final' in header_dic['results']['score']:
        # there is no result field thus, we need to construct it manually and update the datebase
        result = '{0}:{1}'.format(header_dic['results']['score']['final']['score_home'], header_dic['results']['score']['final']['score_guest'])
        logger.debug('update match: {0}: {1}'.format(match_id_, result))
        data_dic['result'] = result

    if 'actualTimeName' in header_dic and header_dic['actualTimeName'].lower() == "ende":
        logger.debug('set finish flag for match: {0}'.format(match_id_))
        data_dic['finish'] = True

    match_add(logger, 'match_id', match_id_, data_dic)

def shots_process(logger, match_dic):
    """ process match dictionary """
    # get list of players
    player_list = player_list_get(LOGGER, None, None, ['player_id'])

    for shot in match_dic['shots']:
        # add player if not exists
        if shot['player_id'] not in player_list:
            logger.debug('create_player: {0}, {1}, {2}, {3}'.format(shot['player_id'], shot['first_name'], shot['last_name'], shot['jersey']))
            player_id = player_add(logger, 'player_id', shot['player_id'], {'player_id': shot['player_id'], 'first_name': shot['first_name'], 'last_name': shot['last_name'], 'jersey': shot['jersey']})
            player_list.append(player_id)

        # add shot
        zone = zone_name_get(logger, shot['coordinate_x'], shot['coordinate_y'])
        logger.debug('add_shot: {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}'.format(shot['player_id'], shot['team_id'], shot['match_shot_resutl_id'], shot['time'], shot['coordinate_x'], shot['coordinate_y'], shot['real_date'], shot['polygon'], zone))
        data_dic = {
            'shot_id': shot['id'],
            'player_id': shot['player_id'],
            'team_id': shot['team_id'],
            'match_id': match_dic['id'],
            'match_shot_resutl_id': shot['match_shot_resutl_id'],
            'timestamp': shot['time'],
            'coordinate_x': shot['coordinate_x'],
            'coordinate_y': shot['coordinate_y'],
            'real_date': shot['real_date'],
            'polygon': shot['polygon'],
            'zone': zone,
        }
        shot_add(logger, 'shot_id', shot['id'], data_dic)

if __name__ == '__main__':

    DEBUG = False

    # initialize logger
    LOGGER = logger_setup(DEBUG)
    # get season_id
    SEASON_ID = season_latest_get(LOGGER)
    # unix timestamp
    UTS = uts_now()

    # Get list of matches to be updated (selection current season, status finish_false, date lt_uts)
    match_list = openmatch_list_get(LOGGER, SEASON_ID, UTS, ['match_id'])

    with DelAppHelper(None, DEBUG) as del_app_helper:
        for match_id in match_list:

            # get matchheader
            gameheader_dic = del_app_helper.gameheader_get(match_id)
            gameheader_add(LOGGER, 'match_id', match_id, {'match_id': match_id, 'gameheader': gameheader_dic})
            _match_update(LOGGER, match_id, gameheader_dic)

            if 'actualTimeAlias' in gameheader_dic:
                period = gameheader_dic['actualTimeAlias']
                home_dic = del_app_helper.playerstats_get(match_id, True)
                visitor_dic = del_app_helper.playerstats_get(match_id, False)
                _playerstats_process(LOGGER, match_id, period, home_dic, visitor_dic)


            # get and store periodevents
            try:
                event_dic = del_app_helper.periodevents_get(match_id)
                # pprint(event_dic)
                periodevent_add(LOGGER, 'match_id', match_id, {'match_id': match_id, 'period_event': event_dic})
            except BaseException:
                LOGGER.debug('ERROR: periodevents_get() failed.')

            try:
                # get and store rosters
                roster_dic = del_app_helper.roster_get(match_id)
                roster_add(LOGGER, 'match_id', match_id, {'match_id': match_id, 'roster': roster_dic})
            except BaseException:
                LOGGER.debug('ERROR: roster_get() failed.')

            try:
                # get teamstat
                home_dic = del_app_helper.teamstats_get(match_id, True)
                visitor_dic = del_app_helper.teamstats_get(match_id, False)
                teamstat_add(LOGGER, 'match_id', match_id, {'match_id': match_id, 'home': home_dic, 'visitor': visitor_dic})
            except BaseException:
                LOGGER.debug('ERROR: teamstats_get() failed.')

            # get shifts
            # shift_dic = del_app_helper.shifts_get(match_id)
            # shift_add(LOGGER, 'match_id', match_id, {'match_id': match_id, 'shift': shift_dic})

            try:
                # get shots
                shots_dic = del_app_helper.shots_get(match_id)
                shots_process(LOGGER, shots_dic['match'])
            except BaseException:
                LOGGER.debug('ERROR: shots_get() failed.')
