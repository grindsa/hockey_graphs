# -*- coding: utf-8 -*-
""" list of functions for matches """
# pylint: disable=E0401, C0413, R0914
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from django.conf import settings
from rest.functions.helper import list_sumup, pctg_float_get, random_file_pick, url_build, uts_now, uts_to_date_utc
from rest.functions.match import pastmatch_list_get
from rest.functions.teammatchstat import teammatchstats_get
from rest.functions.teamstat import teamstat_dic_get


def _bg_image_select(logger, bg_image_list):
    """ bg image selection """
    logger.debug('_bg_image_select()')
    if bg_image_list:
        logger.debug('_bg_image_select(): pick team specific background image')
        file_name = 'img/backgrounds/{0}'.format(random.choice(bg_image_list))
    else:
        # generate random background image
        file_name = 'img/backgrounds/{0}.png'.format(random.randint(1,7))

    return file_name

def prematchoverview_get(logger, request, fkey, fvalue, matchinfo_dic, delstat_dic, color_dic):
    """ get pre-stats """
    logger.debug('prematchoverview_get({0}:{1})'.format(fkey, fvalue))

    prematch_dic = {}
    prematch_dic['background_image'] = '{0}{1}{2}'.format(matchinfo_dic['base_url'], settings.STATIC_URL, _bg_image_select(logger, matchinfo_dic['home_team__bg_images']))
    prematch_dic['date'] = matchinfo_dic['date']
    # prematch_dic['home_team_color'] = color_dic['home_team_color']
    # prematch_dic['visitor_team_color'] = color_dic['visitor_team_color']

    # some texts to be translated
    prematch_dic['txt_gfpg'] = _('Goals For/Game')
    prematch_dic['txt_gapg'] = _('Goals Against/Game')
    prematch_dic['txt_sfpg'] = _('Shots For/Game')
    prematch_dic['txt_sapg'] = _('Shots Against/Game')
    prematch_dic['txt_fac'] = _('Faceoff')
    prematch_dic['txt_bil'] = _('W-L')

    # stats per team per match
    matchstat_list = teammatchstats_get(logger, 'match__season_id', matchinfo_dic['season_id'])
    # stacked stats per team
    teamstat_dic = teamstat_dic_get(logger, matchstat_list)

    # get list of matches for h2h overview
    uts = uts_now()
    past_match_list = pastmatch_list_get(logger, matchinfo_dic['season_id'], uts, ['match_id', 'date', 'date_uts', 'home_team', 'visitor_team', 'result', 'result_suffix', 'finish', 'home_team__logo', 'home_team__shortcut', 'visitor_team__logo', 'visitor_team__shortcut'])

    for team in ('home', 'visitor'):
        prematch_dic['{0}_team_logo'.format(team)] = matchinfo_dic['{0}_team_logo'.format(team)]
        prematch_dic['{0}_team_shortcut'.format(team)] = matchinfo_dic['{0}_team__shortcut'.format(team)]
        prematch_dic['{0}_team_color'.format(team)] = color_dic['{0}_team_color'.format(team)]
        prematch_dic['{0}_fac_pctg'.format(team)] = "%.1f" % delstat_dic[team]['faceOffsWinsPercent']
        prematch_dic['{0}_pk_pctg'.format(team)] = "%.1f" % delstat_dic[team]['penaltyKillingEfficiency']
        prematch_dic['{0}_pp_pctg'.format(team)] = "%.1f" % delstat_dic[team]['powerPlayEfficiency']
        prematch_dic['{0}_goals_for_pg'.format(team)] = "%.2f" % ((delstat_dic[team]['goalScored']['home'] + delstat_dic[team]['goalScored']['away'])/delstat_dic[team]['games'])
        prematch_dic['{0}_goals_against_pg'.format(team)] = "%.2f" % ((delstat_dic[team]['goalsAgainst']['home'] + delstat_dic[team]['goalsAgainst']['away'])/delstat_dic[team]['games'])
        prematch_dic['{0}_wins'.format(team)] = '{0}/{1}/{2}'.format(delstat_dic[team]['regularWins']['home'] + delstat_dic[team]['regularWins']['home'], delstat_dic[team]['overtimeWins']['home'] + delstat_dic[team]['overtimeWins']['home'], delstat_dic[team]['shootoutWins']['home'] + delstat_dic[team]['shootoutWins']['home'])
        prematch_dic['{0}_losses'.format(team)] = '{0}/{1}/{2}'.format(delstat_dic[team]['regularLosses']['home'] + delstat_dic[team]['regularLosses']['home'], delstat_dic[team]['overtimeLosses']['home'] + delstat_dic[team]['overtimeLosses']['home'], delstat_dic[team]['shootoutLosses']['home'] + delstat_dic[team]['shootoutLosses']['home'])
        if not delstat_dic[team]['bilance'] or not delstat_dic[team]['last10']:
            # count matches as its missing in json file
            (bilance, last10) = _winloss_count(logger, matchinfo_dic['season_id'], delstat_dic[team]['teamId'], delstat_dic[team]['bilance'], delstat_dic[team]['last10'], past_match_list)
            prematch_dic['{0}_bilance'.format(team)] = bilance
            prematch_dic['{0}_last10'.format(team)] = last10
        else:
            prematch_dic['{0}_bilance'.format(team)] = delstat_dic[team]['bilance']
            prematch_dic['{0}_last10'.format(team)] = delstat_dic[team]['last10']

    prematchoverview_dic = _pmoshotdata_get(logger, [matchinfo_dic['home_team_id'], matchinfo_dic['visitor_team_id']], teamstat_dic)
    for team_id in prematchoverview_dic:
        if team_id == matchinfo_dic['home_team_id']:
            team = 'home'
        else:
            team = 'visitor'

        for key in prematchoverview_dic[team_id]:
            prematch_dic['{0}_{1}'.format(team, key)] = prematchoverview_dic[team_id][key]

    prematch_dic['h2h_results'] = _h2h_results_get(logger, request, past_match_list, matchinfo_dic['home_team_id'], matchinfo_dic['visitor_team_id'])

    return prematch_dic

