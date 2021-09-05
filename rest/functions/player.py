# -*- coding: utf-8 -*-
""" list of functions for player """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Player, Playerperseason
from rest.functions.helper import list2dic

def player_dic_get(logger):
    """ query players(s) and return a dict """
    logger.debug('player_dic_get()')

    player_list = player_list_get(logger, None, None, ['player_id', 'first_name', 'last_name', 'jersey', 'stick', 'weight',  'height'])
    player_dic = list2dic(logger, player_list, 'player_id')

    return player_dic

def player_list_get(logger, fkey=None, fvalue=None, vlist=('player_id', 'first_name', 'last_name', 'jersey')):
    """ query player(s) from database based with optional filtering """
    try:
        if fkey:
            if len(vlist) == 1:
                player_list = Player.objects.filter(**{fkey: fvalue}).order_by('player_id').values_list(vlist[0], flat=True)
            else:
                player_list = Player.objects.filter(**{fkey: fvalue}).order_by('player_id').values(*vlist)
        else:
            if len(vlist) == 1:
                player_list = Player.objects.all().order_by('player_id').values_list(vlist[0], flat=True)
            else:
                player_list = Player.objects.all().order_by('player_id').values(*vlist)
    except BaseException as err_:
        logger.critical('error in player_list_get(): {0}'.format(err_))
        player_list = []
    return list(player_list)

def player_add(logger, fkey, fvalue, data_dic):
    """ add player to database """
    logger.debug('player_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add authorization
        obj, _created = Player.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.player_id
    except BaseException as err_:
        logger.critical('error in player_add(): {0}'.format(err_))
        result = None
    logger.debug('player_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def playerperseason_add(logger, player_id, season_id, data_dic):
    """ add player to database """
    logger.debug('playerperseason_add({0}:{1})'.format(player_id, season_id))
    try:
        # add authorization
        obj, _created = Playerperseason.objects.update_or_create(player_id=player_id, season_id=season_id, defaults=data_dic)
        obj.save()
        result = obj.player_id
    except BaseException as err_:
        logger.critical('error in playerperseason_add(): {0}'.format(err_))
        result = None
    logger.debug('playerperseason_add({0}:{1}) ended with {2}'.format(player_id, season_id, result))
    return result
