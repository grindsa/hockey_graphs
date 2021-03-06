#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" import shots to database """
# pylint: disable=E0401, C0413
import os
import sys
import pathlib
import argparse
from datetime import datetime
import git
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from rest.functions.gameheader import gameheader_add
from rest.functions.helper import logger_setup, uts_now, json_store
from rest.functions.match import openmatch_list_get, match_add, pastmatch_list_get, sincematch_list_get
from rest.functions.periodevent import periodevent_add
from rest.functions.player import player_list_get, player_add
from rest.functions.playerstat import playerstat_add, playerstat_get
from rest.functions.roster import roster_add
from rest.functions.season import season_latest_get, season_get
from rest.functions.shift import shift_add
from rest.functions.shot import shot_add, shot_delete, zone_name_get
from rest.functions.teamstat import teamstat_add
from delapphelper import DelAppHelper

def _playerstats_process(logger, match_id_, period, home_dic_, visitor_dic_):
    """ update match with result and finish flag """
    playerstat_list = playerstat_get(logger, 'match_id', match_id_)

    if period == 'K' and not playerstat_list:
        logger.debug('covering cornercase and set period to "3"')
        period = '3'

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

        homestat_dic[period] = home_dic_
        visitorstat_dic[period] = visitor_dic_

        playerstat_add(LOGGER, 'match_id', match_id_, {'match_id': match_id_, 'home': homestat_dic, 'visitor': visitorstat_dic})

def _match_update(logger, match_id_, header_dic):
    """ update match with result and finish flag """
    data_dic = {'match_id': match_id_}
    if 'results' in header_dic and 'score' in header_dic['results'] and 'final' in header_dic['results']['score']:
        # there is no result field thus, we need to construct it manually and update the datebase
        result = '{0}:{1}'.format(header_dic['results']['score']['final']['score_home'], header_dic['results']['score']['final']['score_guest'])
        logger.debug('update match: {0}: {1}'.format(match_id_, result))
        data_dic['result'] = result

    if 'actualTimeName' in header_dic and header_dic['actualTimeName'].lower() in ["ende", "ende n. verlängerung", "ende n. penaltyschießen"]:
        logger.debug('set finish flag for match: {0}'.format(match_id_))
        data_dic['finish'] = True
        if 'verlängerung' in header_dic['actualTimeName'].lower():
            data_dic['result_suffix'] = 'n.V.'
        elif 'penaltys' in header_dic['actualTimeName'].lower():
            data_dic['result_suffix'] = 'n.P.'

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

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='match_import.py - update matches in database')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('--shifts', help='debug mode', action="store_true", default=False)
    parser.add_argument('-s', '--season', help='season id', default=None)
    parser.add_argument('--save', help='save directory', default=None)
    parser.add_argument('--hgs', help='hgs directory', default=None)
    parser.add_argument('--gitrepo', help='git repository', action="store_true", default=False)
    mlist = parser.add_mutually_exclusive_group()
    mlist.add_argument('--matchlist', help='list of del matchids', default=[])
    mlist.add_argument('-o', '--openmatches', help='open matches from latest season', action="store_true", default=False)
    mlist.add_argument('-p', '--pastmatches', help='previous matches from latest season', action="store_true", default=False)
    mlist.add_argument('-i', '--interval', help='previous matches during last x hours', default=0)
    args = parser.parse_args()

    # default settings
    season = 0
    matchlist = None

    debug = args.debug
    addshifts = args.shifts
    openmatches = args.openmatches
    pastmatches = args.pastmatches
    season = args.season
    matchlist = args.matchlist
    interval = int(args.interval)
    save = args.save
    gitrepo = args.gitrepo
    hgs_data = args.hgs

    # process matchlist
    try:
        _tmp_list = matchlist.split(',')
    except BaseException:
        _tmp_list = []
    match_list = []
    for match in _tmp_list:
        match_list.append(int(match))

    if not openmatches and not pastmatches and not interval and not match_list:
        print('either -i -o -p parameter must be specified')
        sys.exit(0)

    return(debug, season, match_list, addshifts, openmatches, pastmatches, interval, save, hgs_data, gitrepo)

