# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413, C0116
from rest.functions.timeline import skatersonice_get, penalties_include
from rest.functions.periodevent import scorersfromevents_get
from rest.functions.helper import shot_leaffan_sync, list_sumup, deviation_avg_get, minmax_get
from rest.functions.periodevent import periodevent_get
from rest.functions.shot import shotspermin_count, shotspermin_aggregate
from rest.functions.chartparameters import chart_color6, plotlines_color, title, font_size, corner_annotations, text_color

def _rosterinformation_add(logger, player_corsi_dic, toi_dic, scorer_dic, roster_list):
    """ enrich corsi dictionary with roster information like time-on-ice or line-number """
    logger.debug('_rosterinformation_add()')

    #  here are the roster
    for selector in roster_list:
        if selector == 'home':
            team = 'home_team'
        else:
            team = 'visitor_team'

        for player in roster_list[selector]:
            if roster_list[selector][player]['position'] != 'GK':
                player_name = '{0} {1}'.format(roster_list[selector][player]['name'], roster_list[selector][player]['surname'])
                if player_name in player_corsi_dic[team]:
                    player_corsi_dic[team][player_name]['line_number'] = int(roster_list[selector][player]['roster'][1])
                    player_corsi_dic[team][player_name]['jersey'] = roster_list[selector][player]['jersey']
                    player_corsi_dic[team][player_name]['player_id'] = roster_list[selector][player]['playerId']
                else:
                    player_corsi_dic[team][player_name] = {'shots': 0, 'shots_against': 0, 'name': player_name, 'jersey': roster_list[selector][player]['jersey'], 'player_id': roster_list[selector][player]['playerId']}

                if player_name in toi_dic[team]:
                    player_corsi_dic[team][player_name]['toi'] = toi_dic[team][player_name]
                else:
                    player_corsi_dic[team][player_name]['toi'] = 1

                if player_corsi_dic[team][player_name]['jersey'] in scorer_dic[team]['scorer_list']:
                    player_corsi_dic[team][player_name]['goal'] = True

                if player_corsi_dic[team][player_name]['jersey'] in scorer_dic[team]['assist_list']:
                    player_corsi_dic[team][player_name]['assist'] = True

                if player_corsi_dic[team][player_name]['shots'] + player_corsi_dic[team][player_name]['shots_against'] == 0:
                    player_corsi_dic[team][player_name]['cf_pctg'] = 0
                else:
                    player_corsi_dic[team][player_name]['cf_pctg'] = int(round(player_corsi_dic[team][player_name]['shots'] * 100/(player_corsi_dic[team][player_name]['shots'] + player_corsi_dic[team][player_name]['shots_against']), 0))

                player_corsi_dic[team][player_name]['corsi'] = player_corsi_dic[team][player_name]['shots'] - player_corsi_dic[team][player_name]['shots_against']

    return player_corsi_dic

