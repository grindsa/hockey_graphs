# -*- coding: utf-8 -*-
""" list of functions for team comparison """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.functions.corsi import pace_data_get, pace_updates_get, shotrates_updates_get
from rest.functions.faceoff import faceoff_overview_get, faceoffs_updates_get
from rest.functions.faceoffcharts import faceoff_overview_chart
from rest.functions.age import age_overview_get, league_agestats_get
from rest.functions.agecharts import age_overviewchart_get, league_agechart_get
from rest.functions.helper import mobile_check, language_get, uts_now, uts_to_date_utc
from rest.functions.comment import comment_get
from rest.functions.pdo import pdo_breakdown_data_get, pdo_overview_data_get, breakdown_updates_get, overview_updates_get, ppg_data_get, ppg_updates_get
from rest.functions.pdocharts import pdo_breakdown_chart, pdo_overview_chart, ppg_chart_get
from rest.functions.playerstat import u23_toi_get
from rest.functions.season import seasonid_get
from rest.functions.shotcharts import pace_chart_get, shotrates_chart_get, shotshare_chart_get, rebound_overview_chart, break_overview_chart
from rest.functions.pppk import pppk_data_get, discipline_updates_get, goaliepull_data, goaliepullendata_get, goaliepullen_updates_get, scoreendata_get, scoreen_updates_get
from rest.functions.pppkchart import pppk_chart_get, discipline_chart_get, goaliepullchart_get, scoreenchart_get
# from rest.functions.bananachart import banana_chart1_create, banana_chart2_create
from rest.functions.shot import rebound_overview_get, break_overview_get, rebound_updates_get
from rest.functions.team import team_dic_get, teams_per_season_get
from rest.functions.teammatchstat import teammatchstats_get
from rest.functions.teamstatdel import teamstatdel_get
from rest.functions.teamstat import teamstat_dic_get
from rest.functions.toicharts import u23_toi_chart
from rest.functions.heatmap import teamcomparison_hmdata_get, teamcomparison_updates_get
from rest.functions.heatmapcharts import teamcomparison_chart_get
from rest.functions.xg import xgfa_data_get, xgfa_updates_get, gfxgf_updates_get, dgf_updates_get
from rest.functions.xgchart import xgfa_chart_get, gfxgf_chart_get, dgf_chart_get

def teamcomparison_get(logger, request, fkey=None, fvalue=None):
    """ matchstatistics grouped by days """
    logger.debug('teamcomparison_get({0}:{1})'.format(fkey, fvalue))

    (_fkey, season_id) = seasonid_get(logger, request)

    # get teams and matchstatistics
    teams_dic = teams_per_season_get(logger, season_id, request.META)
    if not teams_dic:
        teams_dic = team_dic_get(logger, request.META)

    matchstat_list = teammatchstats_get(logger, 'match__season_id', season_id)

    ismobile = mobile_check(logger, request)
    language = language_get(logger, request)

    # stacked stats per team
    teamstat_dic = teamstat_dic_get(logger, matchstat_list)
    teamstatdel_dic = teamstatdel_get(logger, season_id=season_id, vlist=['season', 'team', 'agestats'])
    teamstatdel_ly_dic = teamstatdel_get(logger, season_id=season_id-1, vlist=['season', 'team', 'agestats'])

    result = []

    stat_entry = {}
    stat_entry = _teamcomparison_heatmap_get(logger, ismobile, language, teamstat_dic, teams_dic)
    if stat_entry:
        result.append(stat_entry)

    # create PDO breakdown chart
    result.extend(_pdo_breakdown_get(logger, ismobile, teamstat_dic, teams_dic))

    # 5on5 shotcharts
    result.extend(_5v5_pace_get(logger, ismobile, teamstat_dic, teams_dic))

    # faceoff wins
    stat_entry = _faceoff_pctg_get(logger, ismobile, teamstat_dic, teams_dic)
    if stat_entry:
        result.append(stat_entry)

    # rebound efficentcy
    stat_entry = _rebound_pctg_get(logger, ismobile, teamstat_dic, teams_dic)
    if stat_entry:
        result.append(stat_entry)

    # rebound efficentcy
    stat_entry = _break_pctg_get(logger, ismobile, teamstat_dic, teams_dic)
    if stat_entry:
        result.append(stat_entry)

    # Special teams performance
    result.extend(_pppk_pctg_get(logger, ismobile, teamstat_dic, teams_dic))

    # points per game vs. shotefficiency
    stat_entry = _ppg_get(logger, ismobile, teamstat_dic, teams_dic)
    if stat_entry:
        result.append(stat_entry)

    # xg charts
    result.extend(_xgfa_get(logger, ismobile, teamstat_dic, teams_dic))

    # goaliepull effect
    result.extend(_goaliepull_get(logger, ismobile, teamstat_dic, teams_dic))

    # age statistics
    result.extend(_age_statistics_get(logger, ismobile, teamstatdel_dic, teamstatdel_ly_dic, teams_dic))

    # u23 stats
    stat_entry = _u23_toi_stats(logger, ismobile, season_id, teams_dic)
    if stat_entry:
        result.extend(stat_entry)

    return result


