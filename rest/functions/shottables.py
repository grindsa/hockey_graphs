# -*- coding: utf-8 -*-
""" list of functions for shottables """

def shotsperiodtable_get(logger, title, shot_min_dic, matchinfo_dic):
    """ get table with list of shotperiod """
    logger.debug('shotsperiodtable_get()')

    tmp_name_dic = {
        'home_team': {'name': matchinfo_dic['home_team__team_name'], 'logo': matchinfo_dic['home_team_logo']},
        'visitor_team': {'name': matchinfo_dic['visitor_team__team_name'], 'logo': matchinfo_dic['visitor_team_logo']}
    }
    # head-lines
    table_dic = {'th': ['', title, '1st', '2nd', '3rd', 'OT', _('Total')], 'align': [None, 'left', None, None, None, None, None], 'td': []}
    for ele in ('home_team', 'visitor_team'):
        sp1 = 0
        sp2 = 0
        sp3 = 0
        sot = 0
        for min_ in shot_min_dic[ele]:
            if min_ < 21:
                sp1 += shot_min_dic[ele][min_]
            elif min_ < 41:
                sp2 += shot_min_dic[ele][min_]
            elif min_ < 61:
                sp3 += shot_min_dic[ele][min_]
            else:
                sot += shot_min_dic[ele][min_]
        table_dic['td'].append([tmp_name_dic[ele]['logo'], tmp_name_dic[ele]['name'], sp1, sp2, sp3, sot, sp1+sp2+sp3+sot])
    return table_dic
