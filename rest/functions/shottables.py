# -*- coding: utf-8 -*-
""" list of functions for shottables """

def shotsperiodtable_get(logger, title, shot_min_dic, matchinfo_dic):
    """ get table with list of shotperiod """
    # pylint: disable=E0602
    logger.debug('shotsperiodtable_get()')

    tmp_name_dic = {
        'home_team': {'name': matchinfo_dic['home_team__team_name'], 'logo': matchinfo_dic['home_team_logo']},
        'visitor_team': {'name': matchinfo_dic['visitor_team__team_name'], 'logo': matchinfo_dic['visitor_team_logo']}
    }
    # head-lines
    table_dic = {'th': ['', title, '1st', '2nd', '3rd', 'OT', _('Total')], 'align': ['w3-center', 'w3-left-align', 'w3-center', 'w3-center', 'w3-center', 'w3-center', 'w3-center'], 'td': []}
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

def shotstatussumtable_get(logger, _title, shot_min_dic, team, _matchinfo_dic):
    """ create shotstat table """
    # pylint: disable=E0602
    logger.debug('shotstatussumtable_get()')

    table_dic = {'th': [_('Shots per Period'), '1st', '2nd', '3rd', 'OT', _('Total')], 'align': ['w3-left-align', None, None, None, None, None], 'td': []}

    status_dic = {1: _('Shots on Goal'), 2: _('missed'), 3: _('blocked'), 4: _('Goals')}
    # 1 - gehalten
    # 2 - vorbei
    # 3 - geblockt
    # 4 - goal

    for ele in (2, 3, 1, 4):
        sp1 = 0
        sp2 = 0
        sp3 = 0
        sot = 0
        for min_ in shot_min_dic[team][ele]:
            if min_ < 21:
                sp1 += shot_min_dic[team][ele][min_]
            elif min_ < 41:
                sp2 += shot_min_dic[team][ele][min_]
            elif min_ < 61:
                sp3 += shot_min_dic[team][ele][min_]
            else:
                sot += shot_min_dic[team][ele][min_]
        table_dic['td'].append([status_dic[ele], sp1, sp2, sp3, sot, sp1+sp2+sp3+sot])

    return table_dic
