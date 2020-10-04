# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from shapely.geometry import Point
from rest.models import Shot
import functions.rink_dimensions as rd

def _shoot_coordinates_convert(logger, coordinate_x, coordinate_y):
    """ convert  arbitrary coordinates to actual coordinates in meters sourse: leaffan.net """
    try:
        x2m = 0.3048
        y2m = 0.1524
        meter_x = x2m * int(coordinate_x)
        meter_y = y2m * int(coordinate_y)
    except BaseException as err_:
        logger.critical('error in _shoot_coordinates_convert(): {0}'.format(err_))
        meter_x = 0
        meter_y = 0

    return(round(meter_x, 2), round(meter_y, 2))

def shot_list_get(logger, fkey=None, fvalue=None, vlist=('shot_id', 'match_shot_resutl_id', 'player_id', 'zone', 'timestamp')):
    """ query shot(s) from database based with optional filtering """
    try:
        if fkey:
            if len(vlist) == 1:
                shot_list = Shot.objects.filter(**{fkey: fvalue}).order_by('shot_id').values_list(vlist[0], flat=True)
            else:
                shot_list = Shot.objects.filter(**{fkey: fvalue}).order_by('shot_id').values(*vlist)
        else:
            if len(vlist) == 1:
                shot_list = Shot.objects.all().order_by('shot_id').values_list(vlist[0], flat=True)
            else:
                shot_list = Shot.objects.all().order_by('shot_id').values(*vlist)
    except BaseException as err_:
        logger.critical('error in shot_list_get(): {0}'.format(err_))
        shot_list = []
    return list(shot_list)

def shot_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('shot_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add authorization
        obj, _created = Shot.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.shot_id
    except BaseException as err_:
        logger.critical('error in shot_add(): {0}'.format(err_))
        result = None
    logger.debug('shot_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def zone_name_get(logger, coordinate_x, coordinate_y):
    """ get coordinates """
    (meter_x, meter_y) = _shoot_coordinates_convert(logger, coordinate_x, coordinate_y)
    # constructing shot location
    shot_pnt = Point(meter_x, meter_y)
    shot_zone = None
    # determining shot zone
    for poly_name, poly in rd.polygons:
        if poly.intersects(shot_pnt):
            shot_zone = poly_name[5:]
            break
    return shot_zone.lower()
