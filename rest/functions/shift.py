# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Shift

def shift_add(fkey, fvalue, data_dic):
    """ add team to database """
    # add shift
    obj, _created = Shift.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
    obj.save()
    return obj.shift_id
