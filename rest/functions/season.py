# -*- coding: utf-8 -*-
""" list of functions for seasons """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Season

def season_latest_get(logger):
    """get latest season"""
    logger.debug('season_latest_get()')
    try:
        result = len(Season.objects.values())
    except BaseException as err_:
        logger.critical('error in season_latest_get(): {0}'.format(err_))
        result = None
        print('bubu')
    logger.debug('season_latest_get() ended with {0}'.format(result))
    return result