def _u23_toi_stats(logger, ismobile, season_id, teams_dic):
    """ prepare u23 stats """
    logger.debug('_u23_stats()')

    stat_entry_list = []
    u23_toi_dic = u23_toi_get(logger, season_id, teams_dic)

    if u23_toi_dic:
        title =  _('U23 players - Average Time on Ice per Match')
        sub_title = _('Date:') + f" {uts_to_date_utc(uts_now(), '%d.%m.%Y')}"
        stat_entry = {
            'title': title,
            'chart': u23_toi_chart(logger, title, sub_title, ismobile, u23_toi_dic.values()),
            'updates': []
        }

        stat_entry_list.append(stat_entry)

    return stat_entry_list

def _age_statistics_get(logger, ismobile, teamstatdel_dic, teamstatdel_ly_dic, teams_dic):
    """ prepare age_statistics """
    logger.debug('_age_statistics_get()')

    stat_entry_list = []

    agedate_dic = age_overview_get(logger, ismobile, teamstatdel_dic, teams_dic)
    league_agedate_dic = league_agestats_get(logger, ismobile, teamstatdel_dic, teams_dic)
    league_agedate_ly_dic = league_agestats_get(logger, ismobile, teamstatdel_ly_dic, teams_dic)

    if agedate_dic:
        title = _('Age group')
        subtitle = _('licensed players per team')

        stat_entry = {
            'title': title,
            'chart':  age_overviewchart_get(logger, title, subtitle, ismobile, agedate_dic['ALL']['data']),
            'updates': []
        }
        stat_entry_list.append(stat_entry)

    if league_agedate_dic or league_agedate_ly_dic:

        title = _('DEL Age Pyramid')
        subtitle = _('Licensed Players in league')

        stat_entry = {
            'title': title,
            'chart':  league_agechart_get(logger, title, subtitle, ismobile, league_agedate_dic, league_agedate_ly_dic),
            'updates': []
        }
        stat_entry_list.append(stat_entry)

    return stat_entry_list

def _goaliepull_get(logger, ismobile, teamstat_dic, teams_dic):
    """ build structure for goaliepull chart """
    logger.debug('_goaliepull_get()')

    goaliep_data = goaliepull_data(logger, ismobile, teamstat_dic, teams_dic)

    stat_entry_list = []

    if goaliep_data:
        pull_en_data = goaliepullendata_get(logger, goaliep_data)
        if pull_en_data:
            # pylint: disable=E0602
            title = _('The Effects of Goalie Pulling')
            subtitle = _('Own goals vs. empty net goals')

            stat_entry = {
                'title': title,
                'chart':  goaliepullchart_get(logger, title, subtitle, ismobile, pull_en_data[len(pull_en_data.keys())]),
                'updates': goaliepullen_updates_get(logger, pull_en_data)
            }
            stat_entry_list.append(stat_entry)
        score_en_data = scoreendata_get(logger, goaliep_data)
        if score_en_data:
            # pylint: disable=E0602
            title = _('Ability to leverage emptynet situations')
            subtitle = _('Empty net situations vs. empty net goals')

            stat_entry = {
                'title': title,
                'chart': scoreenchart_get(logger, title, subtitle, ismobile, score_en_data[len(score_en_data.keys())]),
                'updates': scoreen_updates_get(logger, score_en_data)
            }
            stat_entry_list.append(stat_entry)

    return stat_entry_list

def _ppg_get(logger, ismobile, teamstat_dic, teams_dic):
    """ build structure for pace chart """
    logger.debug('_ppg_get()')

    ppg_data = ppg_data_get(logger, ismobile, teamstat_dic, teams_dic)

    # pylint: disable=E0602
    title = _('Points per Game')
    subtitle = _('Ranking considering match postponements or cancellation')

    if ppg_data:
        stat_entry = {
            'title': title,
            'chart':  ppg_chart_get(logger, title, subtitle, ismobile, ppg_data[len(ppg_data.keys())]),
            'updates': ppg_updates_get(logger, ppg_data, title)
        }
    else:
        stat_entry = {}

    return stat_entry