def gameplayercorsi_get(logger, shot_list, shift_list, periodevent_list, matchinfo_dic, roster_list, five_filter=True):
    """ get corsi values per player for a certain match """
    # pylint: disable=R0914
    logger.debug('gamecorsi_get()')


    # soi = seconds on ice
    (soi_dic, toi_dic) = skatersonice_get(logger, shift_list, matchinfo_dic)

    if toi_dic['home_team'] and toi_dic['visitor_team']:

        # add penalties to filter 5v5
        soi_dic = penalties_include(logger, soi_dic, periodevent_list)

        # get scorers from events
        scorer_dic = scorersfromevents_get(logger, periodevent_list)

        player_corsi_dic = {'home_team': {}, 'visitor_team': {}}

        for shot in shot_list:

            # skip goals
            # if shot['match_shot_resutl_id'] == 4:
            #    continue

            if five_filter and shot['timestamp'] in soi_dic['home_team'] and shot['timestamp'] in soi_dic['visitor_team']:
                # so far a bid unclear we only count 5vs5
                # 5v5 is ok we can count it
                # pylint: disable=R1703
                if 'count' in soi_dic['home_team'][shot['timestamp']] and 'count' in soi_dic['visitor_team'][shot['timestamp']] and soi_dic['home_team'][shot['timestamp']]['count'] == 5 and soi_dic['visitor_team'][shot['timestamp']]['count'] == 5:
                # if soi_dict['EBB'][shot['time']]['count'] == soi_dict[oteam_name][shot['time']]['count']:
                    count_it = True
                # elif soi_dict['EBB'][shot['time']]['count'] == 4 and soi_dict[oteam_name][shot['time']]['count'] == 4:
                #     count_it = True
                else:
                    count_it = False
            else:
                count_it = True

            if count_it:

                # we need to differenciate between home and visitor team
                if shot['team_id'] == matchinfo_dic['home_team_id']:
                    for_team = 'home_team'
                    against_team = 'visitor_team'
                else:
                    against_team = 'home_team'
                    for_team = 'visitor_team'
                if shot['timestamp'] in soi_dic['home_team'] and shot['timestamp'] in soi_dic['visitor_team']:
                    for player in soi_dic[for_team][shot['timestamp']]['player_list']:
                        if player not in player_corsi_dic[for_team]:
                            player_corsi_dic[for_team][player] = {'shots': 0, 'shots_against': 0, 'name': player}
                        player_corsi_dic[for_team][player]['shots'] += 1

                    for player in soi_dic[against_team][shot['timestamp']]['player_list']:
                        if player not in player_corsi_dic[against_team]:
                            player_corsi_dic[against_team][player] = {'shots': 0, 'shots_against': 0, 'name': player}
                        player_corsi_dic[against_team][player]['shots_against'] += 1

        player_corsi_dic = _rosterinformation_add(logger, player_corsi_dic, toi_dic, scorer_dic, roster_list)
    else:
        player_corsi_dic = {}

    final_player_corsi_dic = {}
    # consistency check delete all entries without corsi
    for team in player_corsi_dic:
        final_player_corsi_dic[team] = {}
        for player in player_corsi_dic[team]:
            if 'corsi' in player_corsi_dic[team][player] and 'toi' in player_corsi_dic[team][player]:
                final_player_corsi_dic[team][player] = player_corsi_dic[team][player]

    return final_player_corsi_dic

def gameshots5v5_get(logger, match_info_dic, team, shot_list, shift_list, periodevent_list):
    # pylint: disable=R0914
    logger.debug('gameshots5v5_get()')

    # get shifts and shots
    # shot_list = shot_list_get(logger, 'match_id', match_id, ['real_date', 'shot_id', 'match_id', 'timestamp', 'match_shot_resutl_id', 'team_id', 'player__first_name', 'player__last_name', 'zone', 'coordinate_x', 'coordinate_y', 'player__jersey'])

    # soi = seconds on ice
    (soi_dic, _toi_dic) = skatersonice_get(logger, shift_list, match_info_dic)

    # add penalties to filter 5v5
    soi_dic = penalties_include(logger, soi_dic, periodevent_list)

    shots_for_5v5 = 0
    shots_against_5v5 = 0
    shots_ongoal_for_5v5 = 0
    shots_ongoal_against_5v5 = 0
    shot_list_5v5 = []

    # hack to sync data with Leaffan.net we aer skipping late corrections form next day
    ltime = 0
    ldate = 'foo'
    for shot in shot_list:
        # sync shots with leaffan
        (process_shot, ltime, ldate) = shot_leaffan_sync(shot, ltime, ldate)
        if process_shot:
            home_penalty = False
            if shot['timestamp'] in soi_dic['home_team']:
                if 'penalty' in soi_dic['home_team'][shot['timestamp']]:
                    home_penalty = True
            visitor_penalty = False
            if shot['timestamp'] in soi_dic['visitor_team']:
                if 'penalty' in soi_dic['visitor_team'][shot['timestamp']]:
                    visitor_penalty = True

            count_shot = False
            if home_penalty == visitor_penalty:
                count_shot = True

            try:
                home_count = soi_dic['visitor_team'][shot['timestamp']]['count']
            except BaseException:
                home_count = 0
            # _visitor_count = soi_dic['visitor_team'][shot['timestamp']]['count']

            # count only shots at 5v5
            if count_shot:
                shot_list_5v5.append(shot)
            # if home_count == 5 and visitor_count == 5:
                if team == 'home':
                    # we count from perspectiv of the come team
                    if shot['team_id'] == match_info_dic['home_team_id']:
                        # this is a shot of the home_team
                        shots_for_5v5 += 1
                        if shot['match_shot_resutl_id'] in (1, 4, 5):
                            # sog_filter
                            shots_ongoal_for_5v5 += 1
                    else:
                        shots_against_5v5 += 1
                        if home_count == 5:
                            shots_ongoal_against_5v5 += 1
                else:
                    # we count from perpsective of visitor team
                    # we count from perspectiv of the come team
                    if shot['team_id'] == match_info_dic['home_team_id']:
                        # this is a shot of the come_team
                        shots_against_5v5 += 1
                        if shot['match_shot_resutl_id'] in (1, 4, 5):
                            # sog_filter
                            shots_ongoal_against_5v5 += 1
                    else:
                        shots_for_5v5 += 1
                        if home_count == 5:
                            shots_ongoal_for_5v5 += 1

    return (shots_for_5v5, shots_against_5v5, shots_ongoal_for_5v5, shots_ongoal_against_5v5, shot_list_5v5)

