# -*- coding: utf-8 -*-
""" helper functions """
import logging
# pylint: disable=E0401, C0413
import sys
import calendar
import json
import configparser
from datetime import datetime
import math
import numpy as np
from dateutil.parser import parse
import pytz

sys.path.insert(0, '.')
sys.path.insert(1, '..')

def config_load(logger=None, mfilter=None, cfg_file='hockeygraphs.cfg'):
    """ small configparser wrappter to load a config file """
    if logger:
        logger.debug('config_load({1}:{0})'.format(mfilter, cfg_file))
    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read(cfg_file)
    return config

def json_load(file_name):
    """ load json structure from file """
    with open(file_name, encoding='utf8') as json_file:
        data = json.load(json_file)
    return data

def json_store(file_name_, data_):
    """ store structure as json to file """
    with open(file_name_, 'w', encoding='utf-8') as out_file:
        json.dump(data_, out_file, ensure_ascii=False, indent=4)

def url_build(environ, include_path=False):
    """ get url """
    if 'HTTP_HOST' in environ:
        server_name = environ['HTTP_HOST']
    else:
        server_name = 'localhost'

    if 'SERVER_PORT' in environ:
        port = environ['SERVER_PORT']
    else:
        port = 80

    if 'HTTP_X_FORWARDED_PROTO' in environ:
        proto = environ['HTTP_X_FORWARDED_PROTO']
    elif 'wsgi.url_scheme' in environ:
        proto = environ['wsgi.url_scheme']
    elif port == 443:
        proto = 'https'
    else:
        proto = 'http'

    if include_path and 'PATH_INFO' in environ:
        result = '{0}://{1}{2}'.format(proto, server_name, environ['PATH_INFO'])
    else:
        result = '{0}://{1}'.format(proto, server_name)
    return result

def testdata_load(_debug=False):
    """ load testdata for unittests """
    # pylint: disable=C0415
    from rest.models import Match, Player, Periodevent, Shift, Season, Shot, Team
    Season.objects.create(name="Season-1")
    Season.objects.create(name="Season-2")
    Team.objects.create(team_id=1, team_name="Team-1", shortcut="T1")
    Team.objects.create(team_id=2, team_name="Team-2", shortcut="T2")
    Match.objects.create(match_id=1, season_id=1, date="2020-12-01", date_uts=1606807800, home_team_id=1, visitor_team_id=2, result='2:1')
    Match.objects.create(match_id=2, season_id=1, date="2020-12-02", date_uts=1606894200, home_team_id=2, visitor_team_id=1, result='1:2')
    Player.objects.create(player_id=1, first_name="first_name_1", last_name="last_name_1", jersey=1)
    Player.objects.create(player_id=2, first_name="first_name_2", last_name="last_name_2", jersey=2)
    Periodevent.objects.create(match_id=1, period_event={'foo': 'bar1'})
    Periodevent.objects.create(match_id=2, period_event={'foo': 'bar2'})
    Shift.objects.create(match_id=1, shift={'foo': 'bar1'})
    Shift.objects.create(match_id=2, shift={'foo': 'bar2'})
    Shot.objects.create(shot_id=11, player_id=1, team_id=1, match_id=1, match_shot_resutl_id=1, timestamp=11, coordinate_x=11, coordinate_y=11, real_date='real_date_11', polygon='polygon_11', zone='zone_11')
    Shot.objects.create(shot_id=12, player_id=1, team_id=1, match_id=1, match_shot_resutl_id=2, timestamp=12, coordinate_x=12, coordinate_y=12, real_date='real_date_12', polygon='polygon_12', zone='zone_12')
    Shot.objects.create(shot_id=13, player_id=1, team_id=1, match_id=1, match_shot_resutl_id=3, timestamp=13, coordinate_x=13, coordinate_y=13, real_date='real_date_13', polygon='polygon_13', zone='zone_13')
    Shot.objects.create(shot_id=14, player_id=1, team_id=1, match_id=1, match_shot_resutl_id=4, timestamp=14, coordinate_x=14, coordinate_y=14, real_date='real_date_14', polygon='polygon_14', zone='zone_14')
    Shot.objects.create(shot_id=21, player_id=2, team_id=2, match_id=1, match_shot_resutl_id=1, timestamp=21, coordinate_x=21, coordinate_y=21, real_date='real_date_21', polygon='polygon_21', zone='zone_21')
    Shot.objects.create(shot_id=22, player_id=2, team_id=2, match_id=1, match_shot_resutl_id=2, timestamp=22, coordinate_x=22, coordinate_y=22, real_date='real_date_22', polygon='polygon_22', zone='zone_22')
    Shot.objects.create(shot_id=23, player_id=2, team_id=2, match_id=1, match_shot_resutl_id=3, timestamp=23, coordinate_x=23, coordinate_y=23, real_date='real_date_23', polygon='polygon_23', zone='zone_23')
    Shot.objects.create(shot_id=24, player_id=2, team_id=2, match_id=1, match_shot_resutl_id=4, timestamp=24, coordinate_x=24, coordinate_y=24, real_date='real_date_24', polygon='polygon_24', zone='zone_24')

def mobile_check(logger, request):
    """ mobile check """
    logger.debug('mobile_check()')
    if hasattr(request, 'GET') and 'mobile' in request.GET:
        if request.GET['mobile'].lower() == 'true':
            mobile = True
        else:
            mobile = False
    else:
        mobile = False
    logger.debug('mobile_check() ended with: {0}'.format(mobile))
    return mobile

def logger_setup(debug):
    """ setup logger """
    if debug:
        log_mode = logging.DEBUG
    else:
        log_mode = logging.INFO

    # log_formet = '%(message)s'
    log_format = '%(asctime)s - hockey_graphs - %(levelname)s - %(message)s'
    logging.basicConfig(
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        level=log_mode)
    logger = logging.getLogger('hockey_graph')
    return logger

