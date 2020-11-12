# -*- coding: utf-8 -*-
""" unittests for players.py """
# pylint: disable = C0415
import unittest
import datetime
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, '.')
sys.path.insert(1, '..')

class HelperTestCase(unittest.TestCase):
    """ player test class """
    def setUp(self):
        """ setup test environment """
        from rest.functions.helper import min2sec, uts_to_date_utc, date_to_uts_utc, pctg_get, url_build
        import logging
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger('test_hockey')
        self.min2sec = min2sec
        self.date_to_uts_utc = date_to_uts_utc
        self.uts_to_date_utc = uts_to_date_utc
        self.pctg_get = pctg_get
        self.url_build = url_build

    def tearDown(self):
        """ teardown test environment """
        # Clean up run after every test method.

    def test_001_helper_min2sec(self):
        """ test min2sec working """
        self.assertEqual('01:00', self.min2sec(60))

    def test_002_helper_min2sec(self):
        """ test min2sec working """
        self.assertEqual('01:15', self.min2sec(75))

    def test_003_helper_min2sec(self):
        """ test min2sec sending shit """
        self.assertFalse(self.min2sec('test'))

    def test_004_helper_min2sec(self):
        """ test min2sec sending empty """
        self.assertFalse(self.min2sec(None))

    def test_005_helper_uts_to_date_utc(self):
        """ test uts_to_date_utc for a given format """
        self.assertEqual('2018-12-01', self.uts_to_date_utc(1543640400, '%Y-%m-%d'))

    def test_006_helper_uts_to_date_utc(self):
        """ test uts_to_date_utc without format """
        self.assertEqual('2018-12-01T05:00:00Z', self.uts_to_date_utc(1543640400))

    def test_007_helper_date_to_uts_utc(self):
        """ test date_to_uts_utc for a given format """
        self.assertEqual(1543622400, self.date_to_uts_utc('2018-12-01', '%Y-%m-%d'))

    def test_008_helper_date_to_uts_utc(self):
        """ test date_to_uts_utc without format """
        self.assertEqual(1543640400, self.date_to_uts_utc('2018-12-01T05:00:00'))

    def test_009_helper_date_to_uts_utc(self):
        """ test date_to_uts_utc with a datestring """
        timestamp = datetime.datetime(2018, 12, 1, 5, 0, 1)
        self.assertEqual(1543640401, self.date_to_uts_utc(timestamp))

    def test_010_helper_pctg_get(self):
        """ test pctg_get - all ok  """
        self.assertEqual('60.0%', self.pctg_get(60, 100))

    def test_011_helper_pctg_get(self):
        """ test pctg_get - all full  """
        self.assertEqual('100.0%', self.pctg_get(100, 100))

    def test_012_helper_pctg_get(self):
        """ test pctg_get - all min  """
        self.assertEqual('0.0%', self.pctg_get(0, 100))

    def test_013_helper_pctg_get(self):
        """ test pctg_get - divisor zero  """
        self.assertEqual('0%', self.pctg_get(6, 0))

    def test_014_helper_pctg_get(self):
        """ test pctg_get - test in part  """
        self.assertEqual('0%', self.pctg_get('test', 6))

    def test_015_helper_pctg_get(self):
        """ test pctg_get - test in base  """
        self.assertEqual('0%', self.pctg_get(6, 'base'))

    def test_016_helper_url_build(self):
        """ url_build https """
        data_dic = {'HTTP_HOST': 'http_host', 'SERVER_PORT': 443, 'PATH_INFO': 'path_info'}
        self.assertEqual('https://http_host', self.url_build(data_dic, False))

    def test_017_helper_url_build(self):
        """ url_build http """
        data_dic = {'HTTP_HOST': 'http_host', 'SERVER_PORT': 80, 'PATH_INFO': 'path_info'}
        self.assertEqual('http://http_host', self.url_build(data_dic, False))

    def test_018_helper_url_build(self):
        """ url_build http wsgi.scheme """
        data_dic = {'HTTP_HOST': 'http_host', 'SERVER_PORT': 80, 'PATH_INFO': 'path_info', 'wsgi.url_scheme': 'wsgi.url_scheme'}
        self.assertEqual('wsgi.url_scheme://http_host', self.url_build(data_dic, False))

    def test_019_helper_url_build(self):
        """ url_build https include_path true bot no pathinfo"""
        data_dic = {'HTTP_HOST': 'http_host', 'SERVER_PORT': 443}
        self.assertEqual('https://http_host', self.url_build(data_dic, True))

    def test_020_helper_url_build(self):
        """ url_build https and path info"""
        data_dic = {'HTTP_HOST': 'http_host', 'SERVER_PORT': 443, 'PATH_INFO': 'path_info'}
        self.assertEqual('https://http_hostpath_info', self.url_build(data_dic, True))

    def test_21_helper_url_build(self):
        """ url_build wsgi.url and pathinfo """
        data_dic = {'HTTP_HOST': 'http_host', 'SERVER_PORT': 80, 'PATH_INFO': 'path_info', 'wsgi.url_scheme': 'wsgi.url_scheme'}
        self.assertEqual('wsgi.url_scheme://http_hostpath_info', self.url_build(data_dic, True))

    def test_022_helper_url_build(self):
        """ url_build http and pathinfo"""
        data_dic = {'HTTP_HOST': 'http_host', 'SERVER_PORT': 80, 'PATH_INFO': 'path_info'}
        self.assertEqual('http://http_hostpath_info', self.url_build(data_dic, True))

    def test_023_helper_url_build(self):
        """ url_build without hostinfo """
        data_dic = {'SERVER_PORT': 80, 'PATH_INFO': 'path_info'}
        self.assertEqual('http://localhost', self.url_build(data_dic, False))

    def test_024_helper_url_build(self):
        """ url_build without SERVER_PORT """
        data_dic = {'HTTP_HOST': 'http_host'}
        self.assertEqual('http://http_host', self.url_build(data_dic, True))

if __name__ == '__main__':
    unittest.main()
