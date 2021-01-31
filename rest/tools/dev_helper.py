#!/usr/bin/python
# -*- coding: utf-8 -*-
""" this is just a wrapper to help in development """
import sys
import os
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()

from rest.functions.helper import logger_setup
from rest.functions.matchstatistics import matchstatistics_get
from rest.functions.teamcomparison import teamcomparison_get
import gettext

en = gettext.translation('django', localedir='locale', languages=['en'])
en.install()


class Request:
    pass

if __name__ == '__main__':


    LOGGER = logger_setup(True)

    request = Request()
    request.META = {'foo': 'bar'}

    FKEY = 'match_id'
    FVALUE = 1853

    # result = matchstatistics_get(LOGGER, request, FKEY, FVALUE)
    result = teamcomparison_get(LOGGER, request, FKEY, FVALUE)

    # from pprint import pprint
    # pprint(result)
