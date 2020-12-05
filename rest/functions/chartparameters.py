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
legend_valign_mobile = 'bottom'

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


def responsive_y1_label():
    """ options for responsiveness """
    return {
        'rules': [{
            'condition': {'maxWidth': 500},
            'chartOptions': {
                'legend': {'verticalAlign': legend_valign_mobile, 'layout': 'horizontal', 'itemStyle': {'font-size': font_size_mobile}},
                'xAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                'yAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                'plotOptions': {'series': {'dataLabels': {'enabled': 1, 'style': {'fontSize': font_size_mobile}}}},
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


def corner_annotations(ismobile, upper_left_text, lower_left_text, upper_right_text, lower_right_text):
    """ annotations in all four corners """

    if ismobile:
        upper_left = {'x': 25, 'y': 55}
        upper_right = {'x': 340, 'y': 55}
        lower_left = {'x': 25, 'y': 310}
        lower_right = {'x': 340, 'y': 310}
    else:
        upper_left = {'x': 25, 'y': 55}
        upper_right = {'x': 750, 'y': 55}
        lower_left = {'x': 25, 'y': 700}
        lower_right = {'x': 750, 'y': 700}

    result = [{
        'labels': [
            {'style': {'fontSize': font_size}, 'backgroundColor': 'white', 'borderColor': 'white', 'point': upper_left, 'text': upper_left_text},
            {'style': {'fontSize': font_size}, 'backgroundColor': 'white', 'borderColor': 'white', 'point': lower_left, 'text': lower_left_text},
            {'style': {'fontSize': font_size}, 'backgroundColor': 'white', 'borderColor': 'white', 'point': upper_right, 'text': upper_right_text},
            {'style': {'fontSize': font_size}, 'backgroundColor': 'white', 'borderColor': 'white', 'point': lower_right, 'text': lower_right_text},
        ],
        'zIndex': 1
    }]

    return result


def color_axis(color_list=None):
    """ create color scheme for heatmap """

    if not color_list:
        color_list = ['#a90c38', '#c11b39', '#e54444', '#ec4f4a', '#e06f5b', '#f98973', '#fa8e78', '#fc9783', '#eac7bf', '#b2cfe2', '#a4cbe5', '#8bb8db', '#70a2c9', '#43719f', '#416f9d', '#2e5b87']

    stop_list = []
    quotient = round(100/ (len(color_list)-1), 0)

    # add first color for start
    stop_list.append([0, color_list[0]])

    # distribute colors equally
    for ele in range(1, len(color_list)-1):
        stop_list.append([ele * quotient/100, color_list[ele]])

    # add last color for end
    stop_list.append([1, color_list[-1]])


    result = {
        'min': 0,
        'stops': stop_list,
    }

    return result
