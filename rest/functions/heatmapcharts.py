# -*- coding: utf-8 -*-
""" list of functions for heatmaps """
# pylint: disable=E0401
from rest.functions.chartparameters import variables_get, credit, exporting, title, subtitle, color_axis, chartstyle
from rest.functions.chartparameters import font_size, font_size_mobile, text_color, chart_color1

def gamematchupchart_create(logger, ctitle, csubtitle, ismobile, lineup_dic, matchup_matrix, plotline_dic, matchinfo_dic):
    """ create matchup heatmeap """
    # pylint: disable=E0602, R0914
    logger.debug('gamematchupchart_create()')

    variable_dic = variables_get(ismobile)

    data_list = []
    for hpid in matchup_matrix:
        for vpid in matchup_matrix[hpid]:
            # data_list.append([hpid, vpid, round(matchup_matrix[hpid][vpid]/60, 0)])
            tmp_dic = {
                'x': hpid, 'y': vpid,
                'value': round(matchup_matrix[hpid][vpid]['seconds']/60, 3),
                'minsec': '{0:02d}:{1:02d}'.format(*divmod(matchup_matrix[hpid][vpid]['seconds'], 60)),
                'home_name': '{0} {1}'.format(lineup_dic['home_team'][hpid]['name'], lineup_dic['home_team'][hpid]['surname']),
                'visitor_name': '{0} {1}'.format(lineup_dic['visitor_team'][vpid]['name'], lineup_dic['visitor_team'][vpid]['surname']),
                'home_shots': matchup_matrix[hpid][vpid]['home_shots'],
                'visitor_shots': matchup_matrix[hpid][vpid]['visitor_shots'],
            }
            # deside how to set label
            if matchup_matrix[hpid][vpid]['home_shots'] - matchup_matrix[hpid][vpid]['visitor_shots'] > 0:
                # arrow up
                tmp_dic['delta'] = '{0}{1}'.format('\u2BC5', matchup_matrix[hpid][vpid]['home_shots'] - matchup_matrix[hpid][vpid]['visitor_shots'])
                tmp_dic['dataLabels'] = {'format': '{0}{1}'.format('\u2BC5', matchup_matrix[hpid][vpid]['home_shots'] - matchup_matrix[hpid][vpid]['visitor_shots'])}
            elif  matchup_matrix[hpid][vpid]['home_shots'] - matchup_matrix[hpid][vpid]['visitor_shots'] == 0:
                # no arrow
                tmp_dic['delta'] = '{0}'.format(matchup_matrix[hpid][vpid]['home_shots'] - matchup_matrix[hpid][vpid]['visitor_shots'])
                tmp_dic['dataLabels'] = {'format': '{0}'.format(matchup_matrix[hpid][vpid]['home_shots'] - matchup_matrix[hpid][vpid]['visitor_shots'])}
            else:
                # left arrow
                tmp_dic['delta'] = '{0}{1}'.format('\u2BC7', matchup_matrix[hpid][vpid]['visitor_shots'] - matchup_matrix[hpid][vpid]['home_shots'])
                tmp_dic['dataLabels'] = {'format': '{0}{1}'.format('\u2BC7', matchup_matrix[hpid][vpid]['visitor_shots'] - matchup_matrix[hpid][vpid]['home_shots'])}
            data_list.append(tmp_dic)

    x_list = []
    x_list_mobile = []
    for player in lineup_dic['home_team']:
        x_list.append('{0} {1}'.format(lineup_dic['home_team'][player]['name'], lineup_dic['home_team'][player]['surname']))
        x_list_mobile.append('{0}. {1}'.format(lineup_dic['home_team'][player]['name'][0], lineup_dic['home_team'][player]['surname']))


    y_list = []
    y_list_mobile = []
    for player in lineup_dic['visitor_team']:
        y_list.append('{0} {1}'.format(lineup_dic['visitor_team'][player]['name'], lineup_dic['visitor_team'][player]['surname']))
        y_list_mobile.append('{0}. {1}'.format(lineup_dic['visitor_team'][player]['name'][0], lineup_dic['visitor_team'][player]['surname']))

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
            'height': variable_dic['shotmap_height_pctg'],
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle, allowhtml=0),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),

        'tooltip': {
            'useHTML': 0,
            'headerFormat': None,
            'pointFormat': '<span><b>{point.home_name} vs, {point.visitor_name}</b></span><br/> <span style="font-size: %(fontsize)s"> {series.name}: {point.minsec} %(min)s</span><br /><span style="font-size: %(fontsize)s"><b>%(headline)s:</b><br /><span style="font-size: %(fontsize)s"> %(homeshots)s: {point.home_shots}</span><br/> <span style="font-size: %(fontsize)s"> %(visitorshots)s: {point.visitor_shots}</span><br/><span style="font-size: %(fontsize)s"> delta: {point.delta}<br />' % {'fontsize': font_size, 'min': 'min', 'headline': _('Shots while players on Ice'), 'homeshots': matchinfo_dic['home_team__shortcut'], 'visitorshots': matchinfo_dic['visitor_team__shortcut']},
        },

        'xAxis': {
            'categories': x_list,
            'opposite':1,
            'plotLines': x_plotlines,
            'labels': {'step': 1, 'rotation': -45}
        },

        'yAxis': {
            'categories': y_list,
            'title': '',
            'reversed': True,
            'plotLines': y_plotlines,
            'labels': {'step': 1}
        },

        'legend': {
            'title': title(_('Time on Ice'), font_size),
            'align': 'center',
            'layout': 'horizontal',
            'verticalAlign': 'bottom',
            'useHTML': 1,
            'itemStyle': {'color': text_color, 'font-size': font_size},
        },

        'colorAxis': {
            'min': 0,
            'minColor': '#FFFFFF',
            'maxColor': chart_color1,
        },

        'series': [{
            'name': _('Time on Ice'),
            'borderWidth': 1,
            'data': data_list,
            'dataLabels': {
                'enabled': 1,
                'useHTML': 0,
                # 'color': text_color,
                'style': {'fontSize': '8px', 'textOutline': 0, 'color': text_color}
            }
        }],

        'responsive': {
            'rules': [{
                'condition': {'maxWidth': 500},
                'chartOptions': {
                    'xAxis': {'categories': x_list_mobile, 'labels': {'style': {'fontSize': font_size_mobile}}},
                    'yAxis': {'categories': y_list_mobile, 'labels': {'style': {'fontSize': font_size_mobile}}},
                }
            }]
        }
    }
    return chart_options

