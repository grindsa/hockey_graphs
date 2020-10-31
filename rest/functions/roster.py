# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Roster

def roster_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('roster_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add roster
        obj, _created = Roster.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in roster_add(): {0}'.format(err_))
        result = None
    logger.debug('roster_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def roster_get(logger, fkey, fvalue, vlist=('match_id', 'roster')):
    """ get info for a specifc match_id """
    logger.debug('roster_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            roster_dic = list(Roster.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            roster_dic = Roster.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except:
        roster_dic = {}

    return roster_dic
