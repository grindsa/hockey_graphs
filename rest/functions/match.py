# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Match

def match_list_get(fkey=None, fvalue=None, vlist=('match_id', 'secaon', 'date', 'date_uts', 'home_team', 'visitior_team')):
    """ query team(s) from database based with optional filtering """
    if fkey:
        if len(vlist) == 1:
            match_list = Match.objects.filter(**{fkey: fvalue}).order_by('match_id').values_list(vlist[0], flat=True)
        else:
            match_list = Match.objects.filter(**{fkey: fvalue}).order_by('match_id').values(*vlist)
    else:
        if len(vlist) == 1:
            match_list = Match.objects.all().order_by('match_id').values_list(vlist[0], flat=True)
        else:
            match_list = Match.objects.all().order_by('match_id').values(*vlist)
    return list(match_list)

def match_add(fkey, fvalue, data_dic):
    """ add team to database """
    # add authorization
    obj, _created = Match.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
    obj.save()
    return obj.match_id
