# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_y1, title, subtitle, legend, font_size, variables_get
from rest.functions.chartparameters import chart_color1, chart_color2, chart_color3, chart_color4

def gametoichart_create(logger, ctitle, csubtitle, ismobile, toi_dic):
    # pylint: disable=E0602
    """ create time-on-ice chart """
    logger.debug('gametoichart_create()')

    variable_dic = variables_get(ismobile)

    # create x axis with player names
    x_list = []
    y_dic = {1: [], 2: [], 3: [], 4: []}

    # we need two iterations of the dictionary
    # first one is to create the list of playernames
    for period in toi_dic:
        for player_name in toi_dic[period]:
            if player_name not in x_list:
                x_list.append(player_name)

    # 2nd one to add toi per player
    for period in toi_dic:
        for player_name in sorted(x_list):
            if player_name in toi_dic[period]:
                # y_dic[period].append('{0:02d}:{1:02d}'.format(*divmod(shifts_dic['ebb'][period][player_name], 60)))
                y_dic[period].append({'y': round(toi_dic[period][player_name]/60, 3), 'label': '{0:02d}:{1:02d}'.format(*divmod(toi_dic[period][player_name], 60))})
            else:
                y_dic[period].append(0)

    chart_options = {

        'chart': {
            'type': 'bar',
            'height': '120%',
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        'responsive': responsive_y1(),

        'plotOptions': {'series': {'stacking': 'normal'}},

        'tooltip': {
            'shared': 1,
            'useHTML': 1,
            'headerFormat': '<span style="font-size: %s"><b>{point.x}</b></span><br/>' % font_size,
            'pointFormat': '<span style="color:{point.color}">\u25CF</span> <span style="font-size: %s">{series.name}: {point.label} %s</span><br/>' % (font_size, _('min'))
        },

        'xAxis': {
            'categories': sorted(x_list),
            'title': title('', font_size),
            'labels': {'style': {'fontSize': font_size},},
            'tickInterval': 1,
            'showFirstLabel': 1,
            'showLastLabel': 1,
        },

        'yAxis': {
            'title': title(_('Time on Ice'), font_size),
            'reversedStacks': 0,
            'tickInterval': 1,
            'maxPadding': 0.1,
            'labels': {'style': {'fontSize': font_size},},
        },

        'series': [
            {'name': _('1st Period'), 'data': y_dic[1], 'color': chart_color3},
            {'name': _('2nd Period'), 'data': y_dic[2], 'color': chart_color1},
            {'name': _('3rd Period'), 'data': y_dic[3], 'color': chart_color2},
            {'name': _('OT'), 'data': y_dic[4], 'color': chart_color4}
        ]
    }
    return chart_options

def gametoipppkchart_create(logger, ctitle, csubtitle, ismobile, toi_dic):
    # pylint: disable=E0602
    """ create time-on-ice chart """
    logger.debug('gametoichart_create()')

    variable_dic = variables_get(ismobile)

    # create x axis with player names
    x_list = []
    pp_list = []
    pk_list = []

    # we need two iterations of the dictionary
    # first one is to create the list of playernames

    for player_name in toi_dic:
        if player_name not in x_list:
            x_list.append(player_name)

    # 2nd one to add toi per player
    for player_name in sorted(x_list):
        if player_name in toi_dic:
            # y_dic[period].append('{0:02d}:{1:02d}'.format(*divmod(shifts_dic['ebb'][period][player_name], 60)))
            pp_list.append({'y': round(toi_dic[player_name]['pp']/60, 3), 'label': '{0:02d}:{1:02d}'.format(*divmod(toi_dic[player_name]['pp'], 60))})
            pk_list.append({'y': round(toi_dic[player_name]['pk']/60, 3), 'label': '{0:02d}:{1:02d}'.format(*divmod(toi_dic[player_name]['pk'], 60))})
        else:
            pp_list.append(0)
            pk_list.append(0)

    chart_options = {

        'chart': {
            'type': 'bar',
            'height': '100%',
            'alignTicks': 0,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        'responsive': responsive_y1(),

        'tooltip': {
            'shared': 1,
            'useHTML': 1,
            'headerFormat': '<span style="font-size: %s"><b>{point.x}</b></span><br/>' % font_size,
            'pointFormat': '<span style="color:{point.color}">\u25CF</span> <span style="font-size: %s">{series.name}: {point.label} %s</span><br/>' % (font_size, _('min'))
        },

        'xAxis': {
            'categories': sorted(x_list),
            'title': title('', font_size),
            'labels': {'style': {'fontSize': font_size},},
            'tickInterval': 1,
            'showFirstLabel': 1,
            'showLastLabel': 1,
        },

        'yAxis': {
            'title': title(_('Time on Ice'), font_size),
            'reversedStacks': 0,
            'tickInterval': 1,
            'maxPadding': 0.1,
            'labels': {'style': {'fontSize': font_size},},
        },

        'series': [
            {'name': _('Time in Powerplay'), 'data': pp_list, 'color': chart_color3},
            {'name': _('Time in Penalty killing'), 'data': pk_list, 'color': chart_color2},
        ]
    }
    return chart_options