def _path_check_create(logger, path):
    """ check save path - create if does not exist """
    logger.debug('_path_check({0})'.format(path))
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':

    (DEBUG, SEASON_ID, MATCH_LIST, ADDSHIFTS, OPENMATCHES, PASTMATCHES, INTERVAL, SAVE, HGS_DATA, GITREPO) = arg_parse()

    TOURNAMENT_ID = None

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    if not SEASON_ID:
        # get season_id
        SEASON_ID = season_latest_get(LOGGER)

    # get tournament_id
    TOURNAMENT_ID = season_get(LOGGER, 'id', SEASON_ID, ['tournament'])

    if SAVE:
        if TOURNAMENT_ID:
            SAVE_DIR = '{0}/{1}'.format(SAVE, TOURNAMENT_ID)
            _path_check_create(LOGGER, SAVE)
        else:
            LOGGER.error('NO TOURNAMENT_ID found. Setting save to "None"')
            SAVE_DIR = None
    else:
        SAVE_DIR = None

    # unix timestamp
    UTS = uts_now()

    if not MATCH_LIST:
        if OPENMATCHES:
            # Get list of matches to be updated (selection current season, status finish_false, date lt_uts)
            MATCH_LIST = openmatch_list_get(LOGGER, SEASON_ID, UTS, ['match_id'])
        elif PASTMATCHES:
            MATCH_LIST = pastmatch_list_get(LOGGER, SEASON_ID, UTS, ['match_id'])
        elif INTERVAL:
            MATCH_LIST = sincematch_list_get(LOGGER, SEASON_ID, UTS, INTERVAL*3600, ['match_id'], )

    with DelAppHelper(None, DEBUG) as del_app_helper:
        for match_id in MATCH_LIST:
            LOGGER.debug('process match: {0}'.format(match_id))

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
                thome_dic = del_app_helper.teamstats_get(match_id, True)
                tvisitor_dic = del_app_helper.teamstats_get(match_id, False)
                teamstat_add(LOGGER, 'match_id', match_id, {'match_id': match_id, 'home': thome_dic, 'visitor': tvisitor_dic})
            except BaseException:
                LOGGER.debug('ERROR: teamstats_get() failed.')

            # get shifts if required
            if ADDSHIFTS:
                # print('adding shifts')
                shift_dic = del_app_helper.shifts_get(match_id)
                shift_add(LOGGER, 'match_id', match_id, {'match_id': match_id, 'shift': shift_dic})

            try:
                # delete shots for the match to cope with renumbering (rember EBBvBHV in 12/20)
                shot_delete(LOGGER, 'match_id', match_id)
                # get shots
                shots_dic = del_app_helper.shots_get(match_id)
                shots_process(LOGGER, shots_dic['match'])
            except BaseException:
                LOGGER.debug('ERROR: shots_get() failed.')

            if SAVE_DIR:
                MATCH_DIR = '{0}/matches/{1}'.format(SAVE_DIR, match_id)
                _path_check_create(LOGGER, MATCH_DIR)
                json_store('{0}/{1}'.format(MATCH_DIR, 'game-header.json'), gameheader_dic)
                json_store('{0}/{1}'.format(MATCH_DIR, 'player-stats-home.json'), home_dic)
                json_store('{0}/{1}'.format(MATCH_DIR, 'player-stats-guest.json'), visitor_dic)
                json_store('{0}/{1}'.format(MATCH_DIR, 'period-events.json'), event_dic)
                json_store('{0}/{1}'.format(MATCH_DIR, 'roster.json'), roster_dic)
                json_store('{0}/{1}'.format(MATCH_DIR, 'team-stats-home.json'), thome_dic)
                json_store('{0}/{1}'.format(MATCH_DIR, 'team-stats-guest.json'), tvisitor_dic)
                json_store('{0}/{1}'.format(MATCH_DIR, 'shots.json'), shots_dic)
                if ADDSHIFTS:
                    json_store('{0}/{1}'.format(MATCH_DIR, 'shifts.json'), shift_dic)
                    if HGS_DATA and not os.path.exists('{0}/shifts/2020/1/{1}.json'.format(HGS_DATA, match_id)):
                        LOGGER.debug('fetch shifts')
                        json_store('{0}/shifts/2020/1/{1}.json'.format(HGS_DATA, match_id), shift_dic)

    if GITREPO and SAVE:
        # check changes into repo
        repo = git.Repo(SAVE)
        if repo.is_dirty(untracked_files=True):
            commit_message = datetime.fromtimestamp(UTS).strftime("%Y-%m-%d %H:%M")
            LOGGER.debug('Changes detected. Creating commit: {0}'.format(commit_message))
            repo.git.add(all=True)
            repo.index.commit(commit_message)
            repo.remotes.origin.push()

    if GITREPO and HGS_DATA:
        # check changes into repo
        repo = git.Repo(HGS_DATA)
        if repo.is_dirty(untracked_files=True):
            commit_message = datetime.fromtimestamp(UTS).strftime("%Y-%m-%d %H:%M")
            LOGGER.debug('Changes detected. Creating commit: {0}'.format(commit_message))
            repo.git.add(all=True)
            repo.index.commit(commit_message)
            repo.remotes.origin.push()
