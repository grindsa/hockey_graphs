#!/usr/bin/python3
""" create matchday summary hockeygraphs matchstatistics """
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import json
from datetime import date
import time
import requests
from wa_hack_cli import simple_send
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
# import project settings
# pylint: disable=C0413
from django.conf import settings
# pylint: disable=E0401, C0413
from rest.functions.helper import logger_setup, uts_now, uts_to_date_utc, date_to_uts_utc, config_load, json_load
from rest.functions.match import match_info_get, sincematch_list_get
from rest.functions.season import season_latest_get
from rest.functions.socialnetworkevent import facebook_post

def _config_load(logger, cfg_file=os.path.dirname(__file__)+'/'+'hockeygraphs.cfg'):
    """" load config from file """
    logger.debug('_config_load()')

    fb_token_file = None

    config_dic = config_load(cfg_file=cfg_file)

    if 'Facebook' in config_dic:
        if 'token_file' in config_dic['Facebook']:
            fb_token_file = config_dic['Facebook']['token_file']

    if not fb_token_file:
        logger.debug('_config_load(): facebook configuration incomplete')
        sys.exit(0)

    logger.debug('_config_load() ended.')
    return fb_token_file

def convert_graph(logger, url, data, file_name):
    """ send data to server """
    logger.debug('convert_graph() for {0}'.format(file_name))

    headers = {'Content-Type': 'application/json'}
    try:
        api_response = requests.post(url=url, data=data, headers=headers, verify=False, timeout=15)
        # pylint: disable=R1705
        if api_response.ok and api_response.content:
            logger.debug('We got something useful back. Lets dump it into a file')
            with open(file_name, "wb") as binary_file:
                binary_file.write(api_response.content)
            return (True, None)
        else:
            logger.debug('Something went south. We got response code: {0}'.format(api_response.status_code))
            # err = api_response.raise_for_status()
            return (False, api_response.status_code)

    except BaseException as _err:
        logger.debug('Connection error')
        return(None, 'Connection error')

def chart_plot(logger, matchid, data, imgid, idx_, exporter_host, exporter_port, fsize):
    """ create images and validate file-size """
    logger.debug('chart_plot()')

    img_name = '{0}/{2}-sel-{1}-{3}.png'.format(TMP_DIR, imgid, matchid, idx_)
    for ele in range(0, 5):
        try:
            logger.debug('fsize: {0} calculated: {1}'.format(os.path.getsize(img_name), fsize))
        except BaseException:
            pass

        # pylint: disable=R1723
        if ele > 2 and os.path.exists(img_name) and os.path.getsize(img_name) >= fsize:
            # seems the be right
            logger.debug('filesize is right')
            break
        else:
            stat_chart = json.dumps({'asyncRendering': 'true', 'infile': data})
            (_result, cerr) = convert_graph(LOGGER, '{0}:{1}'.format(exporter_host, exporter_port), stat_chart, img_name)
            if cerr:
                logger.debug('error during convert_graph: {0}: {1}'.format(cerr, img_name))
            time.sleep(1)

    return img_name

def corsichart_size_get(logger, data):
    """ get expected filesize for corsi-chart """
    logger.debug('corsichart_size_get()')

    homegoals = data['chart']['home_team']['shotsOnGoal'] - data['chart']['visitor_team']['saves']
    visitorgoals = data['chart']['visitor_team']['shotsOnGoal'] - data['chart']['home_team']['saves']

    sum_goals = homegoals + visitorgoals
    # calculate expected filesize
    start_value = 40050
    name_value = 555
    logo_value = 500
    xf_size = start_value + sum_goals * (name_value + logo_value)

    if xf_size <= 43000:
        logger.debug('flip-over and set the filesize to 43000')
        xf_size = 43000

    return (homegoals, visitorgoals, xf_size)

def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='match_import.py - update matches in database')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-f', '--fake', help='fake mode', action="store_true", default=False)
    parser.add_argument('--date', help='specify match date', default=None)
    mlist = parser.add_mutually_exclusive_group()
    mlist.add_argument('--matchlist', help='list of del matchids', default=[])
    args = parser.parse_args()

    # default settings
    matchlist = None

    debug = args.debug
    fake = args.fake
    matchlist = args.matchlist
    matchdate = args.date

    # process matchlist
    try:
        _tmp_list = matchlist.split(',')
    except BaseException:
        _tmp_list = []
    match_list = []
    for match_ in _tmp_list:
        match_list.append(int(match_))

    return(debug, fake, match_list, matchdate)

