#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" small protoype to fetch tweets from twitter based on hashtag """
import os
import sys
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
# pylint: disable=E0401, C0413
from rest.functions.helper import config_load, logger_setup, uts_now, path_check_create, json_store
from rest.functions.match import sincematch_list_get
from rest.functions.season import season_latest_get, season_get
from rest.functions.socialnetworkevent import socialnetworkevent_add, twitter_login, tweets_get, tags_build

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='tag_fetcher.py - fetch tweets from twitter based on hashtag')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-b', '--buffer', help='pre/post game buffer in hours (default: 0)', default=0)
    parser.add_argument('-s', '--season', help='season id', default=None)
    parser.add_argument('--save', help='save directory', default=None)
    mlist = parser.add_mutually_exclusive_group()
    mlist.add_argument('-i', '--interval', help='previous matches during last x hours', default=0)
    mlist.add_argument('--matchlist', help='list of del matchids', default=[])

    args = parser.parse_args()

    # default settings
    season = 0
    matchlist = None

    debug = args.debug
    buffer = int(args.buffer)
    season = args.season
    matchlist = args.matchlist
    interval = int(args.interval)
    save = args.save

    # process matchlist
    try:
        _tmp_list = matchlist.split(',')
    except BaseException:
        _tmp_list = []
    match_list = []
    for match_ in _tmp_list:
        match_list.append(int(match_))

    if not season and not interval and not match_list:
        print('either -i or -s parameter must be specified')
        sys.exit(0)

    return(debug, season, match_list, interval, buffer, save)

def _config_load(logger, cfg_file=os.path.dirname(__file__)+'/'+'hockeygraphs.cfg'):
    """" load config from file """
    logger.debug('_config_load()')

    consumer_key = None
    consumer_secret = None
    oauth_token = None
    oauth_token_secret = None

    config_dic = config_load(cfg_file=cfg_file)
    if 'Twitter' in config_dic:
        if 'consumer_key' in config_dic['Twitter']:
            consumer_key = config_dic['Twitter']['consumer_key']
        if 'consumer_secret' in config_dic['Twitter']:
            consumer_secret = config_dic['Twitter']['consumer_secret']
        if 'oauth_token' in config_dic['Twitter']:
            oauth_token = config_dic['Twitter']['oauth_token']
        if 'oauth_token_secret' in config_dic['Twitter']:
            oauth_token_secret = config_dic['Twitter']['oauth_token_secret']

    if not (consumer_key and consumer_secret and oauth_token and oauth_token_secret):
        logger.debug('_config_load(): twitter configuration incomplete')
        sys.exit(0)

    logger.debug('_config_load() ended.')
    return (consumer_key, consumer_secret, oauth_token, oauth_token_secret)

if __name__ == "__main__":

    # get commandline arguments
    (DEBUG, SEASON_ID, MATCH_LIST, INTERVAL, BUFFER_HR, SAVE) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # calculate pre-post buffer in second
    BUFFER = BUFFER_HR * 3600

    # get season_id if not specified
    if not SEASON_ID:
        SEASON_ID = season_latest_get(LOGGER)

    # get tournament_id
    TOURNAMENT_ID = season_get(LOGGER, 'id', SEASON_ID, ['tournament'])

    if SAVE:
        if TOURNAMENT_ID:
            SAVE_DIR = '{0}/{1}'.format(SAVE, TOURNAMENT_ID)
            path_check_create(LOGGER, SAVE)
        else:
            LOGGER.error('NO TOURNAMENT_ID found. Setting save to "None"')
            SAVE_DIR = None
    else:
        SAVE_DIR = None


    # unix timestamp
    UTS = uts_now()

    # load rebound and break interval from config file
    (CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) = _config_load(LOGGER)
    # LogIn
    TWITTER_API = twitter_login(LOGGER, CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # if not MATCH_LIST:
    # get list of matches
    MATCH_LIST = sincematch_list_get(LOGGER, SEASON_ID, UTS, INTERVAL*3600, ['match_id', 'home_team__shortcut', 'visitor_team__shortcut', 'date_uts'])

    for match in MATCH_LIST:
        # we need the matchid for database update
        match_id = match['match_id']

        # match uts (for comparison against tweets)
        match_uts = match['date_uts']

        # build the tag used in search query
        hashtag_list = tags_build(LOGGER, match['home_team__shortcut'], match['visitor_team__shortcut'])

        # get tweets per hash-tag and store in a list
        TWEET_LIST = tweets_get(LOGGER, TWITTER_API, hashtag_list)

        SAVE_LIST = []
        for tweet in sorted(TWEET_LIST, key=lambda i: i['uts'], reverse=False):
            # check if message is within buffer
            if match_uts - BUFFER <= tweet['uts'] and tweet['uts'] <= match_uts + BUFFER:
                # skip tweets from tippspiel
                if '#bot1337' not in tweet['text_raw']:
                    # push tweet to dictionalry in case we have to sore it
                    if SAVE_DIR:
                        SAVE_LIST.append(tweet)
                    data_dic = {
                        'match_id': match_id,
                        'source': 'twitter',
                        'name':  tweet['name'],
                        'name_alternate': tweet['screen_name'],
                        'identifier': tweet['id'],
                        'created_at': tweet['created_at'],
                        'created_uts': tweet['uts'],
                        'text_raw': tweet['text_raw'],
                        'tag': tweet['hashtag']
                    }
                    socialnetworkevent_add(LOGGER, 'identifier', tweet['id'], data_dic)

        # store tweet_list
        if SAVE_DIR:
            MATCH_DIR = '{0}/matches/{1}'.format(SAVE_DIR, match_id)
            path_check_create(LOGGER, MATCH_DIR)
            json_store('{0}/{1}'.format(MATCH_DIR, 'twitter.json'), SAVE_LIST)
