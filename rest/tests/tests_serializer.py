# -*- coding: utf-8 -*-
""" unittests for players.py """
# pylint: disable= C0415, W0212
import sys
from unittest.mock import patch, Mock
from django.test import TestCase, RequestFactory
from rest.functions.helper import testdata_load
from rest.serializers import MatchSerializer, PeriodeventSerializer, PlayerSerializer, SeasonSerializer, ShiftSerializer, ShotSerializer, TeamSerializer

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class PlayerTestCase(TestCase):
    """ player test class """
    def setUp(self):
        """ setup test environment """
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_playerserializer(self):
        """ test PlayerSerializer """
        val_dic = {'player_id': 10, 'first_name': 'fn', 'last_name':'ln', 'jersey': 20, 'foo': 'bar'}
        result_dic = {'player_id': 10, 'first_name': 'fn', 'last_name':'ln', 'jersey': 20}
        serializer = PlayerSerializer(data=val_dic)
        if serializer.is_valid():
            self.assertEqual(result_dic, serializer.data)
        else:
            print(serializer.errors)

    def test_002_seasonserializer(self):
        """ test SeasonSerializer """
        val_dic = {'id': 10, 'name': 'name', 'foo': 'bar'}
        result_dic = {'name': 'name'}
        serializer = SeasonSerializer(data=val_dic)
        if serializer.is_valid():
            self.assertEqual(result_dic, serializer.data)
        else:
            print(serializer.errors)

    def test_003_teamserializer(self):
        """ test TeamSerializer """
        val_dic = {'team_id': 10, 'team_name': 'team_name', 'shortcut': 'short', 'foo': 'bar'}
        result_dic = {'team_id': 10, 'team_name': 'team_name', 'shortcut': 'short'}
        serializer = TeamSerializer(data=val_dic)
        if serializer.is_valid():
            self.assertEqual(result_dic, serializer.data)
        else:
            print(serializer.errors)

    def test_004_periodeventserializer(self):
        """ test PeriodeventSerializer """
        val_dic = {'match_id': 10, 'period_event': 'period_event', 'foo': 'bar'}
        result_dic = {'period_event': 'period_event'}
        serializer = PeriodeventSerializer(data=val_dic)
        if serializer.is_valid():
            self.assertEqual(result_dic, serializer.data)
        else:
            print(serializer.errors)

    def test_005_shiftserializer(self):
        """ test ShiftSerializer """
        val_dic = {'match_id': 10, 'shift': 'shift', 'foo': 'bar'}
        result_dic = {'shift': 'shift'}
        serializer = ShiftSerializer(data=val_dic)
        if serializer.is_valid():
            self.assertEqual(result_dic, serializer.data)
        else:
            print(serializer.errors)

    def test_006_shotserializer(self):
        """ test ShotSerializer """
        player_dic = {'player_id': 10, 'first_name': 'first_name', 'last_name': 'last_name', 'jersey': 10}
        val_dic = {'shot_id': 10, 'match_id': 10, 'match': 'match', 'player_id': 10, 'player': player_dic, 'timestamp': 10, 'coordinate_x': 10, 'coordinate_y': 10, 'real_date': 'real_date', 'polygon': 'polygon', 'zone': 'zone', 'match_shot_resutl_id': 1, 'foo': 'bar'}
        result_dic = {'shot_id': 10, 'player': player_dic, 'match_shot_resutl_id': 1, 'timestamp': 10, 'coordinate_x': 10, 'coordinate_y': 10, 'real_date': 'real_date', 'polygon': 'polygon', 'zone': 'zone'}
        serializer = ShotSerializer(data=val_dic)
        if serializer.is_valid():
            self.assertEqual(result_dic, serializer.data)
        else:
            print(serializer.errors)

    def test_007_matchserializer(self):
        """ test MatchSerializer """
        val_dic = {'match_id': 10, 'shifts': None, 'shots': None, 'events': None, 'foo': 'bar'}
        result_dic = {'match_id': 10, 'shifts': None, 'shots': None, 'events': None}
        serializer = MatchSerializer(data=val_dic)
        if serializer.is_valid():
            self.assertEqual(result_dic, serializer.data)
        else:
            print(serializer.errors)

    #@patch('rest.serializers.get_url')
    #def test_008_matchserializer(self, mock_url):
    #    """ test MatchSerializer """
    #    mock_url.return_value = 'foo'
    #    val_dic = {'match_id': 10, 'shifts': None, 'shots': None, 'events': None, 'foo': 'bar'}
    #    result_dic = {'match_id': 10, 'shifts': None, 'shots': None, 'events': None}
    #    request = RequestFactory().get('foo')
    #    serializer = MatchSerializer(context={'request': request}, data=val_dic)
    #    if serializer.is_valid():
    #        self.assertEqual(result_dic, serializer.data)
    #    else:
    #        print(serializer.errors)
