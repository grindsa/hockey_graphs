# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
from rest.functions.timeline import skatersonice_get, penalties_include
from rest.functions.periodevent import scorersfromevents_get
from rest.functions.shift import shift_get, toifromshifts_get
from rest.functions.shot import shot_list_get

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

def gamecorsi_get(logger, shot_list, shift_list, periodevent_list, matchinfo_dic, roster_list, five_filter=True):
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

            # do we have to count the shot
            if five_filter:
                # so far a bid uncliear we only count 5vs5
                # 5v5 is ok we can count it
                if soi_dic['home_team'][shot['timestamp']]['count'] == 5 and soi_dic['visitor_team'][shot['timestamp']]['count'] == 5:
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

    return player_corsi_dic

def gamecorsisum_get(logger, match_id, match_info_dic, team):

        # get shifts and shots
        shot_list = shot_list_get(logger, 'match_id', match_id, ['timestamp', 'match_shot_resutl_id', 'team_id', 'player__first_name', 'player__last_name', 'zone', 'coordinate_x', 'coordinate_y', 'player__jersey'])
        shift_list = shift_get(logger, 'match_id', match_id, ['shift'])

        # soi = seconds on ice
        (soi_dic, toi_dic) = skatersonice_get(logger, shift_list, match_info_dic)

        corsi_for = 0
        corsi_for_5 = 0
        corsi_against = 0
        corsi_against_5 = 0

        for shot in shot_list:
            home_count = soi_dic['home_team'][shot['timestamp']]['count']
            visitor_count = soi_dic['visitor_team'][shot['timestamp']]['count']
            # count only shots at even strength
            if home_count == visitor_count:
                if team == 'home':
                    # we count from perspectiv of the come team
                    if shot['team_id'] == match_info_dic['home_team_id']:
                        # this is a shot of the come_team
                        corsi_for += 1
                        if home_count == 5:
                            corsi_for_5 += 1
                    else:
                        corsi_against +=1
                        if home_count == 5:
                            corsi_against_5 += 1
                else:
                    # we count from perpsective of visitor team
                    # we count from perspectiv of the come team
                    if shot['team_id'] == match_info_dic['home_team_id']:
                        # this is a shot of the come_team
                        corsi_against += 1
                        if home_count == 5:
                            corsi_against_5 += 1
                    else:
                        corsi_for +=1
                        if home_count == 5:
                            corsi_for_5 += 1
        return (corsi_for, corsi_for_5, corsi_against, corsi_against_5)
