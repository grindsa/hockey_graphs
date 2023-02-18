# -*- coding: utf-8 -*-
""" list of functions for faceoff statistics """
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
import math
from rest.models import Faceoff
from rest.functions.chartparameters import plotlines_color, chart_color6, title, font_size
from rest.functions.corsi import pace_chartseries_get
from rest.functions.helper import list_sumup, pctg_float_get


def faceoff_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('faceoff_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add faceoff
        obj, _created = Faceoff.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in faceoff_add(): {0}'.format(err_))
        result = None
    logger.debug('faceoff_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def faceoff_get(logger, fkey, fvalue, vlist=('match_id', 'shift')):
    """ get info for a specifc match_id """
    logger.debug('faceoff_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            faceoff_dic = list(Faceoff.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            faceoff_dic = Faceoff.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except BaseException:
        shift_dic = {}

    return faceoff_dic

def _faceoff_sumup(logger, teamstat_dic):
    """ sum up faceoff statistics """
    logger.debug('_faceoff_sumup()')

    update_amount = 0
    teamstat_sum_dic = {}

    for team_id in teamstat_dic:
        # sumup data per team
        teamstat_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'faceoffswon', 'faceoffslost'])
        # check how many items we have to create in update_dic
        if update_amount < len(teamstat_sum_dic[team_id]):
            update_amount = len(teamstat_sum_dic[team_id])

    return (teamstat_sum_dic, update_amount)

def faceoff_overview_get(logger, ismobile, teamstat_dic, teams_dic):
    """ collect data for faceoff overview chart """
    logger.debug('faceoff_overview_get()')

    if ismobile:
        image_width = 25
        image_height = 25
    else:
        image_width = 40
        image_height = 40

    # get summary
    (faceoffsum_dic, update_amount) = _faceoff_sumup(logger, teamstat_dic)

    # build temporary dictionary for date. we build the final sorted in next step
    faceoff_lake = {}
    for ele in range(1, update_amount+1):
        faceoff_lake[ele] = []

    for team_id in faceoffsum_dic:
        # harmonize lengh by adding list elements at the beginning
        if len(faceoffsum_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(faceoffsum_dic[team_id])):
                faceoffsum_dic[team_id].insert(0, faceoffsum_dic[team_id][0])

        for idx, ele in enumerate(faceoffsum_dic[team_id], 1):
            faceoff_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(teams_dic[team_id]['team_logo'])},
                'sum_faceoffslost': ele['sum_faceoffslost'],
                'sum_faceoffswon': ele['sum_faceoffswon'],
                # 'x': ele,
                'y': pctg_float_get(ele['sum_faceoffswon'], (ele['sum_faceoffswon'] + ele['sum_faceoffslost']), 1)
            })

    # build final dictionary
    faceoff_chartseries_dic = pace_chartseries_get(logger, faceoff_lake, True)

    return faceoff_chartseries_dic

def faceoffs_updates_get(logger, ctitle, data_dic):
    """ get data for slider update """
    logger.debug('faceoffs_updates_get()')

    updates_dic = {}

    for ele in data_dic:
        updates_dic[ele] = {
            'text': ele,
            'chartoptions':  {
                'series': [{
                    # pylint: disable=E0602
                    'name': _('Standard Deviation'),
                    'color': plotlines_color,
                    'marker': {'symbol': 'square'},
                    'data': data_dic[ele]['data']
                }],
                'yAxis': {
                    'title': title(ctitle, font_size),
                    'min': data_dic[ele]['y_min_minmax'] - 2,
                    'max':  data_dic[ele]['y_max_minmax'] + 2,
                    'plotBands': [{'from':  data_dic[ele]['y_avg'] -  data_dic[ele]['y_deviation']/2, 'to':  data_dic[ele]['y_avg'] +  data_dic[ele]['y_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 3, 'value':  data_dic[ele]['y_avg']}],
                },
            }
        }

    return updates_dic
