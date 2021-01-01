# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401, R0914
import textwrap
from rest.functions.chartparameters import chartstyle, credit, exporting, title, subtitle, variables_get, chart_color3, chart_color6, twitter_color
from rest.functions.helper import date_to_uts_utc, uts_to_date_utc

def chatterchart_create(logger, ctitle, csubtitle, ismobile, events_dic, plotband_list):
    """ create chatter chart """
    logger.debug('chatterchart_create()')

    variable_dic = variables_get(ismobile)


    data_list = []
    x_list = []

    cnt = 0
    for _uts, event in sorted(events_dic.items()):

        # we need to count the amount of tweets to calculate the chartsize
        cnt += 1

        # on the fly timestamp for x-axis
        timestamp = uts_to_date_utc(date_to_uts_utc(event['created_at']), '%H:%M')

        if 'text_raw' in event:
            # this is a regular event
            text_shorten = textwrap.shorten(event['text_raw'], variable_dic['timeline_wrap_length'])
            data_list.append({'x': cnt, 'name': timestamp, 'aname': '@{0}'.format(event['name_alternate']), 'scolor': twitter_color, 'label': text_shorten, 'description': event['text_raw'], 'dataLabels': {'style': {'fontSize': variable_dic['timeline_font_size']}}})
        else:
            # this is a goal
            data_list.append({'x': cnt, 'name': timestamp, 'aname': '#bot1337', 'scolor': chart_color3, 'color': event['color'], 'label': event['name_alternate'], 'dataLabels': {'color': event['color'], 'style': {'fontSize': variable_dic['timeline_font_size'], 'fontWeight': 'bold'}}})

        x_list.append({'x': cnt, 'name': timestamp})

    # charthight depends on number of tweets - need to be calculated
    chart_height = variable_dic['ticker_startval'] + (cnt * variable_dic['ticker_multiplier'])

    chart_options = {

        'chart': {
            'type': 'timeline',
            'height': '{0}%'.format(chart_height),
            'inverted': 1,
            'zoomType': 'x',
            #'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),

        'plotOptions': {'timeline': {'dataLabels': {'align': 'left', 'distance': variable_dic['timeline_distance'], 'alternate': 0}}},

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '',
            'pointFormat': '<span style="color: {point.scolor}"><b>{point.aname}</b></span><br>{point.description}',
        },

        'xAxis': {
            'categories': x_list,
            'visible': 1,
            'tickWidth': 0,
            'tickInterval': 3,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'lineWidth': 0,
            'labels': {
                'enabled': 1,
                'style': {'fontSize': variable_dic['timeline_font_size']}
            },
            'plotBands': plotband_list,
        },

        'yAxis': {
            'gridLineWidth': 3,
            'title': '',
            'startOnTick': 0,
            'endOnTick': 0,
            'labels': {'enabled': 0},
            'width': 50
        },

        'colors': [chart_color6],
        'series': [{
            'dataLabels': {'allowOverlap': 1, 'format': '{point.label}', 'borderWidth': 0}, 'data': data_list
        }]
    }
    return chart_options
