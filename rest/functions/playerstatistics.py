# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413, R0914
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.functions.bananachart import banana_chart1_create, banana_chart2_create
from rest.functions.helper import url_build, mobile_check

def playerstatistics_get(logger, request, season_pk=None, player_pk=None):
    """ matchstatistics grouped by days """
    logger.debug('matchstatistics_get({0}:{1})'.format(season_pk, player_pk))

    # pint(request.META)

    ismobile = mobile_check(logger, request)

    # fkey = 'match_id'
    # fvalue = 1804

    # we protect the REST and will not return anything without matchid
    if season_pk and player_pk:
        # we need some match_information
        result = []

        # get matchstatistics
        result.append(banana_chart1_create(logger, 'title1'))
        result.append(banana_chart2_create(logger, 'title2'))

        print(season_pk, player_pk )
        pass
    else:
        result = {'error': 'Please specify a season and player'}

    return result