def uts_now():
    """ return unixtimestamp in utc """
    return calendar.timegm(datetime.utcnow().utctimetuple())

def uts_to_date_utc(uts, tformat='%Y-%m-%dT%H:%M:%SZ'):
    """ convert unix timestamp to date format """
    return datetime.fromtimestamp(int(uts), tz=pytz.utc).strftime(tformat)

def date_to_uts_utc(date_human, _tformat='%Y-%m-%dT%H:%M:%S'):
    """ convert date to unix timestamp """
    if isinstance(date_human, datetime):
        # we already got an datetime object as input
        result = calendar.timegm(date_human.timetuple())
    else:
        result = int(calendar.timegm(parse(date_human).timetuple()))
    return result

def date_to_datestr(date, tformat='%Y-%m-%dT%H:%M:%SZ'):
    """ convert dateobj to datestring """
    try:
        result = date.strftime(tformat)
    except BaseException:
        result = None
    return result

def datestr_to_date(datestr, tformat='%Y-%m-%dT%H:%M:%S'):
    """ convert datestr to dateobj """
    try:
        result = datetime.strptime(datestr, tformat)
    except BaseException:
        result = None
    return result

def list2dic(_logger, input_list, pkey=None):
    """ convert a list to a dicitionary """
    # logger.debug('list2dic({0})'.format(pkey))
    output_dict = {}
    if pkey:
        for ele in input_list:
            output_dict[ele[pkey]] = ele
    return output_dict

def maxval_get(input_list, sorter='timestamp', divisor=60, add=1):
    """ look for a matchvalue form a sorted list """
    try:
        x_max = math.ceil(sorted(input_list, key=lambda x: x[sorter])[-1][sorter]/divisor) + add
    except BaseException:
        x_max = divisor + 1
    return x_max

def pctg_float_get(part, base, decimal=2):
    """ calculate pcts and return float """
    try:
        if base != 0:
            pctg_value = round(part*100/base, decimal)
        else:
            pctg_value = 0
    except BaseException:
        pctg_value = 0

    return pctg_value

def pctg_get(part, base):
    """ calculate percentage value and return ans string """
    # catch division by zero exceptions
    try:
        if base != 0:
            pctg_value = '{0}%'.format(round(part*100/base, 0))
        else:
            pctg_value = '0%'
    except BaseException:
        pctg_value = '0%'

    return pctg_value

def min2sec(sec_value):
    """ convert seconds to mm:ss """
    try:
        (min_, sec) = divmod(sec_value, 60)
        min_value = '{:02d}:{:02d}'.format(min_, sec)
    except BaseException:
        min_value = None

    return min_value

def list_sumup(logger, input_list, filter_values, reverse=False):
    """ sum up list of dictionaries based on input """
    logger.debug('list_sumup()')

    match_list = []
    _tmp_sum = {}
    for ele in filter_values:
        _tmp_sum[ele] = 0

    if reverse:
        input_list = list(reversed(input_list))

    for match in input_list:
        _tmp_dic = {}
        for ele in filter_values:
            _tmp_dic[ele] = match[ele]
            _tmp_sum[ele] += match[ele]
            _tmp_dic['sum_{0}'.format(ele)] = _tmp_sum[ele]

        match_list.append(_tmp_dic)

    if reverse:
        match_list = list(reversed(match_list))

    return match_list


def shot_leaffan_sync(shot, ltime, ldate):
    """ keep shot sync with leaffan.net """
    (mday, _time) = shot['real_date'].split(' ', 2)
    if ltime <= shot['timestamp']:
        # usually seonds in match should always increase.. if not - this is a mistake and hould be skippt
        ltime = shot['timestamp']
        ldate = mday
        process_shot = True
    elif abs(ltime - shot['timestamp']) < 300:
        # consider in game corrections
        process_shot = True
        # ldate = mday
    elif ldate == mday:
        # consider corrections outsid
        process_shot = True

    else:
        process_shot = False

    return (process_shot, ltime, ldate)

def deviation_avg_get(logger, input_list, value_list=None):
    """ add standard deviation """
    logger.debug('_deviation_add()')
    _tmp_lake = {}
    for value in value_list:
        _tmp_lake[value] = []

    # compile lists
    for ele in input_list:
        for value in value_list:
            if value in ele:
                _tmp_lake[value].append(ele[value])

    # calculate deviation
    deviation_dic = {}
    for value in _tmp_lake:
        if _tmp_lake[value]:
            deviation_dic[value] = {'std_deviation': round(np.std(_tmp_lake[value]), 2), 'average': round(np.mean(_tmp_lake[value]), 2), 'min': np.amin(_tmp_lake[value]), 'max': np.amax(_tmp_lake[value])}

    return deviation_dic

def minmax_get(minval, maxval, average):
    """ define min/max based on avarage """

    minabs = round(abs(maxval - average), 0)
    maxabs = round(abs(minval - average), 0)

    if maxabs > minabs:
        newmin = average - maxabs
        newmax = average + maxabs
    else:
        newmin = average - minabs
        newmax = average + minabs

    return (newmin, newmax)

def language_get(logger, request):
    """ lang check """
    logger.debug('language_get()')

    if hasattr(request, 'GET') and 'language' in request.GET:
        try:
            language = request.GET['language'].lower()
        except BaseException:
            language = 'en'
    else:
        language = 'en'

    logger.debug('language_get() ended with: {0}'.format(language))
    return language

def period_get(value, vtype='min'):
    """ get period from value """
    if vtype == 'min':
        if value <= 20:
            period = 1
        elif value <= 40:
            period = 2
        elif value <= 60:
            period = 3
        else:
            period = 4
    return period
