# -*- coding: utf-8 -*-
""" toi tables """

def gametoi_table(logger, toi_dic):
    """ time on ice tables """
    # pylint: disable=E0602
    logger.debug('shotsperiodtable_get()')

    table_dic = {'th': ['Name', _('1st Period'), _('2nd Period'), _('3rd Period'), _('OT')], 'align': ['w3-left-align', None, None, None, None], 'td': []}

    playername_list = []

    for period in toi_dic:
        for player_name in toi_dic[period]:
            if player_name not in playername_list:
                playername_list.append(player_name)

    for player_name in sorted(playername_list):

        if player_name not in toi_dic[1]:
            p1_val = '00:00'
        else:
            p1_val = '{0:02d}:{1:02d}'.format(*divmod(toi_dic[1][player_name], 60))

        if player_name not in toi_dic[2]:
            p2_val = '00:00'
        else:
            p2_val = '{0:02d}:{1:02d}'.format(*divmod(toi_dic[2][player_name], 60))

        if player_name not in toi_dic[3]:
            p3_val = '00:00'
        else:
            p3_val = '{0:02d}:{1:02d}'.format(*divmod(toi_dic[3][player_name], 60))

        if player_name not in toi_dic[4]:
            p4_val = '00:00'
        else:
            p4_val = '{0:02d}:{1:02d}'.format(*divmod(toi_dic[4][player_name], 60))


        table_dic['td'].append([player_name, p1_val, p2_val, p3_val, p4_val])

    return table_dic
