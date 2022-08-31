# -*- coding: utf-8 -*-
""" common parameters and functions across all charts """
# pylint: disable=C0103
import math

# size
font_size = '10px'
font_size_mobile = '8px'
title_font_size = '18px'
subtitle_font_size = '14px'
title_font_size_mobile = '14px'
subtitle_font_size_mobile = '12px'

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
shot_posthit_color = '#68717a'
line_color = '#c00c18'

line1_color = chart_color3
line2_color = chart_color1
line3_color = chart_color4
line4_color = chart_color2
line5_color = chart_color5

# hm_color_list = ['#a90c38', '#c11b39', '#e54444', '#ec4f4a', '#e06f5b', '#f98973', '#fa8e78', '#fc9783', '#eac7bf', '#b2cfe2', '#a4cbe5', '#8bb8db', '#70a2c9', '#43719f', '#416f9d', '#2e5b87']
hm_color_list = ['#a90c38', '#c11b39', '#e54444', '#ec4f4a', '#e06f5b', '#f98973', '#fa8e78', '#b2cfe2', '#a4cbe5', '#8bb8db', '#70a2c9', '#43719f', '#416f9d', '#2e5b87', '#2e5b87']

twitter_color = '#1DA1F2'

def credit(text='©2022 GrindSa (https://hockeygraphs.dynamop.de)', href='https://hockeygraphs.dynamop.de'):
    """ add credits """
    return {'text': text, 'href': href}

def labels():
    """ set labels """
    return {'style': {'fontSize': font_size},}

def exporting(_button=None, filename=None, allowhtml=1, sourcewidth=0, sourceheight=0):
    """ export structure """
    # output_dic = {'chartOptions': {'plotOptions': {'series': {'dataLabels': {'enabled': 0}}}}, 'fallbackToExportServer': 0}
    output_dic = {'fallbackToExportServer': 0, 'allowHTML': allowhtml}
    # output_dic['buttons'] = {'customButton': {'text': button}}
    if filename:
        output_dic['filename'] = filename

    if sourcewidth and sourceheight:
        output_dic['sourceWidth'] = sourcewidth
        output_dic['sourceHeight'] = sourceheight

    return output_dic

def plotoptions_marker_disable(ele):
    """ plotoptions for spline """
    return {ele: {'marker': {'enabled': 0}}}
    # return {ele: {'marker': {'enabled': 0}, 'fillOpacity': 0.9}}

def title(text, font_size_=title_font_size, decoration=False, margin=None, align=None, offset=None):
    """ set title """
    result = {'text': text, 'style': {'color': text_color, 'font-size': font_size_}}

    if decoration:
        result['style']['fontWeight'] = 'bold'
        result['style']['textDecoration'] = 'underline'

    if margin:
        result['margin'] = margin

    if align:
        result['align'] = align

    if offset:
        result['offset'] = offset

    return result

def subtitle(text, font_size_=subtitle_font_size):
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

