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

def _shoot_coordinates_convert(coordinate_x, coordinate_y):
    """ convert  arbitrary coordinates to actual coordinates in meters sourse: leaffan.net """
    x2m = 0.3048
    y2m = 0.1524
    meter_x = x2m * coordinate_x
    meter_y = y2m * coordinate_y
    return(round(meter_x, 2), round(meter_y, 2))

def shot_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    # add authorization
    obj, _created = Shot.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
    obj.save()
    return obj.shot_id

def zone_name_get(logger, coordinate_x, coordinate_y):
    """ get coordinates """
    (meter_x, meter_y) = _shoot_coordinates_convert(coordinate_x, coordinate_y)
    # constructing shot location
    shot_pnt = Point(meter_x, meter_y)
    shot_zone = None
    # determining shot zone
    for poly_name, poly in rd.polygons:
        if poly.intersects(shot_pnt):
            shot_zone = poly_name[5:]
            break
    return shot_zone.lower()
