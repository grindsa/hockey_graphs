# -*- coding: utf-8 -*-
""" unittests for teams.py """
# pylint: disable= C0415, W0212
import sys
from django.test import TestCase
from rest.models import Season

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class TeamTestCase(TestCase):
    """ team test class """
    def setUp(self):
        """ setup test environment """
        from rest.functions.season import season_latest_get
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')
        self.season_latest_get = season_latest_get
        Season.objects.create(name="Season-1")
        Season.objects.create(name="Season-2")

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_season_latest_get(self):
        """ test season_latest_get """
        self.assertEqual(2, self.season_latest_get(self.logger))
