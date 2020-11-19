# -*- coding: utf-8 -*-
""" common parameters and functions across all charts """
# pylint: disable=C0103

# size
font_size = '10px'
font_size_mobile = '8px'
title_font_size = '12px'
title_font_size_mobile = '12px'

# align
legend_valign = 'bottom'
legend_valign_mobile = 'top'

# color definition
text_color = '#404040'
plotlines_color = '#d8d9da'
chart_color1 = '#7cb5ec'
chart_color2 = '#b0b3b5'
chart_color3 = '#030357'
chart_color4 = '#68717a'
chart_color5 = '#e6e6fe'
chart_color6 = '#f1f2f3'
chart_color7 = '#e9f3fc'
chart_color8 = '#000052'
chart_color9 = '#525960'
shot_missed_color = '#d8d9da'
shot_blocked_color = '#000052'
shot_goal_color = '#f01a29'
shot_sog_color = '#7cb5ec'
line_color = '#c00c18'

line1_color = chart_color3
line2_color = chart_color1
line3_color = chart_color4
line4_color = chart_color2
line5_color = chart_color5


def credit(text='©2020 GrindSa (https://hockeygraphs.dynamop.de)', href='https://github.com/grindsa/hockey_graphs'):
    """ add credits """
    return {'text': text, 'href': href}

def labels():
    """ set labels """
    return {'style': {'fontSize': font_size},}

def exporting(_button=None, filename=None, allowhtml=1):
    """ export structure """
    # output_dic = {'chartOptions': {'plotOptions': {'series': {'dataLabels': {'enabled': 0}}}}, 'fallbackToExportServer': 0}
    output_dic = {'fallbackToExportServer': 0, 'allowHTML': allowhtml}
    # output_dic['buttons'] = {'customButton': {'text': button}}
    if filename:
        output_dic['filename'] = filename
    return output_dic

def plotoptions_marker_disable(ele):
    """ plotoptions for spline """
    return {ele: {'marker': {'enabled': 0}}}

def title(text, font_size_=title_font_size):
    """ set title """
    return {'text': text, 'style': {'color': text_color, 'font-size': font_size_}}

def legend(enabled=1, additional_parameters=None):
    """ create legend structure """
    result = {'enabled': enabled, 'useHTML': 1, 'itemStyle': {'color': text_color, 'font-size': font_size}, 'verticalAlign': legend_valign, 'symbolRadius': 0}
    if additional_parameters:
        for key, value in additional_parameters.items():
            result[key] = value
    return result

def responsive_gameflow():
    """ options for responsiveness """
    return {
        'rules': [{
            'condition': {'maxWidth': 500},
            'chartOptions': {
                'xAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                'yAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                'title': {'x': 60, 'y': 40},
                'subtitle': {'x': -10, 'y': 40},
                }
        }]
    }

def responsive_bubble():
    """ options for responsiveness """
    return {
        'rules': [{
            'condition': {'maxWidth': 500},
            'chartOptions': {
                'legend': {'verticalAlign': legend_valign_mobile, 'layout': 'horizontal', 'itemStyle': {'font-size': font_size_mobile}},
                'xAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                'yAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                'plotOptions': {'bubble': {'minSize': 3, 'maxSize': 35}}
                }
        }]
    }

def responsive_y1():
    """ options for responsiveness """
    return {
        'rules': [{
            'condition': {'maxWidth': 500},
            'chartOptions': {
                'legend': {'verticalAlign': legend_valign_mobile, 'layout': 'horizontal', 'itemStyle': {'font-size': font_size_mobile}},
                'xAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                'yAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                # 'exporting': {'enabled': False},
                }
        }]
    }

def responsive_y2():
    """ options for responsiveness """
    return {
        'rules': [{
            'condition': {'maxWidth': 500},
            'chartOptions': {
                'legend': {'verticalAlign': legend_valign_mobile, 'layout': 'horizontal', 'itemStyle': {'font-size': font_size_mobile}},
                'xAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                'yAxis': [
                    {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                    {'title': {'style': {'font-size': font_size_mobile}}, 'opposite': 1, 'labels': {'style': {'fontSize': font_size_mobile}}},
                ],
                # 'exporting': {'enabled': False},
                }
        }]
    }

def tooltip(text):
    """ customize tooltip """
    return {'shared': 1, 'useHTML': 1, 'headerFormat': text, 'marker': {'enabled': 0}}
