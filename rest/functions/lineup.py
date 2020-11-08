# -*- coding: utf-8 -*-
""" functions for lineup """
import math

def _rosterid_rebuild(_logger, roster_id):
    """ created sorted lineup from roster_list """
    # logger.debug('_rosterid_rebuild({0})'.format(player_id))

    # split id into different pieces
    playerposition = int(roster_id[0])
    line = int(roster_id[1])
    lineposition = int(roster_id[2])

    if playerposition != 1:
        if playerposition == 3:
            # forwards first
            playerposition = 0
        # new player_id
        new_id = int('{0}{1}{2}'.format(line, playerposition, lineposition))
    else:
        new_id = None

    return new_id

def lineup_sort(logger, roster_list):
    """ created sorted lineup from roster_list """
    logger.debug('lineup_sort()')

    lineup_dic = {'home_team': {}, 'visitor_team': {}}
    player_dic = {}
    plotlines_dic = {'home_team': [], 'visitor_team': []}

    for team in roster_list:

        # decide and harmonize on team_name (location in hash)
        if team == 'home':
            team_name = 'home_team'
        else:
            team_name = 'visitor_team'

        _tmp_dic = {}
        for roster_id in roster_list[team]:
            # we need to rebuild player_id and rearrange for easier sorting
            _id = _rosterid_rebuild(logger, roster_id)
            if _id:
                # skip goalies
                _tmp_dic[_id] = roster_id

        # store entries sorted by key( new player_id) and initialize counter for faster access
        cnt = 0
        initial_line = 1
        for key in sorted(_tmp_dic):
            line = math.floor(key/100)
            if line != initial_line:
                # line flip
                plotlines_dic[team_name].append(cnt)
                initial_line = line

            lineup_dic[team_name][cnt] = roster_list[team][_tmp_dic[key]]
            # hope thats correct we need a dictionary to lookup the position in lineup-dic based on player_id
            player_dic[roster_list[team][_tmp_dic[key]]['playerId']] = cnt
            # print(roster_list[team][_tmp_dic[key]]['playerId'], cnt)
            cnt += 1

    return (lineup_dic, player_dic, plotlines_dic)
