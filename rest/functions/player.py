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
from rest.functions.season import season_get

def u23_player_list_get(logger, season_id):
    """ get list of u23 players """

    u23_maxyear = season_get(logger, 'id', season_id, ['u23year'])

    _player_list = playerperseason_list_get(logger, 'season_id', season_id)

    player_dic = {}
    # filter player based on birthdate
    for player in _player_list:
        if 'player__birthdate' in player and player['player__birthdate']:
            (byear, _bmon, _bday) = player['player__birthdate'].split('-', 2)

            if u23_maxyear <= int(byear):
                player_dic[player['player_id']] = {
                    'player_id': player['player_id'],
                    'team_id': player['player__team'],
                    'shortcut': player['player__team__shortcut'],
                    'first_name': player['player__first_name'],
                    'last_name': player['player__last_name'],
                    'jersey': player['player__jersey'],
                }

    return player_dic

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

def playerperseason_list_get(logger, fkey=None, fvalue=None, vlist=('player_id', 'player__first_name', 'player__last_name', 'player__jersey', 'player__birthdate', 'player__team', 'player__team__shortcut')):
    """ query player(s) from database based with optional filtering """
    try:
        if fkey:
            if len(vlist) == 1:
                player_list = Playerperseason.objects.filter(**{fkey: fvalue}).order_by('player_id').values_list(vlist[0], flat=True)
            else:
                player_list = Playerperseason.objects.filter(**{fkey: fvalue}).order_by('player_id').values(*vlist)
        else:
            if len(vlist) == 1:
                player_list = Playerperseason.objects.all().order_by('player_id').values_list(vlist[0], flat=True)
            else:
                player_list = Playerperseason.objects.all().order_by('player_id').values(*vlist)
    except BaseException as err_:
        logger.critical('error in player_list_get(): {0}'.format(err_))
        player_list = []
    return list(player_list)