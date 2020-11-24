# -*- coding: utf-8 -*-
""" list of functions for team comparison """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.functions.helper import url_build
from rest.functions.season import seasonid_get

def teamcomparison_get(logger, request, fkey=None, fvalue=None):
    """ matchstatistics grouped by days """
    logger.debug('teamcomparison_get({0}:{1})'.format(fkey, fvalue))

    (_fkey, season_id) = seasonid_get(logger, request)

    result = {_fkey: season_id}

    return result
