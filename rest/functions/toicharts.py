# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
from rest.functions.chartparameters import credit, exporting, responsive_y1, title, legend, font_size
from rest.functions.chartparameters import chart_color1, chart_color2, chart_color3, chart_color4, text_color

def gametoichart_create(logger, toi_dic):
    # pylint: disable=E0602
    """ create time-on-ice chart """
    logger.debug('gametoichart_create()')

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
        },

        'exporting': exporting(),
        'title': title(''),
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

def gamematchupchart_create(logger, lineup_dic, matchup_matrix, plotline_dic):
    """ create matchup heatmeap """
    logger.debug('gamematchupchart_create()')


    data_list = []
    for hpid in matchup_matrix:
        for vpid in matchup_matrix[hpid]:
            # data_list.append([hpid, vpid, round(matchup_matrix[hpid][vpid]/60, 0)])
            data_list.append({
                'x': hpid, 'y': vpid, 'value': round(matchup_matrix[hpid][vpid]['seconds']/60, 3),
                'minsec': '{0:02d}:{1:02d}'.format(*divmod(matchup_matrix[hpid][vpid]['seconds'], 60)),
                'home_name': '{0} {1}'.format(lineup_dic['home_team'][hpid]['name'], lineup_dic['home_team'][hpid]['surname']),
                'visitor_name': '{0} {1}'.format(lineup_dic['visitor_team'][vpid]['name'], lineup_dic['visitor_team'][vpid]['surname']),
                'dataLabels': {'format': '{0}:{1:02d}'.format(*divmod(matchup_matrix[hpid][vpid]['seconds'], 60))}
            })

    x_list = []
    for player in lineup_dic['home_team']:
        x_list.append('{0} {1}'.format(lineup_dic['home_team'][player]['name'], lineup_dic['home_team'][player]['surname']))

    y_list = []
    for player in lineup_dic['visitor_team']:
        y_list.append('{0} {1}'.format(lineup_dic['visitor_team'][player]['name'], lineup_dic['visitor_team'][player]['surname']))

    # x_plotlines
    x_plotlines = []
    for plot in plotline_dic['home_team']:
        x_plotlines.append({'color': '#ffffff', 'width': 4, 'value': plot - .5, 'zIndex': 4})

    # y_plotlines
    y_plotlines = []
    for plot in plotline_dic['visitor_team']:
        y_plotlines.append({'color': '#ffffff', 'width': 4, 'value': plot - .5, 'zIndex': 4})

    chart_options = {

        'chart': {
            'type': 'heatmap',
            'height': '90%',
        },

        'exporting': exporting(),
        'title': title(''),
        'credits': credit(),

        'tooltip': {
            'useHTML': 0,
            'headerFormat': None,
            'pointFormat': '<span><b>{point.home_name} vs, {point.visitor_name}</b></span><br><span style="color:{point.color}">\u25CF</span> <span style="font-size: %s"> {series.name}: {point.minsec} %s</span><br/>' % (font_size, _('min')),
        },

        'xAxis': {
            'categories': x_list,
            'opposite':1,
            'plotLines': x_plotlines,
        },

        'yAxis': {
            'categories': y_list,
            'title': '',
            'reversed': True,
            'plotLines': y_plotlines,
        },

        'colorAxis': {
            'min': 0,
            'minColor': '#FFFFFF',
            'maxColor': chart_color1
        },

        'legend': {
            'align': 'right',
            'layout': 'vertical',
            'margin': 0,
            'verticalAlign': 'middle',
            'y': 25,
            'symbolHeight': 280
        },

        'series': [{
            'name': 'Eiszeit',
            'borderWidth': 1,
            'data': data_list,
            'dataLabels': {
                'enabled': 1,
                'useHTML': 0,
                # 'color': text_color,
                'style': {'fontSize': '8px', 'textOutline': 0, 'color': text_color}
            }
        }],
    }
    return chart_options