def pace_data_get(logger, ismobile, teamstat_dic, teams_dic):
    # pylint: disable=R0914
    """ get pace data """
    logger.debug('pace_data_get()')

    if ismobile:
        image_width = 25
    else:
        image_width = 40
    image_height = image_width

    (pace_sum_dic, update_amount) = _pace_sumup(logger, teamstat_dic)

    # build temporary dictionary for date. we build the final sorted in next step
    pace_lake = {}
    shot_rate_lake = {}
    shot_share_lake = {}
    for ele in range(1, update_amount+1):
        pace_lake[ele] = []
        shot_rate_lake[ele] = []
        shot_share_lake[ele] = []

    for team_id in pace_sum_dic:
        # harmonize lengh by adding list elements at the beginning
        if len(pace_sum_dic[team_id]) < update_amount:
            for ele in range(0, update_amount - len(pace_sum_dic[team_id])):
                pace_sum_dic[team_id].insert(0, pace_sum_dic[team_id][0])

        for idx, ele in enumerate(pace_sum_dic[team_id], 1):
            pace_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(teams_dic[team_id]['team_logo'])},
                'sum_shots_for_5v5_60': ele['sum_shots_for_5v5_60'],
                'sum_shots_against_5v5_60': ele['sum_shots_against_5v5_60'],
                'sum_shots_5v5_60': ele['sum_shots_5v5_60'],
                # 'x': ele,
                'y': ele['sum_shots_5v5_60']
            })

            shot_rate_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(teams_dic[team_id]['team_logo'])},
                'x': ele['sum_shots_for_5v5_60'],
                'y': ele['sum_shots_against_5v5_60']
            })

            shot_share_lake[idx].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(teams_dic[team_id]['team_logo'])},
                'sum_shots_for_5v5_60': ele['sum_shots_for_5v5_60'],
                'sum_shots_against_5v5_60': ele['sum_shots_against_5v5_60'],
                'y': ele['sum_shots_for_5v5_60'] - ele['sum_shots_against_5v5_60']
            })

    # build final dictionary
    pace_chartseries_dic = pace_chartseries_get(logger, pace_lake)
    shotrate_chartseries_dic = pace_chartseries_get(logger, shot_rate_lake)
    shotshare_chartseries_dic = pace_chartseries_get(logger, shot_share_lake)

    return (pace_chartseries_dic, shotrate_chartseries_dic, shotshare_chartseries_dic)

