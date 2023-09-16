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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
# import project settings
# pylint: disable=C0413
from django.conf import settings
# pylint: disable=E0401, C0413
from rest.functions.helper import logger_setup, uts_now, uts_to_date_utc, config_load, json_load
from rest.functions.match import match_info_get, futurematch_list_get, match_add, matchinfo_list_get
from rest.functions.season import season_latest_get
from rest.functions.socialnetworkevent import twitter_login_v1, twitter_login_v2, twitter_image_upload, tweet_send, facebook_post, social_config_load
from rest.functions.email import send_mail


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

def twitter_it(logger, uts):
    """ twitter post """
    # pylint: disable=R0914
    logger.debug('twitter_it()')


    # load rebound and break interval from config file
    (consumer_key, consumer_secret, access_token_key, access_token_secret, bearer_token, _fb_token_file) = social_config_load(logger, cfg_file=os.path.dirname(__file__)+'/'+'hockeygraphs.cfg')

    # LogIn
    twitter_v1 = twitter_login_v1(logger, consumer_key, consumer_secret, access_token_key, access_token_secret, bearer_token)

    img_list_ = ['c:/temp/r/2.gif', 'c:/temp/r/1.jpg']
    # upload images
    id_list = twitter_image_upload(logger, twitter_v1, img_list_)

    # id_list = [1701808127656472576, 1701808129795592192]

    # image ids (currently just one but you never know)
    # id_string = '{0}'.format(id_list[0], id_list[1])

    # login
    twitter_api = twitter_login_v2(logger, consumer_key, consumer_secret, access_token_key, access_token_secret)

    text = 'bump 1'
    tags = '#bot1337'
    tweet_text = '{0} {1}'.format(text, tags)


    # send tweet
    result = tweet_send(logger, twitter_api=twitter_api, tweet_text=tweet_text, id_list=[id_list[0]])

    tweet_id = result['id']

    text = 'bump 2'
    tags = '#bot1337'
    tweet_text = '{0} {1}'.format(text, tags)

    result = tweet_send(logger, twitter_api=twitter_api, tweet_text=tweet_text, id_list=[id_list[1]], in_reply_to=tweet_id)


    # store tweetid in datebase for later lookup
    #tweet_id = result['id']
    #if tweet_id:
    #    match_add(LOGGER, 'match_id', match_id_, {'prematch_tweet_id': tweet_id})

def fbook_it(logger, uts):
    """ facebook post """
    # pylint: disable=R0914
    logger.debug('fbook_it()')

    (consumer_key, consumer_secret, access_token_key, access_token_secret, bearer_token, fb_token_file) = social_config_load(logger, cfg_file=os.path.dirname(__file__)+'/'+'hockeygraphs.cfg')

    img_list_ = ['c:/temp/r/2.gif', 'c:/temp/r/1.jpg']


    # get access token
    token_dic = json_load(fb_token_file)
    access_token = None
    if 'access_token' in token_dic:
        access_token = token_dic['access_token']

    message = "test"
    # message test used in post
    # match_date = uts_to_date_utc(matchinfo_dic_['date_uts'], '%d.%m.%Y')
    # message = 'Hier ein paar Pre-Game Stats zum Spiel {0} gg. {1}. am {2}...'.format(matchinfo_dic_['home_team__shortcut'].upper(), matchinfo_dic['visitor_team__shortcut'].upper(), match_date)

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


    # twitterle
    fbook_it(LOGGER, UTS)