def responsive_y1_nolabel():
    """ options for responsiveness """
    return {
        'rules': [{
            'condition': {'maxWidth': 500},
            'chartOptions': {
                'legend': {'verticalAlign': legend_valign_mobile, 'layout': 'horizontal', 'itemStyle': {'font-size': font_size_mobile}},
                'xAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                #'xAxis': {'title': {'style': {'font-size': font_size_mobile}, 'text': 'foo'}, 'labels': {'style': {'fontSize': font_size_mobile}}},
                'yAxis': {'title': {'style': {'font-size': font_size_mobile}}, 'labels': {'enabled': 0, 'style': {'fontSize': font_size_mobile}}},
                'plotOptions': {'series': {'dataLabels': {'style': {'fontSize': font_size_mobile}}}},
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

def gameflow_annotations(ismobile, y_max, home_logo, visitor_logo):
    """ annotations in all four corners """

    # we need to calulcate the y position of the logos dynamically
    y_bar_max = math.ceil(y_max/100) * 100

    # flip by 90 - thus it looks strange
    if ismobile:
        left = {'x':5, 'y': round(-0.75 * y_bar_max, 0), 'xAxis': 0, 'yAxis': 0}
        right = {'x': 5, 'y': round(0.53 * y_bar_max, 0), 'xAxis': 0, 'yAxis': 0}
        img_width = 35
    else:
        img_width = 55
        left = {'x': 5, 'y': round(-0.75 * y_bar_max, 0), 'xAxis': 0, 'yAxis': 0}
        right = {'x': 5, 'y': round(0.6 * y_bar_max, 0), 'xAxis': 0, 'yAxis': 0}

    img_height = img_width
    result = [{
        'shapes': [
            {'type': 'image', 'src': home_logo, 'width': img_width, 'height': img_height, 'point': left},
            {'type': 'image', 'src': visitor_logo, 'width': img_width, 'height': img_height, 'point': right}
        ]
    }]
    return result

def puckpossession_annotations(ismobile, x_bar_max, home_logo, visitor_logo):
    """ puckpossession_annotations in all four corners """

    if ismobile:
        img_width = 35
        home = {'x': round(0.85 * x_bar_max, 0), 'y': 25, 'xAxis': 0, 'yAxis': 0}
        visitor = {'x': round(0.85 * x_bar_max, 0), 'y': 95, 'xAxis': 0, 'yAxis': 0}
    else:
        img_width = 55
        home = {'x': round(0.9 * x_bar_max, 0), 'y': 15, 'xAxis': 0, 'yAxis': 0}
        visitor = {'x': round(0.9 * x_bar_max, 0), 'y': 95, 'xAxis': 0, 'yAxis': 0}

    img_height = img_width

    result = [{
        'shapes': [
            {'type': 'image', 'src': home_logo, 'width': img_width, 'height': img_height, 'point': home},
            {'type': 'image', 'src': visitor_logo, 'width': img_width, 'height': img_height, 'point': visitor}
        ]
    }]
    return result

def _corner_magic(minmax_dic, pctg=4):
    """ do some magic to position the points """

    # points will be positioned relative to axis min/max
    x_diff = minmax_dic['x_max'] - minmax_dic['x_min']
    y_diff = minmax_dic['y_max'] - minmax_dic['y_min']
    factor = pctg # we are moving each annotation by four percent from axis

    x_min = minmax_dic['x_min'] + x_diff * factor/100
    x_max = minmax_dic['x_max'] - x_diff * factor/100
    y_min = minmax_dic['y_min'] + y_diff * factor/100
    y_max = minmax_dic['y_max'] - y_diff * factor/100

    return (x_min, x_max, y_min, y_max)

def corner_annotations(_ismobile, minmax_dic, upper_left_text, lower_left_text, upper_right_text, lower_right_text, pctg=4):
    """ annotations in all four corners """

    (x_min, x_max, y_min, y_max) = _corner_magic(minmax_dic, pctg)

    upper_left = {'x': x_min, 'y': y_max, 'xAxis': 0, 'yAxis': 0}
    upper_right = {'x': x_max, 'y': y_max, 'xAxis': 0, 'yAxis': 0}
    lower_left = {'x': x_min, 'y': y_min, 'xAxis': 0, 'yAxis': 0}
    lower_right = {'x': x_max, 'y': y_min, 'xAxis': 0, 'yAxis': 0}

    result = [{
        'labelOptions': {'x': 0, 'y': 10},
        'labels': [
            {'style': {'fontSize': font_size}, 'backgroundColor': 'rgba(255, 255, 255, 0)', 'borderColor': 'white', 'point': upper_left, 'text': upper_left_text},
            {'style': {'fontSize': font_size}, 'backgroundColor': 'rgba(255, 255, 255, 0)', 'borderColor': 'white', 'point': lower_left, 'text': lower_left_text},
            {'style': {'fontSize': font_size}, 'backgroundColor': 'rgba(255, 255, 255, 0)', 'borderColor': 'white', 'point': upper_right, 'text': upper_right_text},
            {'style': {'fontSize': font_size}, 'backgroundColor': 'rgba(255, 255, 255, 0)', 'borderColor': 'white', 'point': lower_right, 'text': lower_right_text},
        ],
        'zIndex': 1
    }]

    return result

def color_axis(color_list=None, showinlegend=1, minimum=0):
    """ create color scheme for heatmap """
    if not color_list:
        color_list = hm_color_list

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
        'min': minimum,
        'stops': stop_list,
        'showInLegend': showinlegend,
    }

    return result

def chart_colors_get(logger, matchinfo_dic):
    """ get colors for chart """
    color_dic = {
        'home_team_color': chart_color1,
        'home_team_color_primary': chart_color1,
        'visitor_team_color': chart_color2,
        'visitor_team_color_secondary': chart_color2,
        'home_team_color_penalty': chart_color7,
        'visitor_team_color_penalty': chart_color6,
        'home_team_color_penalty_primary': chart_color7,
        'visitor_team_color_penalty_secondary': chart_color6
        }

    # set primary colors
    if 'home_team__color_primary' in matchinfo_dic and bool(matchinfo_dic['home_team__color_primary']):
        color_dic['home_team_color'] = matchinfo_dic['home_team__color_primary']
        color_dic['home_team_color_primary'] = matchinfo_dic['home_team__color_primary']
    if 'visitor_team__color_primary' in matchinfo_dic and bool(matchinfo_dic['visitor_team__color_primary']):
        color_dic['visitor_team_color'] = matchinfo_dic['visitor_team__color_primary']
        color_dic['visitor_team_color_primary'] = matchinfo_dic['visitor_team__color_primary']
    if 'home_team__color_penalty_primary' in matchinfo_dic and bool(matchinfo_dic['home_team__color_penalty_primary']):
        color_dic['home_team_color_penalty'] = matchinfo_dic['home_team__color_penalty_primary']
        color_dic['home_team_color_penalty_primary'] = matchinfo_dic['home_team__color_penalty_primary']
    if 'visitor_team__color_penalty_primary' in matchinfo_dic and bool(matchinfo_dic['visitor_team__color_penalty_primary']):
        color_dic['visitor_team_color_penalty'] = matchinfo_dic['visitor_team__color_penalty_primary']
        color_dic['visitor_team_color_penalty_primary'] = matchinfo_dic['visitor_team__color_penalty_primary']

    # set seconday colors
    if 'home_team__color_secondary' in matchinfo_dic and bool(matchinfo_dic['home_team__color_secondary']):
        color_dic['home_team_color_secondary'] = matchinfo_dic['home_team__color_secondary']
    if 'visitor_team__color_secondary' in matchinfo_dic and bool(matchinfo_dic['visitor_team__color_secondary']):
        color_dic['visitor_team_color_secondary'] = matchinfo_dic['visitor_team__color_secondary']
    if 'home_team__color_penalty_secondary' in matchinfo_dic and bool(matchinfo_dic['home_team__color_penalty_secondary']):
        color_dic['home_team_color_penalty_secondary'] = matchinfo_dic['home_team__color_penalty_secondary']
    if 'visitor_team__color_penalty_secondary' in matchinfo_dic and bool(matchinfo_dic['visitor_team__color_penalty_secondary']):
        color_dic['visitor_team_color_penalty_secondary'] = matchinfo_dic['visitor_team__color_penalty_secondary']

    # cornercase handling switchcolor for visitor team to primary colors
    if color_dic['home_team_color_primary'] == color_dic['visitor_team_color_secondary'] or color_dic['home_team_color_penalty_primary'] == color_dic['visitor_team_color_penalty_secondary']:
        logger.debug('flip to primary color for visitor team')
        color_dic['visitor_team_color'] = matchinfo_dic['visitor_team__color_primary']
        color_dic['visitor_team_color_penalty'] = matchinfo_dic['visitor_team__color_penalty_primary']
        color_dic['visitor_team_color_penalty_secondary'] = matchinfo_dic['visitor_team__color_penalty_primary']
        color_dic['visitor_team_color_secondary'] = matchinfo_dic['visitor_team__color_primary']

    # corner case handling if either colors are similar - in this case switch to backup color
    elif color_dic['home_team_color'] == color_dic['visitor_team_color'] or color_dic['home_team_color_penalty'] == color_dic['visitor_team_color_penalty']:
        logger.debug('flip to secondary color for visitor team')
        if 'visitor_team__color_secondary' in matchinfo_dic and bool(matchinfo_dic['visitor_team__color_secondary']):
            color_dic['visitor_team_color'] = matchinfo_dic['visitor_team__color_secondary']
            color_dic['visitor_team_color_penalty'] = matchinfo_dic['visitor_team__color_penalty_secondary']
        else:
            color_dic['visitor_team_color'] = chart_color2
            color_dic['visitor_team_color_penalty'] = chart_color6

    return color_dic

def variables_get(ismobile):
    """ build variables based on mobile detection """
    if ismobile:
        data_dic = {'export_sourcewidth': 373, 'export_sourceheight': 298, 'linewidth': 2, 'title_margin': 40, 'timeline_distance': 25, 'ticker_startval': 20, 'ticker_multiplier': 5, 'timeline_font_size': font_size, 'timeline_wrap_length': 40, 'border_width': 5, 'title_size': title_font_size_mobile, 'subtitle_size': subtitle_font_size_mobile, 'font_size': font_size_mobile, 'label_size': font_size_mobile, 'shotmap_height_pctg': '130%', 'shotzone_height_pctg': '85%'}
    else:
        data_dic = {'export_sourcewidth': 800, 'export_sourceheight': 600, 'linewidth': 3, 'title_margin': 50, 'timeline_distance': 50, 'ticker_startval': 15, 'ticker_multiplier': 3.42, 'timeline_font_size': '12px', 'timeline_wrap_length': 90, 'border_width': 10, 'title_size': title_font_size, 'subtitle_size': subtitle_font_size, 'font_size': font_size, 'label_size': font_size, 'shotmap_height_pctg': '110%', 'shotzone_height_pctg': '80%'}

    return data_dic

def chartstyle():
    """ return chartstyle """
    return {'fontFamily': 'verdana, helvetica, arial, sans-serif'}

def shotzonelabel(text, size=font_size):
    """ get shotzone marker """
    return {'enabled': 1, 'color': '#ffffff', 'style': {'textShadow': 0, 'textOutline': 0, 'fontSize': size}, 'y': 11, 'format': '{0}%'.format(text), 'align': 'center'}
