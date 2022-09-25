#!/usr/bin/python3
""" twitter bot for hockeygraphs matchstatistics """
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import json
import time
import random
import requests
from wa_hack_cli import simple_send
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
# import project settings
# pylint: disable=C0413
from django.conf import settings
# pylint: disable=E0401, C0413
from rest.functions.helper import logger_setup, uts_now, uts_to_date_utc, config_load, json_load
from rest.functions.match import match_info_get, untweetedmatch_list_get, match_add
from rest.functions.season import season_latest_get
from rest.functions.socialnetworkevent import twitter_login, twitter_image_upload, facebook_post
from rest.functions.email import send_mail

def _config_load(logger, cfg_file=os.path.dirname(__file__)+'/'+'hockeygraphs.cfg'):
    """" load config from file """
    logger.debug('_config_load()')

    consumer_key = None
    consumer_secret = None
    oauth_token = None
    oauth_token_secret = None
    fb_token_file = None

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

    if 'Facebook' in config_dic:
        if 'token_file' in config_dic['Facebook']:
            fb_token_file = config_dic['Facebook']['token_file']

    if not (consumer_key and consumer_secret and oauth_token and oauth_token_secret):
        logger.debug('_config_load(): twitter configuration incomplete')
        sys.exit(0)

    if not fb_token_file:
        logger.debug('_config_load(): facebook configuration incomplete')
        sys.exit(0)

    logger.debug('_config_load() ended.')
    return (consumer_key, consumer_secret, oauth_token, oauth_token_secret, fb_token_file)

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
    parser.add_argument('--force', help='force execution even if already tweeted', action="store_true", default=False)
    parser.add_argument('-r', '--reply', help='post as reply to prematch stat tweet', action="store_true", default=False)
    parser.add_argument('-s', '--season', help='season id', default=None)
    mlist = parser.add_mutually_exclusive_group()
    mlist.add_argument('--matchlist', help='list of del matchids', default=[])
    mlist.add_argument('-i', '--interval', help='previous matches during last x hours', default=0)
    args = parser.parse_args()

    # default settings
    season = 0
    matchlist = None

    debug = args.debug
    fake = args.fake
    reply = args.reply
    season = args.season
    matchlist = args.matchlist
    interval = int(args.interval)
    force = args.force

    # process matchlist
    try:
        _tmp_list = matchlist.split(',')
    except BaseException:
        _tmp_list = []
    match_list = []
    for match in _tmp_list:
        match_list.append(int(match))

    if not interval and not match_list:
        print('either -i or --matchlist parameter must be specified')
        sys.exit(0)

    return(debug, fake, reply, season, match_list, interval, force)

def page_get_via_selenium(logger, url, file_):
    """ get page via selenium """
    logger.debug('get_page_via_selenium()')

    headless = True
    browser = 'Chrome'
    timeout = 10

    if browser == 'Firefox':
        logger.debug('using firefox')
        options = FirefoxOptions()
    else:
        logger.debug('using chrome')
        options = ChromeOptions()
        options.add_argument('--no-sandbox')

    if headless:
        logger.debug('activating headless mode')
        options.add_argument('-headless')

    if browser == 'Firefox':
        driver = webdriver.Firefox(firefox_options=options, executable_path='/usr/local/bin/geckodriver')
    else:
        driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/local/bin/chromedriver')

    driver.set_window_size(1024, 960)
    # open page
    try:
        driver.get(url)
    except TimeoutException:
        logger.debug('error connecting to {0}'.format(url))
        sys.exit(0)

    # time.sleep(3)
    element_present = EC.element_to_be_clickable((By.CLASS_NAME, 'heatmap-canvas'))
    WebDriverWait(driver, timeout).until(element_present)
    driver.save_screenshot(file_)

    # closing
    driver.quit()

