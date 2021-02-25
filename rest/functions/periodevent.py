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

from rest.models import Periodevent
from rest.functions.helper import date_to_uts_utc
from rest.functions.chartparameters import chart_color5, chart_color6

def periodevent_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('periodevent_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add event
        obj, _created = Periodevent.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in periodevent_add(): {0}'.format(err_))
        result = None
    logger.debug('periodevent_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def periodevent_get(logger, fkey, fvalue, vlist=('match_id', 'period_event')):
    """ get info for a specifc match_id """
    logger.debug('periodevent_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            event_dic = list(Periodevent.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            event_dic = Periodevent.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except BaseException:
        event_dic = {}
    return event_dic

def penaltyplotlines_get(logger, fkey, matchid, home_color=chart_color5, visitor_color=chart_color6, scale='min'):
    """ create plotlines for penalites """
    logger.debug('penalty_plotlines_get({0})'.format(matchid))

    # get periodevents
    event_dic = periodevent_get(logger, fkey, matchid, ['period_event'])
    plotline_list = []

    for period in event_dic:
        for event in event_dic[period]:
            # filter penalties
            if event['type'] == 'penalty':
                if scale == 'second':
                    tst_from = event['data']['time']['from']['scoreboardTime']
                    tst_to = event['data']['time']['to']['scoreboardTime']
                elif scale == 'millisecond':
                    tst_from = event['data']['time']['from']['scoreboardTime'] * 1000
                    tst_to = event['data']['time']['to']['scoreboardTime'] * 1000
                else:
                    # convert time to minute
                    tst_from = math.ceil(event['data']['time']['from']['scoreboardTime']/60)
                    tst_to = math.ceil(event['data']['time']['to']['scoreboardTime']/60)
                # create dictionary
                tmp_dic = {'from': tst_from, 'to': tst_to}
                if event['data']['team'] == 'home':
                    tmp_dic['color'] = home_color
                elif event['data']['team'] == 'visitor':
                    tmp_dic['color'] = visitor_color

                # append dictionary to list
                plotline_list.append(tmp_dic)
    return plotline_list

def scorersfromevents_get(logger, period_events):
    """ create dictionry containing scorers and assists """
    logger.debug('scorersfromevents_get()')
    scorer_dic = {'home_team': {'scorer_list': [], 'assist_list': []}, 'visitor_team': {'scorer_list': [], 'assist_list': []}}
    for period in period_events:
        for event in period_events[period]:
            if event['type'] == 'goal':
                team = '{0}_team'.format(event['data']['team'])
                # store scorer
                if event['data']['scorer']['jersey'] not in scorer_dic[team]['scorer_list']:
                    scorer_dic[team]['scorer_list'].append(event['data']['scorer']['jersey'])
                # store assists
                for player in event['data']['assistants']:
                    if player['jersey'] not in scorer_dic[team]['assist_list']:
                        scorer_dic[team]['assist_list'].append(player['jersey'])
    return scorer_dic

def penaltiesfromevents_get(logger, period_events):
    """ create dictionry of penalties """
    logger.debug('penaltiesfromevents_get()')
    penalty_dic = {'home_team': [], 'visitor_team': []}
    for period in period_events:
        for event in period_events[period]:
            if event['type'] == 'penalty':
                team = '{0}_team'.format(event['data']['team'])
                # store penalty seconds
                penalty_dic[team].extend(range(event['data']['time']['from']['scoreboardTime'], event['data']['time']['to']['scoreboardTime'], 1))
                penalty_dic[team].append(event['data']['time']['to']['scoreboardTime'])

    penalty_dic['home_team'] = list(dict.fromkeys(penalty_dic['home_team']))
    penalty_dic['visitor_team'] = list(dict.fromkeys(penalty_dic['visitor_team']))

    return penalty_dic


def goalsfromevents_get(logger, period_events):
    """ create dictionry containing scorers and assists """
    logger.debug('scorersfromevents_get()')

    goal_dic = {'home_team': [], 'visitor_team': []}

    # timezone offset
    tz_offset = 3600

    # filter for goals
    for period in period_events:
        for event in period_events[period]:
            # filter for goals and period events
            if event['type'] == 'goal':
                # differenciate between home and visitor
                team = '{0}_team'.format(event['data']['team'])
                # calculate uts
                event['uts'] = date_to_uts_utc(event['data']['realTime']) - tz_offset
                goal_dic[team].append(event)

    return goal_dic

def goalplotlines_get(logger, events_dic, goal_dic, home_team_name, home_team_color, visitor_team_name, visitor_team_color):
    """ create plotlines from goal information """
    logger.debug('_gamematchup_get()')

    plotline_list = []
    for team in goal_dic:
        color = visitor_team_color
        team_name = visitor_team_name
        if team == 'home_team':
            color = home_team_color
            team_name = home_team_name
        for goal in goal_dic[team]:
            plotline_list.append({'color': color, 'from': goal['uts']-50, 'to': goal['uts']+50})
            events_dic[goal['uts']] = {'created_at': goal['data']['realTime'], 'created_uts': goal['uts'], 'color': color, 'name_alternate': 'TOR {0}: {1}'.format(team_name, goal['data']['currentScore']), 'source': 'grindsa'}

    return (plotline_list, events_dic)

def goaliepull_get(logger, team, periodevent_list):
    """ get goaliepull information """
    logger.debug('goaliepull_get()')

    goaliepull_dic = {
        'goalieown_pull': 0,
        'goalieother_pull': 0,
        'goaliepull_time': 0,
        'goals_en_for': 0,
        'goals_en_against': 0,
        'goals_wogoalie_for': 0,
    }

    goaliepull = False
    for period in periodevent_list:
        for event in periodevent_list[period]:
            # filter goalkeeperchanges
            if 'data' in event and 'type' in event and event['type'] == 'goalkeeperChange':
                # detect goalie pull
                if not goaliepull and 'outgoingGoalkeeper' in event['data'] and event['data']['outgoingGoalkeeper'] and 'player' in event['data'] and not bool(event['data']['player']):
                    # print('goalie-out', event['time'])
                    goaliepull = True
                    if event['data']['team'] == team:
                        # own goaliepull
                        goaliepull_dic['goalieown_pull'] = 1
                    else:
                        # other goaliepull
                        goaliepull_dic['goalieother_pull'] = 1
                    goaliepull_dic['goaliepull_time'] = 3600 - event['time']
                elif goaliepull and 'player' in event['data'] and bool(event['data']['player']) and 'outgoingGoalkeeper' in event['data'] and not bool(event['data']['outgoingGoalkeeper']):
                    # print('goalie-in', event['time'])
                    goaliepull = False

            # detect emptynet
            # pylint: disable=R0916
            if goaliepull and 'data' in event and 'type' in event and event['type'] == 'goal' and 'en' in event['data'] and bool(event['data']['en']):
                if event['data']['team'] == team:
                    goaliepull_dic['goals_en_for'] += 1
                else:
                    goaliepull_dic['goals_en_against'] += 1
            elif goaliepull and 'data' in event and 'type' in event and event['type'] == 'goal':
                # print('goal-for pulling out', event['time'])
                # this is a goal after goalie pull but no emptynet
                if event['data']['team'] == team and goaliepull_dic['goalieown_pull'] == 1:
                    # the team which did pull the goalie scored
                    goaliepull_dic['goals_wogoalie_for'] += 1

    return goaliepull_dic
