#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time
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
from rest.functions.helper import logger_setup

def page_get_via_selenium(logger, url, file_):
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
        driver = webdriver.Firefox(firefox_options=options)
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
    logger.debug('heatmap_image()')

    # build some variables
    stat_url = '{0}/matchstatistics/{1}/{2}/6'.format(url, season_id, match_id)
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
    logger.debug('image_crop()')

    img = Image.open(src)
    # Setting the points for cropped image
    left = 100
    top = 165
    right = 910
    bottom = 665
    cimg = img.crop((left, top, right, bottom))
    cimg = cimg.save(dst)

if __name__ == '__main__':

    DEBUG = True
    TMP_DIR = '/tmp'
    URL = 'https://hockeygraphs.dynamop.de'

    SEASON_ID = 3
    MATCH_ID = 1911
    # initialize logger
    LOGGER = logger_setup(DEBUG)
    IMG_ID = 5

    FILE_SIZE = 150000

    filename = heatmap_image(LOGGER, URL, SEASON_ID, MATCH_ID, TMP_DIR, IMG_ID, FILE_SIZE)
    print(filename)

    list = ['foo', 'foo', None, 'bsbs']
    list.append(None)
    list.append('tata')
    print(len(list))
    if list[2]:
        print('jupp')
    else:
        print('nope')
