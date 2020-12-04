# -*- coding: utf-8 -*-
""" list of functions for heatmaps """
import math
# pylint: disable=E0401
from rest.functions.chartparameters import credit, exporting, responsive_gameflow, responsive_y1, responsive_y1_label, responsive_y2, responsive_bubble, plotoptions_marker_disable, title, legend, tooltip, labels, font_size, font_size_mobile, legend_valign_mobile, corner_annotations
from rest.functions.chartparameters import text_color, plotlines_color, chart_color1, chart_color2, chart_color3, chart_color4, chart_color5, chart_color6, chart_color8, chart_color9, shot_missed_color, shot_blocked_color, shot_goal_color, shot_sog_color, line_color, line1_color, line2_color, line3_color, line4_color, line5_color


def teamcomparison_chart_get(logger, ctitle, data_dic):

    chart_options = {

        'chart': {
            'type': 'heatmap',
            'height': '90%',
            'inverted': 1,
        },

        'exporting': exporting(filename=ctitle, allowhtml=0),
        'title': title(''),
        'credits': credit(),


        'xAxis': {
            'categories': data_dic['x_category'],
        },

        'yAxis': {
            'categories': data_dic['y_category'],
            'title': '',
            'opposite':1,
        },

        'colorAxis': {
            'min': 0,
            'minColor': '#FF0000',
            'maxColor': chart_color1,
        },

        'series': [{
            'name': _('Time on Ice'),
            'borderWidth': 1,
            'data': data_dic['data'],
            'dataLabels': {
                'enabled': 1,
                'useHTML': 0,
                # 'color': text_color,
                'style': {'fontSize': '8px', 'textOutline': 0, 'color': text_color}
            }
        }],


    }

    return chart_options
