#!/usr/bin/python3
""" little utility to extend an existing facebook user-access token """
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
# import project settings
# pylint: disable=C0413, E0401, W0611
from django.conf import settings
from rest.functions.helper import logger_setup, uts_now, uts_to_date_utc, config_load, json_store

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='fb_token_extender.py - extend facebook user-access token to 60days')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-t', '--token', help='useraccess-token', required=True, default=None)
    parser.add_argument('-w', '--write', help='destination file', default='fb-ua-token.json')
    args = parser.parse_args()

    debug = args.debug
    token = args.token
    filename = args.write

    #if not token:
    #    print('-i or --matchlist parameter must be specified')
    #    sys.exit(0)

    return(debug, token, filename)

def _config_load(logger, cfg_file=os.path.dirname(__file__)+'/'+'hockeygraphs.cfg'):
    """" load config from file """
    logger.debug('_config_load()')

    app_name = None
    app_id = None
    app_secret = None

    config_dic = config_load(cfg_file=cfg_file)
    if 'Facebook' in config_dic:
        if 'app_name' in config_dic['Facebook']:
            app_name = config_dic['Facebook']['app_name']
        if 'app_id' in config_dic['Facebook']:
            app_id = config_dic['Facebook']['app_id']
        if 'app_secret' in config_dic['Facebook']:
            app_secret = config_dic['Facebook']['app_secret']

    if not (app_name and app_id and app_secret):
        logger.debug('_config_load(): Facebook configuration incomplete')
        sys.exit(0)

    logger.debug('_config_load() ended.')
    return (app_name, app_id, app_secret)


if __name__ == '__main__':

    (DEBUG, TOKEN, FILENAME) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # load rebound and break interval from config file
    (APP_NAME, APP_ID, APP_SECRET) = _config_load(LOGGER)

    # unix timestamp
    UTS = uts_now()

    URL = "https://graph.facebook.com/v10.0/oauth/access_token"

    data_dic = {
        'grant_type': 'fb_exchange_token',
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'fb_exchange_token': TOKEN
    }

    try:
        req = requests.get(URL, params=data_dic)
        result = req.json()
        # add current uts and date
        result['uts'] = UTS
        result['DATE_HUMAN'] = uts_to_date_utc(UTS)
        # store result
        json_store(FILENAME, result)
        print(result)
    except BaseException as err_:
        print(err_)
