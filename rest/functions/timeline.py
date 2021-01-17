# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413

def skatersonice_get(logger, shift_list, matchinfo_dic, add_id=False):
    """ get skaters on ice for a certain match """
    logger.debug('skatersonice_get()')
    skaters_on_ice_dic = {'home_team': {}, 'visitor_team': {}}
    toi_dic = {'home_team': {}, 'visitor_team': {}}

    # get time stamp of last entry
    try:
        time_end = shift_list[-1]['endTime']['time']
    except BaseException:
        time_end = 3900

    # create game timeline in second interval
    for second_ in range(0, time_end + 20):
        skaters_on_ice_dic['home_team'][second_] = {'player_list': [], 'count': 0}
        skaters_on_ice_dic['visitor_team'][second_] = {'player_list': [], 'count': 0}

    # add players to timeline based on shifts
    for shift in shift_list:

        # store some values in variable for faster access
        shift_duration = (shift['endTime']['time'] - shift['startTime']['time'])
        player_name = shift['player']['name']

        if shift['team']['id'] == matchinfo_dic['home_team_id']:
            team_name = 'home_team'
        else:
            team_name = 'visitor_team'

        # count time_on_ice per player
        if player_name not in toi_dic[team_name]:
            toi_dic[team_name][player_name] = 0
        toi_dic[team_name][player_name] += shift_duration

        for second_ in range(shift['startTime']['time']+1, shift['endTime']['time']+1):
            # add player_ids or names
            if add_id:
                skaters_on_ice_dic[team_name][second_]['player_list'].append(shift['player']['id'])
            else:
                skaters_on_ice_dic[team_name][second_]['player_list'].append(player_name)
            skaters_on_ice_dic[team_name][second_]['count'] += 1

    return (skaters_on_ice_dic, toi_dic)

def penalties_include(logger, soi_dic, period_events):
    """ add penalties to game dictionary """
    logger.debug('penalties_include()')

    for period in period_events:

        #print(period)
        for event in period_events[period]:
            if event['type'] == 'penalty':
                if event['data']['team'] == 'home':
                    team = 'home_team'
                else:
                    team = 'visitor_team'

                # ignoriere match strafen größer als 5min
                if event['data']['duration'] < 301:
                    for second_ in range(event['data']['time']['from']['scoreboardTime']+1, event['data']['time']['to']['scoreboardTime']+1):
                        if second_ not in soi_dic[team]:
                            soi_dic[team][second_] = {}
                        if 'penalty' in soi_dic[team][second_]:
                            try:
                                soi_dic[team][second_]['penalty'] = '{0}, {1}'.format(soi_dic[team][second_]['penalty'], event['data']['disciplinedPlayer']['surname'])
                            except BaseException:
                                soi_dic[team][second_]['penalty'] = '{0}'.format(soi_dic[team][second_]['penalty'])
                        else:
                            if event['data']['disciplinedPlayer']:
                                soi_dic[team][second_]['penalty'] = event['data']['disciplinedPlayer']['surname']
                            else:
                                soi_dic[team][second_]['penalty'] = event['data']['replacedPlayer']['surname']

    return soi_dic