def fbook_it(logger, img_list_, message):
    """ facebook post """
    # pylint: disable=R0914
    logger.debug('fbook_it()')

    # load rebound and break interval from config file
    fb_token_file = _config_load(LOGGER)

    # get access token
    token_dic = json_load(fb_token_file)
    access_token = None
    if 'access_token' in token_dic:
        access_token = token_dic['access_token']

    # list of groups to be published
    group_list = ['1799006236944342']

    # post to facebook group
    facebook_post(logger, group_list, message, img_list_, access_token)


if __name__ == '__main__':

    (DEBUG, FAKE, MATCH_ID_LIST, MATCHDATE) = arg_parse()

    URL = 'https://hockeygraphs.dynamop.de'
    MATCHSTAT = '/api/v1/matchstatistics/'
    TMP_DIR = '/tmp'

    EXPORTER_HOST = 'http://192.168.124.1'
    EXPORTER_PORT = 7801

    FILE_NAME = '/tmp/foo.json'

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    if MATCHDATE:
        TODAY = MATCHDATE
        UTS = date_to_uts_utc('{0} 23:59:59'.format(TODAY)) + 1
    else:
        # unix timestamp
        UTS = uts_now()
        TODAY = date.today().strftime('%d.%m.%Y')
    LOGGER.debug('matchdate: {0}, uts: {1}'.format(TODAY, UTS))

    # get season_id
    SEASON_ID = season_latest_get(LOGGER)

    if not MATCH_ID_LIST:
        DELTA = UTS - date_to_uts_utc(TODAY, '%d.%m.%Y')
        if UTS and DELTA:
            MATCH_ID_LIST = sincematch_list_get(LOGGER, SEASON_ID, UTS, DELTA, ['match_id'], )

    IMGSIZE_DIC = {1: 49000, 2: 48500, 4: 55000}
    IMG_LIST = []
    # empty list to store results
    RESULT_LIST = []

    # create images per match
    if MATCH_ID_LIST:
        for match_id in MATCH_ID_LIST:

            # we need some match_information
            matchinfo_dic = match_info_get(LOGGER, match_id, None)

            # hack to have a better result
            if 'result_suffix' in matchinfo_dic and matchinfo_dic['result_suffix']:
                matchinfo_dic['result_full'] = '{0} {1}'.format(matchinfo_dic['result'], matchinfo_dic['result_suffix'])
            else:
                matchinfo_dic['result_full'] = matchinfo_dic['result']

            # add matchline to list
            RESULT_LIST.append('{0} gg. {1}: {2}'.format(matchinfo_dic['home_team__shortcut'].upper(), matchinfo_dic['visitor_team__shortcut'].upper(), matchinfo_dic['result_full']))

            # request URL and fetch it
            RURL = '{0}{1}{2}/?language=EN&mobile=false'.format(URL, MATCHSTAT, match_id)
            response = requests.get(RURL)
            DATA = response.json()
            for img_id in IMGSIZE_DIC:
                # filter out the chart
                if 'chart' in DATA[img_id]:
                    # tab-chart or not
                    if DATA[img_id]['tabs']:
                        for idx, chart in enumerate(DATA[img_id]['chart']):
                            IMG_LIST.append(chart_plot(LOGGER, match_id, DATA[img_id]['chart'][idx], img_id, idx, EXPORTER_HOST, EXPORTER_PORT, IMGSIZE_DIC[img_id]))
                    else:
                        # get filesize for checkup
                        if img_id == 1:
                            (home_goals, visitor_goals, file_size) = corsichart_size_get(LOGGER, DATA[0])
                        IMG_LIST.append(chart_plot(LOGGER, match_id, DATA[img_id]['chart'], img_id, 1, EXPORTER_HOST, EXPORTER_PORT, file_size))

    if IMG_LIST and RESULT_LIST:
        if not FAKE:

            # create message
            MESSAGE = 'Hier ein paar Charts zu den Penny DEL Spielen vom {0}\n\n'.format(TODAY)
            for match in RESULT_LIST:
                MESSAGE = '{0} {1}\n'.format(MESSAGE, match)

            MESSAGE = '{0}\nMehr unter https://hockeygraphs.dynamop.de/matchstatistics/{1}\n'.format(MESSAGE, SEASON_ID)

            # post to facebook
            fbook_it(LOGGER, IMG_LIST, MESSAGE)

        # send notification via whatsapp
        if(hasattr(settings, 'WA_ADMIN_NUMBER') and hasattr(settings, 'WA_SRV') and hasattr(settings, 'WA_PORT')):

            # send whatsapp message
            MESSAGE = 'hockey_graphs: Summary {0}'.format(TODAY)
            try:
                simple_send(settings.WA_SRV, settings.WA_PORT, settings.WA_ADMIN_NUMBER, MESSAGE)
            except BaseException:
                pass

        # cleanup and housekeeping
        for img in IMG_LIST:
            os.remove(img)
