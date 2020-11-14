# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()

from rest.models import Gameheader
from rest.functions.chartparameters import chart_color5, chart_color6

def gameheader_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('gameheader_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add event
        obj, _created = Gameheader.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in gameheader_add(): {0}'.format(err_))
        result = None
    logger.debug('gameheader_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def gameheader_get(logger, fkey, fvalue, vlist=('match_id', 'period_event')):
    """ get info for a specifc match_id """
    logger.debug('gameheader_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            event_dic = list(Gameheader.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            event_dic = Gameheader.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except BaseException:
        event_dic = {}
    return event_dic
