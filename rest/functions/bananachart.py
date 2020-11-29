# -*- coding: utf-8 -*-
""" test chart for rest-testing """
# pylint: disable=E0401

def banana_chart1_create(logger, title):
    # pylint: disable=E0602
    """ create banana_chart """
    logger.debug('banana_chart_create()')

    chart_options = {
        'chart': {'type': 'bar'},
        'title': {'text': title},
        'xAxis': {'categories': ['Apples', 'Bananas', 'Oranges']},
        'yAxis': {'title': {'text': 'Fruit eaten'}},
        'series': [
            {'name': 'Jane', 'data': [1, 2, 3]},
            {'name': 'John', 'data': [3, 6, 9]}
            ]
        }

    stat_entry = {
        'title': title,
        'chart': chart_options,
        'updates': {
            1: {'text': 'foo1', 'chartoptions': {'title': {'text': 'foo10'}, 'series': [{'data': [1, 2, 3]}, {'data': [3, 9, 6]}]}},
            2: {'text': 'foo2', 'chartoptions': {'title': {'text': 'foo10'}, 'series': [{'data': [2, 3, 1]}, {'data': [6, 3, 9]}]}},
            3: {'text': 'foo3', 'chartoptions': {'title': {'text': 'foo10'}, 'series': [{'data': [3, 1, 2]}, {'data': [9, 6, 3]}]}}
        },
        'sliderlength': 3
    }
    return stat_entry

def banana_chart2_create(logger, title):
    # pylint: disable=E0602
    """ create banana_chart """
    logger.debug('banana_chart_create()')

    chart_options = {
        'chart': {'type': 'bar'},
        'title': {'text': title},
        'xAxis': {'categories': ['Apples', 'Bananas', 'Oranges']},
        'yAxis': {'title': {'text': 'Fruit eaten'}},
        'series': [
            {'name': 'Jane', 'data': [3, 6, 9]},
            {'name': 'John', 'data': [1, 2, 3]}
            ]
        }

    stat_entry = {
        'title': title,
        'chart': chart_options,
        'updates': {
            1: {'text': 'foo1', 'chartoptions': {'title': {'text': 'foo10'}, 'series': [{'data': [3, 9, 6]}, {'data': [1, 2, 3]}]}},
            2: {'text': 'foo2', 'chartoptions': {'title': {'text': 'foo10'}, 'series': [{'data': [6, 3, 9]}, {'data': [2, 3, 1]}]}},
            3: {'text': 'foo3', 'chartoptions': {'title': {'text': 'foo10'}, 'series': [{'data': [9, 6, 3]}, {'data': [3, 1, 2]}]}}  
        },
        'sliderlength': 3
    }
    return stat_entry
