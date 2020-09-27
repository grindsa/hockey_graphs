# -*- coding: utf-8 -*-
""" list of functions for player """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Player

def player_list_get(fkey=None, fvalue=None, vlist=('player_id', 'first_name', 'last_name', 'jersey')):
    """ query player(s) from database based with optional filtering """
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
    return list(player_list)

def player_add(fkey, fvalue, data_dic):
    """ add team to database """
    # add authorization
    obj, _created = Player.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
    obj.save()
    return obj.player_id
