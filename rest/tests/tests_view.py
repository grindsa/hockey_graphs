# -*- coding: utf-8 -*-
""" unittests for teams.py """
# pylint: disable= C0415, W0212
import sys
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest.functions.helper import testdata_load

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class ApiTestCase(TestCase):
    """ team test class """
    def setUp(self):
        """ setup test environment """
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')
        self.client = APIClient()
        testdata_load()

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_playerview(self):
        """ test playerview """
        url = reverse('player-list')
        response = self.client.get(url)
        result = b'{"count":2,"next":null,"previous":null,"results":[{"player_id":1,"first_name":"first_name_1","last_name":"last_name_1","jersey":1},{"player_id":2,"first_name":"first_name_2","last_name":"last_name_2","jersey":2}]}'
        self.assertEqual(200, response.status_code)
        self.assertEqual(result, response.content)

    def test_002_teamview(self):
        """ test teamview """
        url = reverse('team-list')
        response = self.client.get(url)
        result = b'{"count":2,"next":null,"previous":null,"results":[{"team_id":1,"team_name":"Team-1","shortcut":"T1"},{"team_id":2,"team_name":"Team-2","shortcut":"T2"}]}'
        self.assertEqual(200, response.status_code)
        self.assertEqual(result, response.content)

    def test_003_matchview(self):
        """ test matchview """
        url = reverse('match-list')
        response = self.client.get(url)
        result = b'{"count":2,"next":null,"previous":null,"results":[{"match_id":1,"season":"Season-1","date":"2020-12-01","date_uts":1606807800,"home_team":"Team-1","visitor_team":"Team-2"},{"match_id":2,"season":"Season-1","date":"2020-12-02","date_uts":1606894200,"home_team":"Team-2","visitor_team":"Team-1"}]}'
        self.assertEqual(200, response.status_code)
        self.assertEqual(result, response.content)

    def test_004_periodeventview(self):
        """ test periodeventview """
        url = reverse('Periodevent-list')
        response = self.client.get(url)
        result = b'[]'
        self.assertEqual(200, response.status_code)
        self.assertEqual(result, response.content)

    def test_005_periodeventview(self):
        """ test periodeventview with valid filter """
        # url = reverse('Periodevent-list')
        url = '/api/v1/events/'
        data = {'match_id': 1}
        response = self.client.get(url, data)
        result = b'[{"foo":"bar1"}]'
        self.assertEqual(200, response.status_code)
        self.assertEqual(result, response.content)

    def test_006_periodeventview(self):
        """ test periodeventview with invalid filter """
        url = reverse('Periodevent-list')
        # url = '/api/v1/events/'
        data = {'match_id': 3}
        response = self.client.get(url, data)
        result = b'[]'
        self.assertEqual(200, response.status_code)
        self.assertEqual(result, response.content)
