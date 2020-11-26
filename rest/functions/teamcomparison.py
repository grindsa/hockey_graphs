# -*- coding: utf-8 -*-
""" list of functions for team comparison """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.functions.season import seasonid_get
from rest.functions.bananachart import banana_chart1_create, banana_chart2_create

def teamcomparison_get(logger, request, fkey=None, fvalue=None):
    """ matchstatistics grouped by days """
    logger.debug('teamcomparison_get({0}:{1})'.format(fkey, fvalue))

    (_fkey, _season_id) = seasonid_get(logger, request)

    result = []

    result.append(banana_chart1_create(logger, 'foo1'))
    result.append(banana_chart2_create(logger, 'foo2'))


    return result
