#!/usr/bin/python3
""" little utility to extend an existing facebook user-access token """
# -*- coding: utf-8 -*-
import os
import sys
import argparse
from wa_hack_cli import simple_send
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
# import project settings
# pylint: disable=C0413, E0401, W0611
import django
from django.conf import settings
from rest.functions.helper import logger_setup, uts_now, json_load
django.setup()

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='fb_token_check.py - check validity of user-access token')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-i', '--input', help='destination file', default='fb-ua-token.json')
    parser.add_argument('-t', '--threshold', help='threshold in days', default=7)
    args = parser.parse_args()

    debug = args.debug
    input_file = args.input
    try:
        threshold = int(args.threshold) * 86400
    except BaseException:
        threshold = 604800

    return(debug, input_file, threshold)

if __name__ == '__main__':

    (DEBUG, INPUT_FILE, THRESHOLD) = arg_parse()

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # unix timestamp
    UTS = uts_now()

    # load token from file
    TOKEN_DIC = json_load(INPUT_FILE)

    ERROR = None
    if 'expires_in' in TOKEN_DIC and 'uts' in TOKEN_DIC:
        token_expiry = TOKEN_DIC['expires_in']  + TOKEN_DIC['uts']

        if token_expiry - UTS < THRESHOLD:
            ERROR = 'fb-token goken is going to expire in {0}s'.format(token_expiry - UTS)

    else:
        ERROR = 'wrong token content'

    # send notification via whatsapp
    if(ERROR and hasattr(settings, 'WA_ADMIN_NUMBER') and hasattr(settings, 'WA_SRV') and hasattr(settings, 'WA_PORT')):
        # send whatsapp message
        MESSAGE = 'hockey_graphs: fb_token_chk.py: {0}'.format(ERROR)
        try:
            simple_send(settings.WA_SRV, settings.WA_PORT, settings.WA_ADMIN_NUMBER, MESSAGE)
        except BaseException:
            pass
