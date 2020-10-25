# -*- coding: utf-8 -*-
""" common parameters and functions across all charts """

# size
font_size = '10px'
title_font_size = '12px'

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

def credits(text='©2020 GrindSa', href='https://github.com/grindsa/'):
    """ add credits """
    return {'text': text, 'href': href}

def labels():
    """ set labels """
    return {'style': {'fontSize': font_size},}

def exporting():
    """ export structure """
    return {'chartOptions': {'plotOptions': {'series': {'dataLabels': {'enabled': 0 }}}}, 'fallbackToExportServer': 0}

def plotoptions_marker_disable(ele):
    """ plotoptions for spline """
    return {ele: { 'marker': {'enabled': 0}}}

def title(text, _font_size=title_font_size):
    """ set title """
    return {'text': text, 'style': {'color': text_color, 'font-size': _font_size}}

def legend(enabled=1):
    """ create legend structure """
    return {'enabled': enabled, 'useHTML': 1, 'itemStyle': {'color': text_color, 'font-size': font_size}, 'verticalAlign': 'bottom', 'symbolRadius': 0}

def tooltip(tooltip):
    """ customize tooltip """
    return {'shared': 1, 'useHTML': 1, 'headerFormat': tooltip}
