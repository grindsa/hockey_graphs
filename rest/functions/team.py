# -*- coding: utf-8 -*-
""" list of functions for teams """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Team

def team_list_get(fkey=None, fvalue=None, vlist=('team_id', 'team_name', 'short_name')):
    """ query team(s) from database based with optional filtering """
    if fkey:
        if len(vlist) == 1:
            team_list = Team.objects.filter(**{fkey: fvalue}).order_by('team_id').values_list(vlist[0], flat=True)
        else:
            team_list = Team.objects.filter(**{fkey: fvalue}).order_by('team_id').values(*vlist)
    else:
        if len(vlist) == 1:
            team_list = Team.objects.all().order_by('team_id').values_list(vlist[0], flat=True)
        else:
            team_list = Team.objects.all().order_by('team_id').values(*vlist)
    return list(team_list)

def team_add(fkey, fvalue, data_dic):
    """ add team to database """
    # add authorization
    obj, _created = Team.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
    obj.save()
    return obj.team_id
