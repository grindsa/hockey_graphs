#!/usr/bin/python
# -*- coding: utf-8 -*-
""" this is just a wrapper for prototyping attempts """
import sys
import os
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()

from rest.functions.helper import logger_setup
from rest.functions.team import team_list_get
from rest.functions.helper import list2dic

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


# import zip
import numpy

def ColorDistance1(fst, snd):
    rm = 0.5 * (fst[:, 0] + snd[:, 0])
    drgb = (fst - snd) ** 2
    t = np.array([2 + rm, 4 + 0 * rm, 3 - rm]).T
    return np.sqrt(np.sum(t * drgb, 1))

def ColorDistance(rgb1,rgb2):
    '''d = {} distance between two colors(3)'''
    rm = 0.5*(rgb1[0]+rgb2[0])
    d = sum((2+rm, 4, 3-rm)*(rgb1-rgb2)**2)**0.5
    return d

def hex2rgb(html_color):
    html_color = html_color.lstrip('#')
    rgb_color = tuple(int(html_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb_color

if __name__ == '__main__':

    LOGGER = logger_setup(True)

    team_1 = 'KEV'
    team_2 = 'EBB'

    team_list = team_list_get(LOGGER, None, None, ['team_id', 'team_name', 'shortcut', 'logo', 'color_primary', 'color_penalty_primary'])
    team_dic = list2dic(LOGGER, team_list, 'shortcut')

    html_color1 = team_dic[team_1]['color_primary']
    html_color2 = team_dic[team_2]['color_primary']

    rgb1 = numpy.array(hex2rgb(html_color1))
    rgb2 = numpy.array(hex2rgb(html_color2))
    result = ColorDistance(rgb1,rgb2)
    print(result)

    #html_color1 = team_dic[team_1]['color_penalty_primary']
    #html_color2 = team_dic[team_2]['color_penalty_primary']

    #print(hex2rgb(html_color1))
    #print(hex2rgb(html_color2))
    #rgb1 = numpy.array(hex2rgb(html_color1))
    #rgb2 = numpy.array(hex2rgb(html_color2))
    #result = ColorDistance(rgb1,rgb2)
    #print(result)
