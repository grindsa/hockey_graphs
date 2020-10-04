# -*- coding: utf-8 -*-
""" unittests for periodeventss.py """
# pylint: disable= C0415, W0212
import sys
from django.test import TestCase
from rest.functions.helper import testdata_load

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class PeriodeventTestCase(TestCase):
    """ periodevents test class """
    def setUp(self):
        """ setup test environment """
        from rest.functions.periodevent import periodevent_add
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')
        self.periodevent_add = periodevent_add
        testdata_load()
        from rest.models import Match
        Match.objects.create(match_id=3, season_id=1, date="2020-12-05", date_uts=1606894220, home_team_id=1, visitor_team_id=2, result='3:1')

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_periodevent_add(self):
        """ test periodevent_add"""
        self.assertEqual(3, self.periodevent_add(self.logger, 'match_id', 3, {'period_event': {'foo': 'bar3'}}))

    def test_002_periodevent_add(self):
        """ test periodevent_add"""
        err_msg = "CRITICAL:test_hockey:error in periodevent_add(): Invalid field name(s) for model Periodevent: 'event'."
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.periodevent_add(self.logger, 'match_id', 3, {'event': {'foo': 'bar3'}}))
        self.assertIn(err_msg, lcm.output)

    def test_003_periodevents_add(self):
        """ test periodevent_add for existing entry"""
        self.assertEqual(2, self.periodevent_add(self.logger, 'match_id', 2, {'period_event': {'foo': 'bar2'}}))

    def test_004_periodevents_add(self):
        """ test periodevent_add for existing entry"""
        self.assertEqual(2, self.periodevent_add(self.logger, 'match_id', 2, {'period_event': {'foo': 'bar 2'}}))
