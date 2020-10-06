# -*- coding: utf-8 -*-
""" helper functions """
import logging
# pylint: disable=E0401, C0413
import sys
sys.path.insert(0, '.')
sys.path.insert(1, '..')

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