def heatmap_image(logger, url, season_id, match_id, tmp_dir, imgid, file_size):
    """ download heatmap image """
    logger.debug('heatmap_image()')

    # build some variables
    stat_url = '{0}/matchstatistics/{1}/{2}/{3}?lang=en&disableperiod=True'.format(url, season_id, match_id, imgid + 1)
    img_file = '{0}/tmp_{1}.png'.format(tmp_dir, match_id)
    dst = '{0}/{1}-sel-{2}-0.png'.format(tmp_dir, match_id, imgid)

    # get sceenshot of heatmap
    page_get_via_selenium(logger, stat_url, img_file)

    # crop image if it exists and has a vlaid sisize
    if os.path.exists(img_file) and os.path.getsize(img_file) >= file_size:
        logger.debug('{0} found. Cropping ....'.format(img_file))
        image_crop(logger, img_file, dst)
    else:
        dst = None
    return dst

def image_crop(logger, src, dst):
    """ crop image """
    logger.debug('image_crop()')

    img = Image.open(src)
    # Setting the points for cropped image
    left = 100
    top = 165
    right = 910
    bottom = 665
    cimg = img.crop((left, top, right, bottom))
    cimg = cimg.save(dst)

def twitter_it(logger, matchinfo_dic_, img_list_, season_id, match_id_, reply_):
    """ twitter post """
    # pylint: disable=R0914
    logger.debug('twitter_it()')

    tags = '#{0}vs{1} #{0}{1} #bot1337'.format(matchinfo_dic_['home_team__shortcut'].upper(), matchinfo_dic_['visitor_team__shortcut'].upper())

    # load rebound and break interval from config file
    (consumer_key, consumer_secret, oauth_token, oauth_token_secret, _fb_token_file) = _config_load(LOGGER)

    chart_list = ['Charts', 'bunte Bildchen', 'Grafiken', 'Chartz']
    match_date = uts_to_date_utc(matchinfo_dic_['date_uts'], '%d.%m.%Y')
    text_initial = 'Hier ein paar {2} zum Spiel {0} gg. {1}. vom {5} (Endstand: {6}).\nMehr unter https://hockeygraphs.dynamop.de/matchstatistics/{3}/{4} ...'.format(matchinfo_dic_['home_team__shortcut'].upper(), matchinfo_dic['visitor_team__shortcut'].upper(), random.choice(chart_list), season_id, match_id_, match_date, matchinfo_dic_['result_full'])
    text_reply = 'Und noch die Eiszeiten pro Spieler sowie die Eiszeiten in Über- und Unterzahl... {0}'.format(tags)

    # LogIn
    twitter_uploader = twitter_login(logger, consumer_key, consumer_secret, oauth_token, oauth_token_secret, 'upload.twitter.com')
    # upload images
    id_list = twitter_image_upload(logger, twitter_uploader, img_list_)

    # add shotmap if existing
    if id_list[3]:
        id_string = '{0},{1},{2},{3}'.format(id_list[0], id_list[1], id_list[2], id_list[3])
        id_string_reply = '{0},{1},{2},{3}'.format(id_list[4], id_list[5], id_list[6], id_list[7])
    else:
        id_string = '{0},{1},{2}'.format(id_list[0], id_list[1], id_list[2])
        id_string_reply = '{0},{1},{2},{3}'.format(id_list[3], id_list[4], id_list[5], id_list[6])

    twitter_api = twitter_login(logger, consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    tweet_text = '{0} {1}'.format(text_initial, tags)
    if reply_ and 'prematch_tweet_id' in matchinfo_dic_ and matchinfo_dic_['prematch_tweet_id']:
        logger.debug('twitter_it(): tweet reply to prematch tweet {0}'.format(matchinfo_dic_['prematch_tweet_id']))
        result = twitter_api.statuses.update(status=tweet_text, media_ids=id_string, in_reply_to_status_id=matchinfo_dic_['prematch_tweet_id'])
    else:
        result = twitter_api.statuses.update(status=tweet_text, media_ids=id_string)
    id_str = result['id']
    result = twitter_api.statuses.update(status=text_reply, media_ids=id_string_reply, in_reply_to_status_id=id_str)

def fbook_it(logger, matchinfo_dic_, img_list_, season_id, match_id):
    """ facebook post """
    # pylint: disable=R0914
    logger.debug('fbook_it()')

    # load rebound and break interval from config file
    (_consumer_key, _consumer_secret, _oauth_token, _oauth_token_secret, fb_token_file) = _config_load(LOGGER)

    # get access token
    token_dic = json_load(fb_token_file)
    access_token = None
    if 'access_token' in token_dic:
        access_token = token_dic['access_token']

    # message test used in post
    match_date = uts_to_date_utc(matchinfo_dic_['date_uts'], '%d.%m.%Y')
    message = 'Hier ein paar Charts zum Spiel {0} gg. {1}. vom {2} (Endstand: {3}).\nMehr unter https://hockeygraphs.dynamop.de/matchstatistics/{4}/{5} ...'.format(matchinfo_dic['home_team__shortcut'].upper(), matchinfo_dic['visitor_team__shortcut'].upper(), match_date, matchinfo_dic['result_full'], season_id, match_id)

    # list of groups to be published
    group_list = ['1799006236944342']

    # post to facebook group
    facebook_post(logger, group_list, message, img_list_, access_token)

def get_imagesize_dic(logger):
    """ pick images to post """
    logger.debug('get_imagesize_dic()')
    source_dic = {2: 48500, 4: 55000, 7: 35000, 10: 35000}
    toi_dic = {11: 30000, 12: 30000}
    map_dic = {5: 150000, 6: 65000}

    # we always add the shot-chart
    imagesize_dic = {1: 49000}

    # pick a shotmap randomly
    for ele in random.sample(list(map_dic), k=1):
        imagesize_dic[ele] = map_dic[ele]

    # pck to other chats randomly
    for ele in random.sample(list(source_dic), k=2):
        imagesize_dic[ele] = source_dic[ele]

    # add toi chart
    for ele in toi_dic:
        imagesize_dic[ele] = toi_dic[ele]

    logger.debug('get_imagesize_dic() ended with: {0}'.format(imagesize_dic.keys()))
    return imagesize_dic

if __name__ == '__main__':

    (DEBUG, FAKE, REPLY, SEASON_ID, MATCH_ID_LIST, INTERVAL, FORCE) = arg_parse()

    URL = 'https://hockeygraphs.dynamop.de'
    MATCHSTAT = '/api/v1/matchstatistics/'
    TMP_DIR = '/tmp'

    EXPORTER_HOST = 'http://192.168.124.1'
    EXPORTER_PORT = 7801

    FILE_NAME = '/tmp/foo.json'

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # unix timestamp
    UTS = uts_now()

    if not SEASON_ID:
        # get season_id
        SEASON_ID = season_latest_get(LOGGER)

    if not MATCH_ID_LIST:
        if INTERVAL:
            MATCH_ID_LIST = untweetedmatch_list_get(LOGGER, SEASON_ID, UTS, INTERVAL*3600, ['match_id'], )

    for match_id in MATCH_ID_LIST:

        # IMGSIZE_DIC = {1: 49000, 2: 48500, 4: 55000, 5: 150000, 11: 30000, 12: 30000}
        # new image list due to wrong coordinates in shots.json
        IMGSIZE_DIC = get_imagesize_dic(LOGGER)
        print(IMGSIZE_DIC)

        # we need some match_information
        matchinfo_dic = match_info_get(LOGGER, match_id, None, ['result_suffix', 'result', 'home_team__shortcut', 'visitor_team__shortcut', 'home_team__facebook_groups', 'date_uts', 'visitor_team__facebook_groups', 'prematch_tweet_id', 'tweet'])

        if not FORCE:
            if matchinfo_dic['tweet']:
                LOGGER.info('match {0} got already tweeted. Ignoring it...'.format(match_id))
                continue

        # hack to have a better result
        if 'result_suffix' in matchinfo_dic and matchinfo_dic['result_suffix']:
            matchinfo_dic['result_full'] = '{0} {1}'.format(matchinfo_dic['result'], matchinfo_dic['result_suffix'])
        else:
            matchinfo_dic['result_full'] = matchinfo_dic['result']

        # request URL and fetch it
        RURL = '{0}{1}{2}/?language=EN&mobile=false'.format(URL, MATCHSTAT, match_id)
        response = requests.get(RURL)
        DATA = response.json()

        img_list = []
        for img_id in IMGSIZE_DIC:
            # filter out the chart
            if 'chart' in DATA[img_id]:
                # tab-chart or not
                if DATA[img_id]['tabs']:
                    for idx, chart in enumerate(DATA[img_id]['chart']):
                        img_list.append(chart_plot(LOGGER, match_id, DATA[img_id]['chart'][idx], img_id, idx, EXPORTER_HOST, EXPORTER_PORT, IMGSIZE_DIC[img_id]))
                else:
                    # get filesize for checkup
                    if img_id == 1:
                        (home_goals, visitor_goals, file_size) = corsichart_size_get(LOGGER, DATA[0])
                    else:
                        file_size = IMGSIZE_DIC[img_id]
                    if img_id == 5:
                        # special handling for heatmap
                        img_list.append(heatmap_image(LOGGER, URL, SEASON_ID, match_id, TMP_DIR, img_id, file_size))
                    else:
                        img_list.append(chart_plot(LOGGER, match_id, DATA[img_id]['chart'], img_id, 1, EXPORTER_HOST, EXPORTER_PORT, file_size))

        if img_list:
            if not FAKE:

                # update database and set post flag - we do this before posting to avoid loops due to exceptions
                match_add(LOGGER, 'match_id', match_id, {'tweet': True})

                # twitterle
                twitter_it(LOGGER, matchinfo_dic, img_list, SEASON_ID, match_id, REPLY)
                # fb-post
                fbook_it(LOGGER, matchinfo_dic, img_list, SEASON_ID, match_id)

            # temporary email
            MATCH_DATE = uts_to_date_utc(matchinfo_dic['date_uts'], '%d.%m.%Y')
            MESSAGE = 'Hier ein paar Charts zum Spiel {0} gg. {1}. vom {2} (Endstand: {3}).\nMehr unter https://hockeygraphs.dynamop.de/matchstatistics/{4}/{5} ...'.format(matchinfo_dic['home_team__shortcut'].upper(), matchinfo_dic['visitor_team__shortcut'].upper(), MATCH_DATE, matchinfo_dic['result_full'], SEASON_ID, match_id)
            SUBJECT = '{0} vs {1}'.format(matchinfo_dic['home_team__shortcut'], matchinfo_dic['visitor_team__shortcut'])
            send_mail('joern.mewes@gmail.com', 'joern.mewes@gmail.com', SUBJECT, MESSAGE, img_list, server=settings.EMAIL_HOST, username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)

            # send notification via whatsapp
            if(hasattr(settings, 'WA_ADMIN_NUMBER') and hasattr(settings, 'WA_SRV') and hasattr(settings, 'WA_PORT')):
                if matchinfo_dic['home_team__facebook_groups']:
                    matchinfo_dic['home_team__shortcut'] = '*{0}*'.format(matchinfo_dic['home_team__shortcut'])
                if matchinfo_dic['visitor_team__facebook_groups']:
                    matchinfo_dic['visitor_team__shortcut'] = '*{0}*'.format(matchinfo_dic['visitor_team__shortcut'])

                # send whatsapp message
                MESSAGE = 'hockey_graphs: tweety.py: {0} vs {1}'.format(matchinfo_dic['home_team__shortcut'].upper(), matchinfo_dic['visitor_team__shortcut'].upper())
                try:
                    simple_send(settings.WA_SRV, settings.WA_PORT, settings.WA_ADMIN_NUMBER, MESSAGE)
                except BaseException:
                    pass

            # cleanup and housekeeping
            try:
                os.remove('/tmp/tmp_{0}.png'.format(match_id))
            except Exception as _err:
                LOGGER.debug('could not delete /tmp/tmp_{0}.png'.format(match_id))
            for img in img_list:
                os.remove(img)
