# -*- coding: utf-8 -*-
""" test chart for rest-testing """
# pylint: disable=E0401

def banana_chart_create(logger, title):
    # pylint: disable=E0602
    """ create banana_chart """
    logger.debug('banana_chart_create()')

    chart_options = {
        'chart': {'type': 'bar'},
        'title': {'text': title},
        'xAxis': {'categories': ['Apples', 'Bananas', 'Oranges']},
        'yAxis': {'title': {'text': 'Fruit eaten'}},
        'series': [
            {'name': 'Jane', 'data': [1, 0, 4]},
            {'name': 'John', 'data': [5, 7, 3]}
            ]
        }

    stat_entry = {
        'title': title,
        'chart': chart_options,
        'updates': {
            1: {'title': {'text': 'foo10'}, 'series': [{'data': [5, 6, 7]}, {'data': [2, 1, 3]}]},
            2: {'title': {'text': 'foo10'}, 'series': [{'data': [2, 6, 5]}, {'data': [4, 2, 7]}]},
            3: {'title': {'text': 'foo10'}, 'series': [{'data': [1, 0, 4]}, {'data': [5, 7, 3]}]}
        }
    }
    return stat_entry
