# -*- coding: utf-8 -*-
""" functions to feed age-charts """
from functions.corsi import pace_chartseries_get

def age_overview_get(logger, ismobile, teamstatdel_dic, teams_dic):
    """ get age-statistics per team """
    logger.debug('age_overview_get()')

    if ismobile:
        image_width = 25
        image_height = 25
    else:
        image_width = 40
        image_height = 40

    agelake_dic = {}

    for team in teamstatdel_dic:

        team_id = team['team']
        for position, values in team['agestats']['position'].items():
            if not position in agelake_dic:
                agelake_dic[position] = []

            agelake_dic[position].append({
                'team_name': teams_dic[team_id]['team_name'],
                'shortcut':  teams_dic[team_id]['shortcut'],
                'marker': {'width': image_width, 'height': image_height, 'symbol': 'url({0})'.format(teams_dic[team_id]['team_logo'])},
                'y': [values['age']['min'], values['age']['average'], values['age']['max']]
                # 'x': ele,
            })

    # build final dictionary
    age_chartseries_dic = pace_chartseries_get(logger, agelake_dic)

    return age_chartseries_dic


def league_agestats_get(logger, ismobile, teamstatdel_dic, teams_dic):
    """ get agestatistics for entire league """
    logger.debug('age_overview_get()')

    league_agestats_dic = {}
    for team in teamstatdel_dic:

        for region, values in team['agestats']['region'].items():
            for age, cnt in values.items():
                if int(age) not in league_agestats_dic:
                    league_agestats_dic[int(age)] = {}
                if region not in league_agestats_dic[int(age)]:
                    league_agestats_dic[int(age)][region] = cnt
                else:
                    league_agestats_dic[int(age)][region] += cnt

    return league_agestats_dic