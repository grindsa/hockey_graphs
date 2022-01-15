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
from rest.functions.match import match_info_get, futurematch_list_get, match_add, matchinfo_list_get
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


def arg_parse():
    """ simple argparser """
    parser = argparse.ArgumentParser(description='match_import.py - update matches in database')
    parser.add_argument('-d', '--debug', help='debug mode', action="store_true", default=False)
    parser.add_argument('-f', '--fake', help='fake mode', action="store_true", default=False)
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
    season = args.season
    matchlist = args.matchlist
    interval = int(args.interval)

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

    return(debug, fake, season, match_list, interval)

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
    element_present = EC.element_to_be_clickable((By.CLASS_NAME, 'content'))
    WebDriverWait(driver, timeout).until(element_present)
    driver.save_screenshot(file_)

    # closing
    driver.quit()

def prematch_overview(logger, url, season_id, match_id, tmp_dir):
    """ download heatmap image """
    logger.debug('prematch_overview()')

    # build some variables
    stat_url = '{0}/matchstatistics/{1}/{2}/{3}?lang=en&disableperiod=True'.format(url, season_id, match_id, 1)
    img_file = '{0}/tmp_{1}.png'.format(tmp_dir, match_id)
    dst = '{0}/{1}-sel-{2}-0.png'.format(tmp_dir, match_id, 1)

    # get sceenshot of heatmap
    page_get_via_selenium(logger, stat_url, img_file)

    #crop image if it exists and has a vlaid sisize
    if os.path.exists(img_file):
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
    left = 99
    top = 165
    right = 910
    bottom = 613
    cimg = img.crop((left, top, right, bottom))
    cimg = cimg.save(dst)

def twitter_it(logger, matchinfo_dic_, img_list_, season_id, match_id_):
    """ twitter post """
    # pylint: disable=R0914
    logger.debug('twitter_it()')

    tags = '#{0}vs{1} #{0}{1} #bot1337'.format(matchinfo_dic_['home_team__shortcut'].upper(), matchinfo_dic_['visitor_team__shortcut'].upper())

    # load rebound and break interval from config file
    (consumer_key, consumer_secret, oauth_token, oauth_token_secret, _fb_token_file) = _config_load(LOGGER)

    match_date = uts_to_date_utc(matchinfo_dic_['date_uts'], '%d.%m.%Y')
    text = 'Hier ein paar Pre-Game Stats zum Spiel {0} gg. {1}. am {2}...'.format(matchinfo_dic_['home_team__shortcut'].upper(), matchinfo_dic['visitor_team__shortcut'].upper(), match_date)

    # LogIn
    twitter_uploader = twitter_login(logger, consumer_key, consumer_secret, oauth_token, oauth_token_secret, 'upload.twitter.com')
    # upload images
    id_list = twitter_image_upload(logger, twitter_uploader, img_list_)

    # image ids (currently just one but you never know)
    id_string = '{0}'.format(id_list[0])
    # login
    twitter_api = twitter_login(logger, consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    tweet_text = '{0} {1}'.format(text, tags)
    # send tweet
    result = twitter_api.statuses.update(status=tweet_text, media_ids=id_string)

    # store tweetid in datebase for later lookup
    tweet_id = result['id']
    if tweet_id:
        match_add(LOGGER, 'match_id', match_id_, {'prematch_tweet_id': tweet_id})

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
    message = 'Hier ein paar Pre-Game Stats zum Spiel {0} gg. {1}. am {2}...'.format(matchinfo_dic_['home_team__shortcut'].upper(), matchinfo_dic['visitor_team__shortcut'].upper(), match_date)

    # list of groups to be published
    group_list = ['1799006236944342']

    # post to facebook group
    facebook_post(logger, group_list, message, img_list_, access_token)


if __name__ == '__main__':

    (DEBUG, FAKE, SEASON_ID, MATCH_ID_LIST, INTERVAL) = arg_parse()

    URL = 'https://hockeygraphs.dynamop.de'
    MATCHSTAT = '/api/v1/matchstatistics/'
    TMP_DIR = '/tmp'

    # initialize logger
    LOGGER = logger_setup(DEBUG)

    # unix timestamp
    UTS = uts_now()

    if not SEASON_ID:
        # get season_id
        SEASON_ID = season_latest_get(LOGGER)

    MATCH_STAT_LIST = []
    if not MATCH_ID_LIST:
        if INTERVAL:
            MATCH_STAT_LIST = futurematch_list_get(LOGGER, SEASON_ID, UTS, INTERVAL*3600, ['match_id', 'prematch_tweet_id'])
    else:
        match_dic = matchinfo_list_get(LOGGER, MATCH_ID_LIST, None, ['match_id', 'prematch_tweet_id'])
        for match_id in match_dic:
            MATCH_STAT_LIST.append(match_dic[match_id])

    if MATCH_STAT_LIST:
        for match in MATCH_STAT_LIST:
            img_list = []
            if not match['prematch_tweet_id']:
                img_list.append(prematch_overview(LOGGER, URL, SEASON_ID, match['match_id'], TMP_DIR))
                if img_list:
                    matchinfo_dic = match_info_get(LOGGER, match['match_id'], None)
                    if not FAKE:
                        # twitterle
                        twitter_it(LOGGER, matchinfo_dic, img_list, SEASON_ID, match['match_id'])
                        # fb-post
                        fbook_it(LOGGER, matchinfo_dic, img_list, SEASON_ID, match_id)

                    # send notification via whatsapp
                    if(hasattr(settings, 'WA_ADMIN_NUMBER') and hasattr(settings, 'WA_SRV') and hasattr(settings, 'WA_PORT')):
                        if matchinfo_dic['home_team__facebook_groups']:
                            matchinfo_dic['home_team__shortcut'] = '*{0}*'.format(matchinfo_dic['home_team__shortcut'])
                        if matchinfo_dic['visitor_team__facebook_groups']:
                            matchinfo_dic['visitor_team__shortcut'] = '*{0}*'.format(matchinfo_dic['visitor_team__shortcut'])

                        # send whatsapp message
                        MESSAGE = 'hockey_graphs: tweety_prematch.py: {0} vs {1}'.format(matchinfo_dic['home_team__shortcut'].upper(), matchinfo_dic['visitor_team__shortcut'].upper())
                        try:
                            simple_send(settings.WA_SRV, settings.WA_PORT, settings.WA_ADMIN_NUMBER, MESSAGE)
                        except BaseException:
                            pass

                    os.remove('/tmp/tmp_{0}.png'.format(match['match_id']))
                    for img in img_list:
                        os.remove(img)