def _pmoshotdata_get(logger, team_list, teamstat_dic):
    """ get prematch overview data """
    logger.debug('_pmoshotdata_get()')

    teamstat_sum_dic = {}
    for team_id in team_list:
        teamstat_sum_dic[team_id] = {}
        # sumup data per team
        tmp_list = list_sumup(logger, teamstat_dic[team_id], ['match_id', 'goals_pp', 'goals_pp_against', 'ppcount', 'shcount', 'faceoffslost', 'faceoffswon', 'goals_for', 'goals_against', 'shots_for_5v5', 'shots_against_5v5', 'shots_ongoal_for', 'shots_ongoal_against', 'goals_pp', 'ppcount', 'goals_pp_against', 'shcount', 'saves'])
        games_num = len(tmp_list)

        tmp_dic = tmp_list[-1]
        # shots on goal per game
        teamstat_sum_dic[team_id]['shots_ongoal_for_pg'] = "%.1f" % round(tmp_dic['sum_shots_ongoal_for']/games_num, 1)
        teamstat_sum_dic[team_id]['shots_ongoal_against_pg'] = "%.1f" % round(tmp_dic['sum_shots_ongoal_against']/games_num, 1)
        # corsi
        teamstat_sum_dic[team_id]['corsi_pctg'] = pctg_float_get(tmp_dic['sum_shots_for_5v5'], tmp_dic['sum_shots_for_5v5'] + tmp_dic['sum_shots_against_5v5'], 1)
        # pdo
        teamstat_sum_dic[team_id]['sh_pctg'] = pctg_float_get(tmp_dic['sum_goals_for'], tmp_dic['sum_shots_ongoal_for'], 1)
        teamstat_sum_dic[team_id]['sv_pctg'] = pctg_float_get(tmp_dic['sum_saves'], tmp_dic['sum_shots_ongoal_against'], 1)
        teamstat_sum_dic[team_id]['pdo'] = "%.1f" % (teamstat_sum_dic[team_id]['sh_pctg'] + teamstat_sum_dic[team_id]['sv_pctg'])

    return teamstat_sum_dic

def _winloss_count(logger, season_id, team_id, bilance, last10, match_list):
    """ count win/loss """
    logger.debug('_winloss_count({0}:{1})'.format(season_id, team_id))

    win_all = 0
    loss_all = 0
    win_10 = 0
    loss_10 = 0
    cnt = 0
    for match in sorted(match_list, key=lambda i: i['date_uts'], reverse=True):

        # filter team
        if match['home_team'] == int(team_id) or match['visitor_team'] == int(team_id) and match['finish']:
            cnt += 1
            # could be that there is a pending game
            (home_goals, visitor_goals) = match['result'].split(':', 2)

            if match['home_team'] == int(team_id):
                # home-game
                if int(home_goals) > int(visitor_goals):
                    win_all += 1
                    if cnt <= 10:
                        win_10 += 1
                elif int(home_goals) < int(visitor_goals):
                    loss_all += 1
                    if cnt <= 10:
                        loss_10 += 1
            elif match['visitor_team'] == int(team_id):
                # roadgame
                if int(visitor_goals) > int(home_goals):
                    win_all += 1
                    if cnt <= 10:
                        win_10 += 1
                elif int(visitor_goals) < int(home_goals):
                    loss_all += 1
                    if cnt <= 10:
                        loss_10 += 1

    return ('{0}-{1}'.format(win_all, loss_all), '{0}-{1}'.format(win_10, loss_10))


def _h2h_results_get(logger, request, match_list, home_team_id, visitor_team_id):
    """ get head-to-head results """
    logger.debug('_h2h_results_get({0}:{1})'.format(home_team_id, visitor_team_id))

    base_url = url_build(request.META)

    h2h_list = []
    for match in sorted(match_list, key=lambda i: i['date_uts']):
        # filter finished matches as per team combination
        if (match['home_team'] == int(home_team_id) and match['visitor_team'] == int(visitor_team_id) and match['finish']) or (match['visitor_team'] == int(home_team_id) and match['home_team'] == int(visitor_team_id) and match['finish']):
            tmp_dic = {'home_team_shortcut': match['home_team__shortcut'], 'visitor_team_shortcut': match['visitor_team__shortcut']}
            tmp_dic['home_team_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match['home_team__logo'])
            tmp_dic['visitor_team_logo'] = '{0}{1}{2}'.format(base_url, settings.STATIC_URL, match['visitor_team__logo'])
            if match['result_suffix']:
                tmp_dic['result'] = '{0} {1}'.format(match['result'], match['result_suffix'])
            else:
                tmp_dic['result'] = match['result']
            tmp_dic['date'] = uts_to_date_utc(match['date_uts'], '%d.%m.%Y')
            tmp_dic['match_id'] = match['match_id']
            h2h_list.append(tmp_dic)

    return h2h_list
