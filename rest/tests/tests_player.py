# -*- coding: utf-8 -*-
""" unittests for players.py """
# pylint: disable= C0415, W0212
import sys
from django.test import TestCase
from rest.functions.helper import testdata_load

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class PlayerTestCase(TestCase):
    """ player test class """
    def setUp(self):
        """ setup test environment """
        from rest.functions.player import player_list_get, player_add
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')
        self.player_list_get = player_list_get
        self.player_add = player_add
        testdata_load()

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_player_list_get(self):
        """ test player_list get with no filter"""
        player_list = [{'player_id': 1, 'first_name': 'first_name_1', 'last_name': 'last_name_1', 'jersey': 1}, {'player_id': 2, 'first_name': 'first_name_2', 'last_name': 'last_name_2', 'jersey': 2}]
        self.assertEqual(player_list, self.player_list_get(self.logger))

    def test_002_player_list_get(self):
        """ test player_list get with filter value exists """
        player_list = [{'player_id': 1, 'first_name': 'first_name_1', 'last_name': 'last_name_1', 'jersey': 1}]
        self.assertEqual(player_list, self.player_list_get(self.logger, 'player_id', 1))

    def test_003_player_list_get(self):
        """ test player_list get with filter value exists and filtered output to list """
        player_list = [1]
        self.assertEqual(player_list, self.player_list_get(self.logger, 'player_id', 1, ['jersey']))

    def test_004_player_list_get(self):
        """ test player_list get with filter value exists and filtered output to dict """
        player_list = [{'last_name': 'last_name_1', 'jersey': 1}]
        self.assertEqual(player_list, self.player_list_get(self.logger, 'player_id', 1, ['last_name', 'jersey']))

    def test_005_player_list_get(self):
        """ test player_list get with filter value does not exists """
        self.assertFalse(self.player_list_get(self.logger, 'last_name', 'last_name'))

    def test_006_player_list_get(self):
        """ test player_list get with filter value exists and filtered output to dict  with not existing element"""
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.player_list_get(self.logger, 'player_id', 1, ['last_name', 'not_exist']))
        err_msg = "CRITICAL:test_hockey:error in player_list_get(): Cannot resolve keyword 'not_exist' into field. Choices are: first_name, jersey, last_name, player_id, shot"
        self.assertIn(err_msg, lcm.output)

    def test_007_player_add(self):
        """ test  player_add"""
        self.assertEqual(3, self.player_add(self.logger, 'player_id', 3, {'first_name': 'first_name_3', 'last_name': 'last_name_3', 'jersey': 3}))
        player_list = [{'player_id': 3, 'first_name': 'first_name_3', 'last_name': 'last_name_3', 'jersey': 3}]
        self.assertEqual(player_list, self.player_list_get(self.logger, 'player_id', 3))

    def test_008_player_add(self):
        """ test  player_add"""
        err_msg = "CRITICAL:test_hockey:error in player_add(): Invalid field name(s) for model Player: 'notexist'."
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.player_add(self.logger, 'player_id', 3, {'first_name': 'first_name_3', 'notexist': 'notexist'}))
        self.assertIn(err_msg, lcm.output)

    def test_009_player_add(self):
        """ test  player_add for existing entry"""
        self.assertEqual(2, self.player_add(self.logger, 'player_id', 2, {'first_name': 'first_name_2', 'last_name': 'last_name_2', 'jersey': 2}))
        player_list = [{'player_id': 2, 'first_name': 'first_name_2', 'last_name': 'last_name_2', 'jersey': 2}]
        self.assertEqual(player_list, self.player_list_get(self.logger, 'player_id', 2))

    def test_010_player_add(self):
        """ test  player_add for existing entry / update """
        self.assertEqual(2, self.player_add(self.logger, 'player_id', 2, {'first_name': 'first_name_2', 'last_name': 'last_name2', 'jersey': 2}))
        player_list = [{'player_id': 2, 'first_name': 'first_name_2', 'last_name': 'last_name2', 'jersey': 2}]
        self.assertEqual(player_list, self.player_list_get(self.logger, 'player_id', 2))
