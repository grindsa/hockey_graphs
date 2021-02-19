# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
import math
from rest.functions.chartparameters import chartstyle, credit, exporting, title, subtitle, legend, font_size, variables_get, plotlines_color

def shiftsperplayerchart_create(logger, ctitle, csubtitle, ismobile, shift_dic, goal_dic, color1, color2, color3):
    # pylint: disable=E0602, R0914
    """ create shift per player chart """
    logger.debug('shiftsperplayerchart_create()')

    variable_dic = variables_get(ismobile)

    playername_list = []
    data_list = []
    data_list_pp = []
    data_list_pk = []

    tst_end = 3600

    line_number = 1
    y_plotlines = []

    for idx, player_id in enumerate(sorted(shift_dic, key=lambda i: (shift_dic[i]['line_number'], -shift_dic[i]['role'], shift_dic[i]['position']))):
        # add playername to x_list
        player_string = '{0} ({1})'.format(shift_dic[player_id]['name'], shift_dic[player_id]['jersey'])
        playername_list.append(player_string)

        # add plotline in case the line-number changes
        if shift_dic[player_id]['line_number'] != line_number:
            line_number = shift_dic[player_id]['line_number']
            y_plotlines.append({'color': plotlines_color, 'width': 2, 'value': idx - 0.5})

        for sh_idx, shift in enumerate(shift_dic[player_id]['shifts']):

            if shift['start'] > tst_end or shift['end'] > tst_end:
                tst_end = 3900

            # add index, count and playername to shift
            shift['y'] = idx
            shift['cnt'] = sh_idx + 1
            shift['playername'] = player_string
            shift['start_human'] = '{0:02d}:{1:02d}'.format(*divmod(shift['start'], 60))
            shift['end_human'] = '{0:02d}:{1:02d}'.format(*divmod(shift['end'], 60))

            if shift['type'] == 'pp':
                shift['color'] = color1
                data_list_pp.append(shift)
            elif shift['type'] == 'pk':
                shift['color'] = color2
                data_list_pk.append(shift)
            else:
                shift['color'] = color3
                # add shift
                data_list.append(shift)

    x_list = []
    for second in range(0, tst_end + 1):
        x_list.append(math.ceil(second/60))

    xtickposition_list = []
    for second in range(0, tst_end +1, 300):
        xtickposition_list.append(second)

    # goals for annotations on y-bar
    annotationlabel_list = []
    for team in goal_dic:
        for goal in goal_dic[team]:
            annotationlabel_list.append({'point': {'x': goal['time'], 'y': 0, 'xAxis': 0}, 'text': goal['data']['currentScore']})

    chart_options = {
        'ctype': 'gantt',
        'chart': {
            'height': '90%',
            'alignTicks': 0,
            'style': chartstyle()
        },
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'subtitle': subtitle(csubtitle, variable_dic['subtitle_size']),
        'credits': credit(),
        'legend': legend(),
        'exporting': exporting(filename=ctitle),

        'plotOptions': {'series': {'states': {'inactive': {'opacity': 1}}}},

        'tooltip': {
            'useHTML': 0,
            'headerFormat': '',
            'pointFormat': '<b>{point.playername}</b><br>#{point.cnt} - {series.name}: {point.start_human}m - {point.end_human}m',
            'followPointer': 1,
        },

        'xAxis': [{
            'title': title(_('Game Time'), font_size, margin=15),
            'labels': {'enabled': 1, 'align': 'center'},
            'categories': x_list,
            'tickInterval': 300,
            'tickPositions': xtickposition_list,
            'tickWidth': 1,
            'grid': {'enabled': 0},
            'plotLines': [
                {'color': plotlines_color, 'width': 2, 'value': 1200},
                {'color': plotlines_color, 'width': 2, 'value': 2400},
                {'color': plotlines_color, 'width': 2, 'value': 3600}
                ],
            }],

        'yAxis': {
            'title': title('', font_size),
            'categories': playername_list,
            'grid': {'enabled': 0},
            'plotLines': y_plotlines
            },

        'annotations': [{
            'labels': annotationlabel_list,
            'labelOptions': {'y': -30, 'style': {'fontSize': variable_dic['label_size']}}
        }],

        'series': [
            {'name': ('Even Strength'), 'data': data_list, 'color': color3, 'marker': {'symbol': 'square'}},
            {'name': 'PP', 'data': data_list_pp, 'color': color1, 'marker': {'symbol': 'square'}, 'showInLegend': 0},
            {'name': 'PK', 'data': data_list_pk, 'color': color2, 'marker': {'symbol': 'square'}, 'showInLegend': 0},
            {'type': 'column', 'name': 'PP', 'color': color1, 'marker': {'symbol': 'square'}},
            {'type': 'column', 'name': 'PK', 'color': color2, 'marker': {'symbol': 'square'}}
        ]
    }

    return chart_options