def _pace_sumup(logger, teamstat_dic):
    """ sumup shots and generate 60 values """
    logger.debug('_pace_sumup()')

    update_amount = 0
    pace_sum_dic = {}
    for team_id in teamstat_dic:
        # sumup data per team
        pace_sum_dic[team_id] = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'shots_for_5v5', 'shots_against_5v5', 'matchduration'])
        # check how many items we have to create in update_dic
        if update_amount < len(pace_sum_dic[team_id]):
            update_amount = len(pace_sum_dic[team_id])

        for ele in pace_sum_dic[team_id]:
            # we nbeed to add the 60 data
            sum_shots_for_5v5 = ele['sum_shots_for_5v5']
            sum_shots_against_5v5 = ele['sum_shots_against_5v5']
            sum_matchduration = ele['sum_matchduration']

            # calculate 60
            ele['sum_shots_for_5v5_60'] = round(sum_shots_for_5v5 *  3600 / sum_matchduration, 0)
            ele['sum_shots_against_5v5_60'] = round(sum_shots_against_5v5 * 3600 / sum_matchduration, 0)
            ele['sum_shots_5v5_60'] = ele['sum_shots_for_5v5_60'] + ele['sum_shots_against_5v5_60']

    return (pace_sum_dic, update_amount)

def pace_chartseries_get(logger, data_dic, minmax=False):
    """ build structure for chart series """
    logger.debug('pace_chartseries_get()')
    chartseries_dic = {}
    for ele in data_dic:
        chartseries_dic[ele] = {'data': []}
        for datapoint in sorted(data_dic[ele], key=lambda i: i['y']):
            chartseries_dic[ele]['data'].append(datapoint)

        # get statistic values we need
        deviation_dic = deviation_avg_get(logger, chartseries_dic[ele]['data'], ['x', 'y'])

        for value in deviation_dic:
            chartseries_dic[ele]['{0}_deviation'.format(value)] = deviation_dic[value]['std_deviation']
            chartseries_dic[ele]['{0}_min'.format(value)] = deviation_dic[value]['min']
            chartseries_dic[ele]['{0}_max'.format(value)] = deviation_dic[value]['max']
            chartseries_dic[ele]['{0}_avg'.format(value)] = deviation_dic[value]['average']

            if minmax:
                # set minmax to the same values
                (min_, max_) = minmax_get(deviation_dic[value]['min'], deviation_dic[value]['max'], deviation_dic[value]['average'])
                chartseries_dic[ele]['{0}_min_minmax'.format(value)] = min_
                chartseries_dic[ele]['{0}_max_minmax'.format(value)] = max_

    return chartseries_dic

def pace_updates_get(logger, data_dic, ctitle):
    logger.debug('pace_updates_get()')

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
                    'min': data_dic[ele]['y_min'] - 2,
                    'max':  data_dic[ele]['y_max'] + 2,
                    'plotBands': [{'from':  data_dic[ele]['y_avg'] -  data_dic[ele]['y_deviation']/2, 'to':  data_dic[ele]['y_avg'] +  data_dic[ele]['y_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 3, 'value':  data_dic[ele]['y_avg']}],
                },
            }
        }

    return updates_dic

