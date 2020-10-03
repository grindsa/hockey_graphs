# -*- coding: utf-8 -*-
""" unittests for teams.py """
# pylint: disable= C0415, W0212
import sys
from django.test import TestCase
from rest.models import Team

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class TeamTestCase(TestCase):
    """ team test class """
    def setUp(self):
        """ setup test environment """
        from rest.functions.team import team_list_get, team_add
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')
        self.team_list_get = team_list_get
        self.team_add = team_add
        Team.objects.create(team_id="1", team_name="Team-1", shortcut="T1")
        Team.objects.create(team_id="2", team_name="Team-2", shortcut="T2")

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_team_list_get(self):
        """ test team_list get with no filter"""
        team_list = [{'team_id': 1, 'team_name': 'Team-1', 'shortcut': 'T1'}, {'team_id': 2, 'team_name': 'Team-2', 'shortcut': 'T2'}]
        self.assertEqual(team_list, self.team_list_get(self.logger))

    def test_002_team_list_get(self):
        """ test team_list get with filter value exists """
        team_list = [{'shortcut': 'T1', 'team_id': 1, 'team_name': 'Team-1'}]
        self.assertEqual(team_list, self.team_list_get(self.logger, 'team_id', 1))

    def test_003_team_list_get(self):
        """ test team_list get with filter value exists and filtered output to list """
        team_list = ['T1']
        self.assertEqual(team_list, self.team_list_get(self.logger, 'team_id', 1, ['shortcut']))

    def test_004_team_list_get(self):
        """ test team_list get with filter value exists and filtered output to dict """
        team_list = [{'shortcut': 'T1', 'team_name': 'Team-1'}]
        self.assertEqual(team_list, self.team_list_get(self.logger, 'team_id', 1, ['team_name', 'shortcut']))

    def test_005_team_list_get(self):
        """ test team_list get with filter value does not exists """
        self.assertFalse(self.team_list_get(self.logger, 'team_name', 'Team'))

    def test_006_team_list_get(self):
        """ test team_list get with filter value exists and filtered output to dict  with not existing element"""
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.team_list_get(self.logger, 'team_id', 1, ['team_name', 'not_exist']))
        err_msg = "CRITICAL:test_hockey:error in team_list_get(): Cannot resolve keyword 'not_exist' into field. Choices are: home_team, shortcut, shot, team_id, team_name, visitor_team"
        self.assertIn(err_msg, lcm.output)

    def test_007_team_add(self):
        """ test  team_add"""
        self.assertEqual(3, self.team_add(self.logger, 'team_id', 3, {'team_name': 'Team-3', 'shortcut': 'T3'}))
        team_list = [{'shortcut': 'T3', 'team_id': 3, 'team_name': 'Team-3'}]
        self.assertEqual(team_list, self.team_list_get(self.logger, 'team_id', 3))

    def test_008_team_add(self):
        """ test  team_add"""
        err_msg = "CRITICAL:test_hockey:error in team_add(): Invalid field name(s) for model Team: 'short_cut'."
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.team_add(self.logger, 'team_id', 3, {'team_name': 'Team-3', 'short_cut': 'T3'}))
        self.assertIn(err_msg, lcm.output)

    def test_009_team_add(self):
        """ test  team_add for existing entry"""
        self.assertEqual(2, self.team_add(self.logger, 'team_id', 2, {'team_name': 'Team-2', 'shortcut': 'T2'}))
        team_list = [{'shortcut': 'T2', 'team_id': 2, 'team_name': 'Team-2'}]
        self.assertEqual(team_list, self.team_list_get(self.logger, 'team_id', 2))

    def test_010_team_add(self):
        """ test  team_add for existing entry / update """
        self.assertEqual(2, self.team_add(self.logger, 'team_id', 2, {'team_name': 'Team2', 'shortcut': 'T2'}))
        team_list = [{'shortcut': 'T2', 'team_id': 2, 'team_name': 'Team2'}]
        self.assertEqual(team_list, self.team_list_get(self.logger, 'team_id', 2))
