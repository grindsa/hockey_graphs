# -*- coding: utf-8 -*-
""" unittests for shiftss.py """
# pylint: disable= C0415, W0212
import sys
from django.test import TestCase
from rest.functions.helper import testdata_load

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class ShiftTestCase(TestCase):
    """ shifts test class """
    def setUp(self):
        """ setup test environment """
        from rest.functions.shift import shift_add
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')
        self.shift_add = shift_add
        testdata_load()
        from rest.models import Match
        Match.objects.create(match_id=3, season_id=1, date="2020-12-05", date_uts=1606894220, home_team_id=1, visitor_team_id=2, result='3:1')

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_shift_add(self):
        """ test shift_add"""
        self.assertEqual(3, self.shift_add(self.logger, 'match_id', 3, {'shift': {'foo': 'bar3'}}))

    def test_002_shift_add(self):
        """ test shifts_add"""
        err_msg = "CRITICAL:test_hockey:error in shift_add(): Invalid field name(s) for model Shift: 'shot'."
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.shift_add(self.logger, 'match_id', 3, {'shot': {'foo': 'bar3'}}))
        self.assertIn(err_msg, lcm.output)

    def test_003_shift_add(self):
        """ test  shifts_add for existing entry"""
        self.assertEqual(2, self.shift_add(self.logger, 'match_id', 2, {'shift': {'foo': 'bar2'}}))

    def test_004_shift_add(self):
        """ test  shifts_add for existing entry"""
        self.assertEqual(2, self.shift_add(self.logger, 'match_id', 2, {'shift': {'foo': 'bar 2'}}))