def _xgfa_get(logger, ismobile, teamstat_dic, teams_dic):
    logger.debug('_xgfa_get()')
    # create empty list returning data
    stat_entry_list = []

    (xgfa_data, gfxgf_data, dgf_data) = xgfa_data_get(logger, ismobile, teamstat_dic, teams_dic)

    if xgfa_data:
        # xgfa chart
        # pylint: disable=E0602
        title = _('Expected Goals For/Against for 5v5')
        subtitle = _('Ability to use and prevent scoring chances')

        stat_entry = {
            'title': title,
            'chart':  xgfa_chart_get(logger, title, subtitle, ismobile, xgfa_data[len(xgfa_data.keys())]),
            'updates': xgfa_updates_get(logger, xgfa_data, _('Headless'), _('Boring'), _('Exciting'), _('Coolly'))
        }
        stat_entry_list.append(stat_entry)

    if dgf_data:
        # xgfa chart
        # pylint: disable=E0602
        title = _('Performance vs. Expectations (dGF%)')
        subtitle = _('Team GF% vs xGF% on 5v5')

        stat_entry = {
            'title': title,
            'chart':  dgf_chart_get(logger, title, subtitle, ismobile, dgf_data[len(dgf_data.keys())]),
            'updates': dgf_updates_get(logger, dgf_data)
        }
        stat_entry_list.append(stat_entry)

    if gfxgf_data:
        # xgfa chart
        # pylint: disable=E0602
        title = _('GF% vs xGF% on 5v5')
        subtitle = _('Who is performing as we would expect')

        stat_entry = {
            'title': title,
            'chart':  gfxgf_chart_get(logger, title, subtitle, ismobile, gfxgf_data[len(gfxgf_data.keys())]),
            'updates': gfxgf_updates_get(logger, gfxgf_data, _('Underperforming'), _('Bad'), _('Good'), _('Overperforming'))
        }
        stat_entry_list.append(stat_entry)

    return stat_entry_list

def _pppk_pctg_get(logger, ismobile, teamstat_dic, teams_dic):
    """ build structure for pppk chart """
    logger.debug('_pppk_pctg_get()')

    # create empty list returning data
    stat_entry_list = []

    (pppk_data, discipline_data) = pppk_data_get(logger, ismobile, teamstat_dic, teams_dic)

    if pppk_data:

        # discipline chart
        # pylint: disable=E0602
        title = _('Penalty Minutes (For/Against)')
        subtitle = _('Average number of Penalty Minutes per game')

        stat_entry = {
            'title': title,
            'chart':  discipline_chart_get(logger, title, subtitle, ismobile, discipline_data[len(discipline_data.keys())]),
            'updates': discipline_updates_get(logger, discipline_data, _('Undisciplined'), _('Friendly'), _('Chippy'), _('Disciplined'))
        }
        stat_entry_list.append(stat_entry)

        # penalty scoring and killing chart
        # pylint: disable=E0602
        title = _('Special team performance')
        subtitle = _('Ability to score / prevent goals')

        stat_entry = {
            'title': title,
            'chart':  pppk_chart_get(logger, title, subtitle, ismobile, pppk_data[len(pppk_data.keys())]),
            'updates': breakdown_updates_get(logger, pppk_data, _('Defensive'), _('Overstrained'), _('Agressive'), _('Offensive'))
        }
        stat_entry_list.append(stat_entry)

    return stat_entry_list

def _teamcomparison_heatmap_get(logger, ismobile, language, teamstat_dic, teams_dic):
    """ build structure for pace chart """
    logger.debug('_teamcomparison_heatmap_get()')

    heatmap_data = teamcomparison_hmdata_get(logger, ismobile, teamstat_dic, teams_dic)

    # team heatmap
    # pylint: disable=E0602
    title = _('Team heatmaps')
    subtitle = _('A league-wide, at-a-glance look on Team performance. Red is bad, blue is good')

    if heatmap_data:
        stat_entry = {
            'title': title,
            'chart':  teamcomparison_chart_get(logger, title, subtitle, ismobile, heatmap_data[len(heatmap_data.keys())]),
            'updates': teamcomparison_updates_get(logger, title, ismobile, heatmap_data),
            'comment': comment_get(logger, 'name', 'teamcomparison_heatmap', [language])
        }
    else:
        stat_entry = {}

    return stat_entry

