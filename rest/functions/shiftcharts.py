# -*- coding: utf-8 -*-
""" time on ice charts """
# pylint: disable=E0401
import math
import json
from rest.functions.chartparameters import chartstyle, credit, exporting, responsive_y1, title, subtitle, legend, font_size, variables_get, responsive_y1_nolabel
from rest.functions.chartparameters import chart_color1, chart_color2, chart_color3, chart_color4, chart_color6, chart_color8, plotlines_color
from rest.functions.helper import json_store

def shiftsperplayerchart_create(logger, ctitle, csubtitle, ismobile, shift_dic, goal_dic, color1, color2, color3):
    # pylint: disable=E0602
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
        playername_list.append(shift_dic[player_id]['name'])

        # add plotline in case the line-number changes
        if shift_dic[player_id]['line_number'] != line_number:
            line_number = shift_dic[player_id]['line_number']
            y_plotlines.append({'color': plotlines_color, 'width': 2, 'value': idx - 0.5})

        for shift in shift_dic[player_id]['shifts']:

            if shift['start'] > tst_end or shift['end'] > tst_end:
                tst_end = 3900

            # add index to shift
            shift['y'] = idx
            shift['name'] = 'foo'
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

    annotationlabel_list = []
    for team in goal_dic:
        for goal in goal_dic[team]:
                # print(goal['time'], goal['data']['currentScore'])
    #        # x_list2[goal['time']] = goal['data']['currentScore']
    #       xtickposition_list2.append(goal['time'])
            annotationlabel_list.append({'point': {'x': goal['time'], 'y': 0, 'xAxis': 0}, 'text': goal['data']['currentScore']})


    chart_options = {
        'ctype': 'gantt',
        'chart': {
            'height': '80%',
            'alignTicks': 0,
            'style': chartstyle()
        },
        'title': title(ctitle, variable_dic['title_size'], decoration=True),
        'credits': credit(),
        'legend': legend(),

        'xAxis': [
            {
            'title': title('', font_size),
            'labels': {'enabled': 1, 'align': 'center'},
            'categories': x_list,
            'showFirstLabel': 1,
            'showLastLabel': 1,
            'tickInterval': 300,
            'tickPositions': xtickposition_list,
            'tickWidth': 1,
            'grid': {'enabled': 0},
            'plotLines': [
                {'color': plotlines_color, 'width': 2, 'value': 1200},
                {'color': plotlines_color, 'width': 2, 'value': 2400},
                {'color': plotlines_color, 'width': 2, 'value': 3600}
                ],
            },
            ],

        'yAxis': {
            'title': title('', font_size),
            'categories': playername_list,
            'grid': {'enabled': 0},
            'plotLines': y_plotlines
            },

        'annotations': [{
                'labels': annotationlabel_list,
                'labelOptions': {
                    'y': -30,
                },
            }],

        'series': [
            {'name': ('Even Strength'), 'data': data_list, 'color': color3, 'marker': {'symbol': 'square'}},
            {'name': 'PP', 'data': data_list_pp, 'color': color1, 'marker': {'symbol': 'square'}},
            {'name': 'PK', 'data': data_list_pk, 'color': color2, 'marker': {'symbol': 'square'}},
        ]
    }

    return chart_options