def teamcomparison_chart_get(logger, ctitle, csubtitle, ismobile, data_dic):
    """ team comparison heatmap chart """
    logger.debug('teamcomparison_chart_get()')

    variable_dic = variables_get(ismobile)

    chart_options = {

        'chart': {
            'type': 'heatmap',
            'height': '110%',
            'inverted': 1,
            'style': chartstyle()
        },

        'exporting': exporting(filename=ctitle, allowhtml=0),
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),

        'xAxis': {
            'categories': data_dic['x_category'],
            'type': 'category',
            'labels': {'useHTML': 1, 'align': 'center'}
        },

        'yAxis': {
            'categories': data_dic['y_category'],
            'title': '',
            'opposite':1,
        },

        'tooltip': {
            'headerFormat': '',
            'pointFormat': '<b>{point.y_name}</b>: {point.ovalue}',
            'split': 1,
        },

        'legend': {
            'align': 'center',
            'layout': 'horizontal',
            'verticalAlign': 'bottom',
            'useHTML': 0,
            'itemStyle': {'color': text_color, 'font-size': font_size},
        },

        'colorAxis': color_axis(showinlegend=0),

        'series': [{
            'marker': {'symbol': 'square'},
            'borderWidth': variable_dic['border_width'],
            'borderColor': '#ffffff',
            'data': data_dic['data'],
            'showInLegend': 0,
            'dataLabels': {'enabled': 0}
        }],
    }

    return chart_options