def shotrates_updates_get(logger, data_dic):
    logger.debug('shotrates_updates_get()')

    updates_dic = {}

    for ele in data_dic:

        minmax_dic = {
            'x_min': round(data_dic[ele]['x_min'] - 1, 0),
            'y_min': round(data_dic[ele]['y_min'] - 1, 0),
            'x_max': round(data_dic[ele]['x_max'] + 1, 0),
            'y_max': round(data_dic[ele]['y_max'] + 1, 0)
        }

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
                'xAxis': {
                    # pylint: disable=E0602
                    'title': title(_('Corsi For per 60 minutes at 5v5 (Cf/60)'), font_size),
                    'min': minmax_dic['x_min'],
                    'max':  minmax_dic['x_max'],
                    'tickInterval': 1,
                    'gridLineWidth': 1,
                    'plotBands': [{'from':  data_dic[ele]['x_avg'] -  data_dic[ele]['x_deviation']/2, 'to':  data_dic[ele]['x_avg'] +  data_dic[ele]['x_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 2, 'value':  data_dic[ele]['x_avg']}],
                },
                'yAxis': {
                    # pylint: disable=E0602
                    'title': title(_('Corsi Against per 60 minutes at 5v5 (Ca/60)'), font_size),
                    'min': minmax_dic['y_min'],
                    'max':  minmax_dic['y_max'],
                    'tickInterval': 1,
                    'gridLineWidth': 1,
                    'plotBands': [{'from':  data_dic[ele]['y_avg'] -  data_dic[ele]['y_deviation']/2, 'to':  data_dic[ele]['y_avg'] +  data_dic[ele]['y_deviation']/2, 'color': chart_color6}],
                    'plotLines': [{'zIndex': 3, 'color': plotlines_color, 'width': 3, 'value':  data_dic[ele]['y_avg']}],
                },
                # pylint: disable=E0602
                'annotations': corner_annotations(None, minmax_dic, _('Bad'), _('Dull'), _('Fun'), _('Good')),
            }
        }

    return updates_dic

def goals5v5_get(logger, match_id, _match_info_dic):
    logger.debug('goals5v5_get({0})'.format(match_id))

    # create empty dictionary
    goals5v5_dic = {'home': 0, 'visitor': 0}

    # get period events
    periodevent_list = periodevent_get(logger, 'match_id', match_id, ['period_event'])
    for period in periodevent_list:
        for event in periodevent_list[period]:
            # filter goals on even strength
            if event['type'] == "goal" and event['data']['balance'] == "EQ":
                goals5v5_dic[event['data']['team']] += 1

    return goals5v5_dic

def gamecorsi_get(logger, shot_list, shot_list_5v5, matchinfo_dic, color_dic):
    logger.debug('gamecorsi_get()')

    # get shots and goals per min
    (_shotmin_dic, goal_dic) = shotspermin_count(logger, shot_list, matchinfo_dic)
    (shotmin_dic, _goal_dic) = shotspermin_count(logger, shot_list_5v5, matchinfo_dic)
    # aggregate 5v5 shots per min
    shotsum_dic = shotspermin_aggregate(logger, shotmin_dic)

    corsi_dic = {}
    for min_, _value in shotsum_dic['home_team'].items():
        corsi = shotsum_dic['visitor_team'][min_] - shotsum_dic['home_team'][min_]
        if min_ in goal_dic['home_team'].keys():
            # corsi_dic[min_] = {'y': corsi, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['home_team_logo'])}, 'dataLabels': {'enabled': 1, 'color': chart_color4, 'format': '{0}'.format(goal_dic['home_team'][min_])}}
            corsi_dic[min_] = {'y': corsi, 'marker' : {'enabled': 1, 'fillColor': color_dic['home_team_color_primary']}, 'dataLabels': {'enabled': 1, 'color': text_color, 'format': '{0}'.format(goal_dic['home_team'][min_])}}
            # corsi_dic[min_] = {'y': corsi, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['home_team_logo'])}}

        elif min_ in goal_dic['visitor_team'].keys():
            # corsi_dic[min_] = {'y': corsi, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['visitor_team_logo'])}, 'dataLabels': {'enabled': 1, 'color': chart_color4, 'format': '{0}'.format(goal_dic['visitor_team'][min_])}}
            corsi_dic[min_] = {'y': corsi, 'marker' : {'enabled': 1, 'fillColor': color_dic['visitor_team_color_secondary']}, 'dataLabels': {'enabled': 1, 'color': text_color, 'format': '{0}'.format(goal_dic['visitor_team'][min_])}}
            # corsi_dic[min_] = {'y': corsi, 'marker' : {'enabled': 1, 'width': 25, 'height': 25, 'symbol': 'url({0})'.format(matchinfo_dic['visitor_team_logo'])}}
        else:
            corsi_dic[min_] = corsi

    return corsi_dic