def _5v5_pace_get(logger, ismobile, teamstat_dic, teams_dic):
    """ build structure for pace chart """
    logger.debug('_5v5_pace_get()')

    # create empty list returning data
    stat_entry_list = []

    # two different data series
    (pace_dic, shotrates_dic, shotshares_dic) = pace_data_get(logger, ismobile, teamstat_dic, teams_dic)

    if pace_dic:
        # 5v5 pace chart
        # pylint: disable=E0602
        title = _('5v5 "Pace" (Cf/60 + Ca/60)')
        subtitle = _('Combined shots on own and other goal during 5-on-5 play (on 60min adjusted)')
        stat_entry = {
            'title': title,
            'chart':  pace_chart_get(logger, title, subtitle, ismobile, pace_dic[len(pace_dic.keys())]),
            'updates': pace_updates_get(logger, pace_dic, title)
        }
        stat_entry_list.append(stat_entry)

    if shotrates_dic:
        # shotrates
        # pylint: disable=E0602
        title = _('5v5 Shot rates Cf/60 vs Ca/60')
        subtitle = _('Shots generated during 5-on-5 play (on 60min adjusted)')
        stat_entry = {
            'title': title,
            'chart':  shotrates_chart_get(logger, title, subtitle, ismobile, shotrates_dic[len(shotrates_dic.keys())]),
            'updates': shotrates_updates_get(logger, shotrates_dic)
        }
        stat_entry_list.append(stat_entry)

        # shotshare
        # pylint: disable=E0602
        title = _('5v5 Shot share C/60')
        subtitle = _('Each team’s share of shots taken in their games')
        stat_entry = {
            'title': title,
            'chart':  shotshare_chart_get(logger, title, subtitle, subtitle, shotshares_dic[len(shotshares_dic.keys())]),
            'updates': pace_updates_get(logger, shotshares_dic, title)
        }
        stat_entry_list.append(stat_entry)

    return stat_entry_list

def _pdo_breakdown_get(logger, ismobile, teamstat_dic, teams_dic):
    """ pdo breakdown """
    logger.debug('_pdo_breakdown_get()')

    # get data for breakdown chart
    breakdown_dic = pdo_breakdown_data_get(logger, ismobile, teamstat_dic, teams_dic)
    # we need the breakdown data as input thus it must run first
    overview_dic = pdo_overview_data_get(logger, ismobile, breakdown_dic)

    stat_entry_list = []

    # pdo overview
    # pylint: disable=E0602
    title = _('PDO overview')
    subtitle = _('5v5 shooting percentage and save percentage')

    if overview_dic:
        stat_entry = {
            'title': title,
            'chart':  pdo_overview_chart(logger, title, subtitle, ismobile, overview_dic[len(overview_dic.keys())]),
            'updates': overview_updates_get(logger, overview_dic),
        }
        stat_entry_list.append(stat_entry)

    if breakdown_dic:
        # pdo breakdown chart
        # pylint: disable=E0602
        title = _('PDO breakdown')
        subtitle = _('luck and fun across the league')
        stat_entry = {
            'title': title,
            'chart':  pdo_breakdown_chart(logger, title, subtitle, ismobile, breakdown_dic[len(breakdown_dic.keys())]),
            'updates': breakdown_updates_get(logger, breakdown_dic, _('Dull'), _('Unlucky'), _('Lucky'), _('Fun'), ismobile),
        }
        stat_entry_list.append(stat_entry)

    return stat_entry_list

def _faceoff_pctg_get(logger, ismobile, teamstat_dic, teams_dic):
    """ faceoff wins """
    logger.debug('_faceoff_pctg_get()')

    faceoff_dic = faceoff_overview_get(logger, ismobile, teamstat_dic, teams_dic)

    if faceoff_dic:
        # pylint: disable=E0602
        title = _('Faceoff win rate')
        stat_entry = {
            'title': title,
            'chart': faceoff_overview_chart(logger, title, ismobile, faceoff_dic[len(faceoff_dic.keys())]),
            'updates': faceoffs_updates_get(logger, title, faceoff_dic)
        }
    else:
        stat_entry = {}

    return stat_entry

def _rebound_pctg_get(logger, ismobile, teamstat_dic, teams_dic):
    """ faceoff wins """
    logger.debug('_rebound_pctg_get()')

    rebound_dic = rebound_overview_get(logger, ismobile, teamstat_dic, teams_dic)

    # pylint: disable=E0602
    title = _('Rebound success rate')
    subtitle = _('Percentage of rebounds leading to a goal')
    if rebound_dic:
        stat_entry = {
            'title': title,
            'chart': rebound_overview_chart(logger, title, subtitle, ismobile, rebound_dic[len(rebound_dic.keys())]),
            'updates': rebound_updates_get(logger, title, rebound_dic, 'goals_rebound_for_pctg', 'goals_rebound_against_pctg'),
        }
    else:
        stat_entry = {}

    return stat_entry

def _break_pctg_get(logger, ismobile, teamstat_dic, teams_dic):
    """ faceoff wins """
    logger.debug('_break_pctg_get()')

    break_dic = break_overview_get(logger, ismobile, teamstat_dic, teams_dic)

    # pylint: disable=E0602
    title = _('Break success rate')
    subtitle = _('Percentage of breaks leading to a goal')
    if break_dic:
        stat_entry = {
            'title': title,
            'chart': break_overview_chart(logger, title, subtitle, ismobile, break_dic[len(break_dic.keys())]),
            'updates': rebound_updates_get(logger, title, break_dic, 'goals_break_for_pctg', 'goals_break_against_pctg'),
        }
    else:
        stat_entry = {}

    return stat_entry
