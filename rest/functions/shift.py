# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Shift

def shift_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('shift_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add shift
        obj, _created = Shift.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in shift_add(): {0}'.format(err_))
        result = None
    logger.debug('shift_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def shift_get(logger, fkey, fvalue, vlist=('match_id', 'shift')):
    """ get info for a specifc match_id """
    logger.debug('shift_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            shift_dic = list(Shift.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            shift_dic = Shift.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except BaseException:
        shift_dic = {}

    return shift_dic

def toifromshifts_get(logger, matchinfo_dic, shift_list):
    """ get time on ice per player"""
    logger.debug('toifromshifts_get()')

    # inititialize dictionaries to store the data
    shift_dic = {'home_team': {1: {}, 2: {}, 3: {}, 4: {}}, 'visitor_team': {1: {}, 2: {}, 3: {}, 4: {}}}

    for shift in shift_list:
        if shift['team']['id'] == matchinfo_dic['home_team_id']:
            team_name = 'home_team'
        else:
            team_name = 'visitor_team'

        # get the shift data we need
        player_name = shift['player']['name']
        period = math.ceil(shift['endTime']['time']/1200)
        shift_duration = (shift['endTime']['time'] - shift['startTime']['time'])

        # create entry if does not exist and add sum
        if player_name not in shift_dic[team_name][period]:
            shift_dic[team_name][period][player_name] = 0

        shift_dic[team_name][period][player_name] += shift_duration

    return shift_dic

def _shifttype_get(logger, team, start_time, end_time, penalty_dic):
    """ get type thype of a shift (pp, pk, normal) """
    logger.debug('_shifttype_get()')

    # home penalty during this shift
    # pylint: disable=R1703
    if start_time in penalty_dic['home_team'] or end_time in penalty_dic['home_team']:
        home_penalty = True
    else:
        home_penalty = False

    # visitor penalty during this shift
    if start_time in penalty_dic['visitor_team'] or end_time in penalty_dic['visitor_team']:
        visitor_penalty = True
    else:
        visitor_penalty = False

    # decide on PP/PK
    if home_penalty != visitor_penalty:
        if home_penalty:
            if team == 'home_team':
                shift_type = _('PK')
            else:
                shift_type = _('PP')
        else:
            if team == 'home_team':
                shift_type = _('PP')
            else:
                shift_type = _('PK')
    else:
        shift_type = _('Even Strength')

    return shift_type

def shiftsperplayer_get(logger, matchinfo_dic, shift_list, roster_list, penalty_dic):
    """  shifts per player """
    logger.debug('shiftsperplayer_get()')

    shift_dic = {'home_team': {}, 'visitor_team': {}}
    for shift in shift_list:

        # we need to differenciate between home and visitor team
        if shift['team']['id'] == matchinfo_dic['home_team_id']:
            team = 'home_team'
        else:
            team = 'visitor_team'

        # we need the type of the shift to set the right color in the chart
        shift_type = _shifttype_get(logger, team, shift['startTime']['time'], shift['endTime']['time'], penalty_dic)

        if shift['player']['id'] not in shift_dic[team]:
            shift_dic[team][shift['player']['id']] = {'shifts': [], 'name': shift['player']['name']}

        shift_dic[team][shift['player']['id']]['shifts'].append({'start': shift['startTime']['time'], 'end': shift['endTime']['time'], 'type': shift_type})

    #  add roster information
    for selector in roster_list:
        team = '{0}_team'.format(selector)
        for player in roster_list[selector]:
            if roster_list[selector][player]['position'] != 'GK':
                pid = roster_list[selector][player]['playerId']
                if pid in shift_dic[team]:
                    shift_dic[team][pid]['role'] = int(roster_list[selector][player]['roster'][0])
                    shift_dic[team][pid]['line_number'] = int(roster_list[selector][player]['roster'][1])
                    shift_dic[team][pid]['position'] = int(roster_list[selector][player]['roster'][2])
                    shift_dic[team][pid]['surname'] = roster_list[selector][player]['surname']
                    shift_dic[team][pid]['jersey'] = roster_list[selector][player]['jersey']

    return shift_dic
