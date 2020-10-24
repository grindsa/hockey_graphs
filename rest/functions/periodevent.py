# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
import math
from rest.models import Periodevent

def periodevent_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('periodevent_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add event
        obj, _created = Periodevent.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in periodevent_add(): {0}'.format(err_))
        result = None
    logger.debug('periodevent_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def periodevent_get(logger, match_id, vlist=('match_id', 'period_event')):
    """ get info for a specifc match_id """
    logger.debug('periodevent_get({0})'.format(match_id))
    try:
        event_dic = Periodevent.objects.filter(match_id=match_id).values(*vlist)[0]
    except:
        event_dic = {}
    return event_dic

def penaltyplotlines_get(logger, matchid, home_color='#e6e6ff', visitor_color='#f1f2f3'):
    """ create plotlines for penalites """
    logger.debug('penalty_plotlines_get({0})'.format(matchid))

    # get periodevents
    event_dic = periodevent_get(logger, matchid)
    plotline_list = []

    for period in event_dic['period_event']:
        for event in event_dic['period_event'][period]:
            # filter penalties
            if event['type'] == 'penalty':
                # convert time to minute
                min_from = math.ceil(event['data']['time']['from']['scoreboardTime']/60)
                min_to = math.ceil(event['data']['time']['to']['scoreboardTime']/60)
                # create dictionary
                tmp_dic = {'from': min_from, 'to': min_to}
                if event['data']['team'] == 'home':
                    tmp_dic['color'] = home_color
                elif event['data']['team'] == 'visitor':
                    tmp_dic['color'] = visitor_color

                # append dictionary to list
                plotline_list.append(tmp_dic)
    return plotline_list
