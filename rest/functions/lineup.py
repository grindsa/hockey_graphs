# -*- coding: utf-8 -*-

def lineup_sort(logger, roster_list):
    """ created sorted lineup from roster_list """
    logger.debug('lineup_sort()')

    lineup_dic = {'home_team': {}, 'guest_team': {}}

    # from pprint import pprint
    # pprint(roster_list)
