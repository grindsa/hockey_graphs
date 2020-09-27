# -*- coding: utf-8 -*-
""" list of functions for seasons """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Season

def season_latest_get():
    """get latest season"""
    # get season_id
    return len(Season.objects.values())
