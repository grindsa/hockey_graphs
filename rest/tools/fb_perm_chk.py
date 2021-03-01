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
from rest.functions.helper import logger_setup, uts_now, uts_to_date_utc, config_load, json_load

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='fb_token_check.py - check validity of user-access token')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-i', '--input', help='destination file', default='fb-ua-token.json')
    args = parser.parse_args()

    debug = args.debug
    input_file = args.input

    return(debug, input_file)

if __name__ == '__main__':

    (DEBUG, FILENAME) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    TOKEN_DIC = json_load(FILENAME)

    ACCESS_TOKEN = None
    if 'access_token' in TOKEN_DIC:
        ACCESS_TOKEN = TOKEN_DIC['access_token']

    # get USERID
    ME_URL = "https://graph.facebook.com/v10.0/me"
    data_dic = {
        'access_token': ACCESS_TOKEN
    }
    req = requests.get(ME_URL, params=data_dic)
    result = req.json()
    name = result['name']
    user_id = result['id']

    print('name: {0}'.format(name))
    print('user_id: {0}'.format(user_id))

    # get access-rights
    ACC_URL = "https://graph.facebook.com/v10.0/{0}/accounts".format(user_id)

    req = requests.get(ACC_URL, params=data_dic)
    result = req.json()

    from pprint import pprint
    pprint(result)

    # check access
    CHK_URL = 'https://graph.facebook.com/1260098154385578/feed'

    req = requests.get(CHK_URL, params=data_dic)
    result = req.json()

    from pprint import pprint
    pprint(result)
