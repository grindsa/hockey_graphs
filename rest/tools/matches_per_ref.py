#!/usr/bin/python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from rest.functions.season import season_latest_get, season_get
from rest.functions.team import team_dic_get
from rest.functions.helper import logger_setup, uts_now, uts_to_date_utc
from rest.functions.match import pastmatch_list_get, matchstats_get, match_info_get
from rest.functions.gameheader import gameheader_get
from pprint import pprint
import gettext

if __name__ == '__main__':

    DEBUG = False
    TEAM_SHORTCUT = 'AEV'
    REF_NAME = 'Rantala'
    SEASON_LIST = [3, 4]

    # initialize logger
    LOGGER = logger_setup(DEBUG)
    TEAM_ID = None
    MATCH_LIST = []

    # unix timestamp
    UTS = uts_now()

    # ugly hack to set localdir correctly
    if os.path.exists('/var/www/hockey_graphs/locale'):
        localedir = '/var/www/hockey_graphs/locale'
    else:
        localedir = 'locale'
    LOGGER.debug('set localedir to: {0}'.format(localedir))

    en = gettext.translation('django', localedir=localedir, languages=['en'])
    de = gettext.translation('django', localedir=localedir, languages=['de'])
    en.install()
    LCLANG = 'en'

    # lookup id of team in scope of analysis
    TEAM_DIC = team_dic_get(LOGGER, None)
    for _team_id in TEAM_DIC:
        if TEAM_DIC[_team_id]['shortcut'] == TEAM_SHORTCUT:
            TEAM_ID = _team_id
            break

    if TEAM_ID:
        # lookup matches from season list
        for season_id in SEASON_LIST:
            match_list =  pastmatch_list_get(LOGGER, season_id, UTS, ['match_id'])
            MATCH_LIST.extend(match_list)

        if MATCH_LIST:
            for match_id in MATCH_LIST:
                game_header = gameheader_get(LOGGER, 'match_id', match_id, ['gameheader'])
                if game_header:
                    # filter on team
                    if game_header['teamInfo']['home']['id'] == TEAM_ID or game_header['teamInfo']['visitor']['id'] == TEAM_ID:
                        # filter on ref
                        if REF_NAME in game_header['referees']['headReferee1']['name'] or REF_NAME in game_header['referees']['headReferee2']['name']:
                            matchstat_dic = matchstats_get(LOGGER, match_id)
                            matchinfo_dic = match_info_get(LOGGER, match_id, None)
                            # print(matchinfo_dic)
                            game_info = '{0}: {1} ({2}) {5}:{6} {3} ({4})'.format(
                                uts_to_date_utc(matchinfo_dic['date_uts'], '%d.%m.%Y'),
                                game_header['teamInfo']['home']['shortcut'],
                                matchstat_dic['chart']['home_team']['penaltyMinutes'],
                                game_header['teamInfo']['visitor']['shortcut'],
                                matchstat_dic['chart']['visitor_team']['penaltyMinutes'],
                                game_header['results']['score']['final']['score_home'],
                                game_header['results']['score']['final']['score_guest'])

                            print(game_info)
