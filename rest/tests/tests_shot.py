# -*- coding: utf-8 -*-
""" unittests for shots.py """
# pylint: disable= C0415, W0212
import sys
from django.test import TestCase
from rest.functions.helper import testdata_load

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class ShotTestCase(TestCase):
    """ shot test class """
    def setUp(self):
        """ setup test environment """
        from rest.functions.shot import _shoot_coordinates_convert, shot_list_get, shot_add
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')
        self._shoot_coordinates_convert = _shoot_coordinates_convert
        self.shot_add = shot_add
        self.shot_list_get = shot_list_get
        testdata_load()

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_shot_list_get(self):
        """ test shot_list get with no filter"""
        shot_list = [{'shot_id': 11, 'match_shot_resutl_id': 1, 'player_id': 1, 'zone': 'zone_11', 'timestamp': 11}, {'shot_id': 12, 'match_shot_resutl_id': 2, 'player_id': 1, 'zone': 'zone_12', 'timestamp': 12}, {'shot_id': 13, 'match_shot_resutl_id': 3, 'player_id': 1, 'zone': 'zone_13', 'timestamp': 13}, {'shot_id': 14, 'match_shot_resutl_id': 4, 'player_id': 1, 'zone': 'zone_14', 'timestamp': 14}, {'shot_id': 21, 'match_shot_resutl_id': 1, 'player_id': 2, 'zone': 'zone_21', 'timestamp': 21}, {'shot_id': 22, 'match_shot_resutl_id': 2, 'player_id': 2, 'zone': 'zone_22', 'timestamp': 22}, {'shot_id': 23, 'match_shot_resutl_id': 3, 'player_id': 2, 'zone': 'zone_23', 'timestamp': 23}, {'shot_id': 24, 'match_shot_resutl_id': 4, 'player_id': 2, 'zone': 'zone_24', 'timestamp': 24}]
        self.assertEqual(shot_list, self.shot_list_get(self.logger))

    def test_002_shot_list_get(self):
        """ test shot_list get with filter value exists """
        shot_list = [{'shot_id': 11, 'match_shot_resutl_id': 1, 'player_id': 1, 'zone': 'zone_11', 'timestamp': 11}]
        self.assertEqual(shot_list, self.shot_list_get(self.logger, 'shot_id', 11))

    def test_003_shot_list_get(self):
        """ test shot_list get with filter value exists and filtered output to list """
        shot_list = [11]
        self.assertEqual(shot_list, self.shot_list_get(self.logger, 'shot_id', 11, ['timestamp']))

    def test_004_shot_list_get(self):
        """ test shot_list get with filter value exists and filtered output to dict """
        shot_list = [{'timestamp': 11, 'match_shot_resutl_id': 1}]
        self.assertEqual(shot_list, self.shot_list_get(self.logger, 'shot_id', 11, ['timestamp', 'match_shot_resutl_id']))

    def test_005_shot_list_get(self):
        """ test shot_list get with filter value does not exists """
        self.assertFalse(self.shot_list_get(self.logger, 'shot_id', 10))

    def test_006_shot_list_get(self):
        """ test shot_list get with filter value exists and filtered output to dict  with not existing element"""
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.shot_list_get(self.logger, 'shot_id', 11, ['timestamp', 'not_exist']))
        err_msg = "CRITICAL:test_hockey:error in shot_list_get(): Cannot resolve keyword 'not_exist' into field. Choices are: coordinate_x, coordinate_y, match, match_id, match_shot_resutl_id, player, player_id, polygon, real_date, shot_id, team, team_id, timestamp, zone"
        self.assertIn(err_msg, lcm.output)

    def test_007_shot_add(self):
        """ test  shot_add"""
        add_dic = {'shot_id': 15, 'player_id': 1, 'team_id': 1, 'match_id': 1, 'match_shot_resutl_id': 1, 'timestamp': 15, 'coordinate_x': 15, 'coordinate_y': 15, 'real_date': 'real_date_15', 'polygon': 'polygon_15', 'zone': 'zone_15'}
        self.assertEqual(15, self.shot_add(self.logger, 'shot_id', 15, add_dic))
        shot_list = [{'shot_id': 15, 'player_id': 1, 'timestamp': 15}]
        self.assertEqual(shot_list, self.shot_list_get(self.logger, 'shot_id', 15, ['shot_id', 'player_id', 'timestamp']))

    def test_008_shot_add(self):
        """ test  shot_add"""
        add_dic = {'shot_id': 15, 'player_id': 1, 'team_id': 1, 'match_id': 1, 'match_shot_resutl_id': 1, 'times_tamp': 15, 'coordinate_x': 15, 'coordinate_y': 15, 'real_date': 'real_date_15', 'polygon': 'polygon_15', 'zone': 'zone_15'}
        err_msg = "CRITICAL:test_hockey:error in shot_add(): Invalid field name(s) for model Shot: 'times_tamp'."
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertFalse(self.shot_add(self.logger, 'shot_id', 15, add_dic))
        self.assertIn(err_msg, lcm.output)

    def test_009_shot_add(self):
        """ test  shot_add for existing entry"""
        add_dic = {'shot_id': 14, 'player_id': 1, 'team_id': 1, 'match_id': 1, 'match_shot_resutl_id': 1, 'times_tamp': 14, 'coordinate_x': 14, 'coordinate_y': 14, 'real_date': 'real_date_14', 'polygon': 'polygon_14', 'zone': 'zone_14'}
        self.assertEqual(14, self.shot_add(self.logger, 'shot_id', 14, add_dic))
        shot_list = [{'shot_id': 14, 'match_shot_resutl_id': 1, 'player_id': 1, 'zone': 'zone_14', 'timestamp': 14}]
        self.assertEqual(shot_list, self.shot_list_get(self.logger, 'shot_id', 14))

    def test_010_shot_add(self):
        """ test  shot_add update existing entry"""
        add_dic = {'shot_id': 14, 'player_id': 1, 'team_id': 1, 'match_id': 1, 'match_shot_resutl_id': 2, 'times_tamp': 14, 'coordinate_x': 14, 'coordinate_y': 14, 'real_date': 'real_date_14', 'polygon': 'polygon_14', 'zone': 'zone_14'}
        self.assertEqual(14, self.shot_add(self.logger, 'shot_id', 14, add_dic))
        shot_list = [{'shot_id': 14, 'match_shot_resutl_id': 2, 'player_id': 1, 'zone': 'zone_14', 'timestamp': 14}]
        self.assertEqual(shot_list, self.shot_list_get(self.logger, 'shot_id', 14))

    def test_011__shoot_coordinates_convert(self):
        """ test _shoot_coordinates_convert - all ok """
        my_x = 1
        my_y = 1
        self.assertEqual((0.3, 0.15), self._shoot_coordinates_convert(self.logger, my_x, my_y))

    def test_011__shoot_coordinates_convert(self):
        """ test _shoot_coordinates_convert - insert string which can be converted to int"""
        my_x = "10"
        my_y = "10"
        self.assertEqual((3.05, 1.52), self._shoot_coordinates_convert(self.logger, my_x, my_y))

    def test_011__shoot_coordinates_convert(self):
        """ test _shoot_coordinates_convert - insert string which cannot be converted to int"""
        my_x = "foo"
        my_y = "bar"
        err_msg = "CRITICAL:test_hockey:error in _shoot_coordinates_convert(): invalid literal for int() with base 10: 'foo'"
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertEqual((0, 0), self._shoot_coordinates_convert(self.logger, my_x, my_y))
        self.assertIn(err_msg, lcm.output)

    def test_012__shoot_coordinates_convert(self):
        """ test _shoot_coordinates_convert - insert string y which cannot be converted to int"""
        my_x = 1
        my_y = "bar"
        err_msg = "CRITICAL:test_hockey:error in _shoot_coordinates_convert(): invalid literal for int() with base 10: 'bar'"
        with self.assertLogs('test_hockey', level='INFO') as lcm:
            self.assertEqual((0, 0), self._shoot_coordinates_convert(self.logger, my_x, my_y))
        self.assertIn(err_msg, lcm.output)
