# -*- coding: utf-8 -*-
""" unittests for matchs.py """
# pylint: disable= C0415, W0212
import sys
from django.test import TestCase
from rest.functions.helper import testdata_load

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class MatchTestCase(TestCase):
    """ Match test class """
    def setUp(self):
        """ setup test environment """
        from rest.functions.match import match_list_get, match_add
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')
        self.match_list_get = match_list_get
        self.match_add = match_add
        testdata_load()

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_match_list_get(self):
        """ test match_list get with no filter"""
        match_list = [{'match_id': 1, 'season': 1, 'date': '2020-12-01', 'date_uts': 1606807800, 'home_team': 1, 'visitor_team': 2}, {'match_id': 2, 'season': 1, 'date': '2020-12-02', 'date_uts': 1606894200, 'home_team': 2, 'visitor_team': 1}]
        self.assertEqual(match_list, self.match_list_get(self.logger))

    def test_002_match_list_get(self):
        """ test match_list get with filter value exists """
        match_list = [{'match_id': 1, 'season': 1, 'date': '2020-12-01', 'date_uts': 1606807800, 'home_team': 1, 'visitor_team': 2}]
        self.assertEqual(match_list, self.match_list_get(self.logger, 'match_id', 1))

    def test_003_match_list_get(self):
        """ test match_list get with filter value exists and filtered output to list """
        match_list = ['2:1']
        self.assertEqual(match_list, self.match_list_get(self.logger, 'match_id', 1, ['result']))

    def test_004_match_list_get(self):
        """ test match_list get with filter value exists and filtered output to dict """
        match_list = [{'date': '2020-12-01', 'result': '2:1'}]
        self.assertEqual(match_list, self.match_list_get(self.logger, 'match_id', 1, ['result', 'date']))

    def test_005_match_list_get(self):
        """ test match_list get with filter value does not exists """
        self.assertFalse(self.match_list_get(self.logger, 'match_id', 25))

    def test_006_match_list_get(self):
        """ test match_list get with filter value exists and filtered output to dict  with not existing element"""
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.match_list_get(self.logger, 'match_id', 1, ['result', 'not_exist']))
        err_msg = "CRITICAL:test_hockey:error in match_list_get(): Cannot resolve keyword 'not_exist' into field. Choices are: date, date_uts, home_team, home_team_id, match_id, periodevent, result, season, season_id, shift, shot, visitor_team, visitor_team_id"
        self.assertIn(err_msg, lcm.output)

    def test_007_match_add(self):
        """ test  match_add"""
        self.assertEqual(3, self.match_add(self.logger, 'match_id', 3, {'season_id': 1, 'date': '2020-12-03', 'date_uts': 1580715000, 'home_team_id': 1, 'visitor_team_id': 2}))
        match_list = [{'match_id': 3, 'season': 1, 'date': '2020-12-03', 'date_uts': 1580715000, 'home_team': 1, 'visitor_team': 2}]
        self.assertEqual(match_list, self.match_list_get(self.logger, 'match_id', 3))

    def test_008_match_add(self):
        """ test  match_add without uts """
        self.assertEqual(4, self.match_add(self.logger, 'match_id', 4, {'season_id': 1, 'date': '2020-12-04', 'home_team_id': 1, 'visitor_team_id': 2}))
        match_list = [{'match_id': 4, 'season': 1, 'date': '2020-12-04', 'date_uts': 0, 'home_team': 1, 'visitor_team': 2}]
        self.assertEqual(match_list, self.match_list_get(self.logger, 'match_id', 4))

    def test_009_match_add(self):
        """ test  match_add"""
        err_msg = "CRITICAL:test_hockey:error in match_add(): Invalid field name(s) for model Match: 'date_ut'."
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.match_add(self.logger, 'match_id', 3, {'season_id': 1, 'date': '2020-12-03', 'date_ut': 1580715000, 'home_team_id': 1, 'visitor_team_id': 2}))
        self.assertIn(err_msg, lcm.output)

    def test_010_match_add(self):
        """ test  match_add for existing entry"""
        self.assertEqual(2, self.match_add(self.logger, 'match_id', 2, {'season_id': 1, 'date': '2020-12-02', 'date_uts': 1606894200, 'home_team_id': 2, 'visitor_team_id': 1}))
        match_list = [{'match_id': 2, 'season': 1, 'date': '2020-12-02', 'date_uts': 1606894200, 'home_team': 2, 'visitor_team': 1}]
        self.assertEqual(match_list, self.match_list_get(self.logger, 'match_id', 2))

    def test_011_match_add(self):
        """ test  match_add for existing entry / update """
        self.assertEqual(2, self.match_add(self.logger, 'match_id', 2, {'season_id': 1, 'date': '2020-12-02', 'date_uts': 1606894201, 'home_team_id': 2, 'visitor_team_id': 1}))
        match_list = [{'match_id': 2, 'season': 1, 'date': '2020-12-02', 'date_uts': 1606894201, 'home_team': 2, 'visitor_team': 1}]
        self.assertEqual(match_list, self.match_list_get(self.logger, 'match_id', 2))
