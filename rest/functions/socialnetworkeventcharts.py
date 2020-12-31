# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
import textwrap
from rest.functions.chartparameters import chartstyle, credit, exporting, labels, responsive_y1, tooltip, title, subtitle, legend, font_size, plotlines_color, corner_annotations, variables_get, plotoptions_marker_disable
from rest.functions.chartparameters import text_color, chart_color1, chart_color3, chart_color4, chart_color6, twitter_color

def chatterchart_create(logger, ctitle, csubtitle, ismobile, shotsum_dic, events_dic, plotline_list, matchinfo_dic, color_dic):
    """ create chatter chart """
    logger.debug('chatterchart_create()')

    variable_dic = variables_get(ismobile)

    # minute_list = events_dic.keys()
    minute_list = shotsum_dic.keys()

    # max_len
    x_max = len(minute_list)

    data_list = []
    defer = 500
    tick = 500
    alternate = 0
    for min_ in events_dic:
        distance = 20
        for event in events_dic[min_]:
            # wrap text based on amount of events to display
            if len(events_dic[min_]) > 1:
                wrap_len = 30
            else:
                wrap_len = 70
            text_shorten = textwrap.shorten(event['text_raw'], wrap_len)

            data_list.append({'x': min_, 'aname': event['name_alternate'], 'scolor': twitter_color, 'label': text_shorten, 'description': event['text_raw']})

    chart_options = {

        'chart': {
            'type': 'timeline',
            'height': '140%',
            'inverted': 1,
            #'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        #'legend': legend(),
        # 'plotOptions': plotoptions_marker_disable('spline'),

        'tooltip': {
            'useHTML': 1,
            'headerFormat': '',
            'pointFormat': '<span style="color: %s"><b>@{point.aname}</b></span><br>{point.description}' % twitter_color,
            },

        'credits': credit(),
        # 'responsive': responsive_y1(),

        'colors': ['rgba(255, 255, 255, 0.0)'],

        'xAxis': {
            'categories': minute_list,
            'title': {
                'text': _('Game Time'),
                'style': {'color': text_color, 'font-size': font_size},
            },
            'labels': {'style': {'fontSize': font_size}},
            'tickInterval': 5,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'plotLines': [
                {'color': plotlines_color, 'width': 2, 'value': 20},
                {'color': plotlines_color, 'width': 2, 'value': 40},
                {'color': plotlines_color, 'width': 2, 'value': 60}
                ],
            'plotBands': plotline_list,
            'max': x_max,
        },

        'yAxis':{'title': '', 'labels': {'enabled': 0}},

        'series': [{
            'dataLabels': {'connectorWidth': 0, 'backgroundColor': 'rgba(255, 255, 255, 0.1)', 'borderWidth': 0, 'allowOverlap': 1, 'format': '{point.label}'},
            'data': data_list,
        }]
    }

    return chart_options
