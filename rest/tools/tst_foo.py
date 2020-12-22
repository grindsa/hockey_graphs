#!/usr/bin/python
# -*- coding: utf-8 -*-
""" this is just a wrapper for prototyping attempts """
# import zip
from itertools import tee
from collections import deque
import more_itertools

def sliding_window(in_list, size=5):
    """ implement a sliding window for a list """
    backward_list = []
    forward_list = []
    for idx, current in enumerate(range(len(in_list)), start = 0-size):
        # print(idx, current)
        if idx < 0:
            idx = 0
        backward_list.append(in_list[idx:current+1])
        forward_list.append(in_list[current:current+size])

    return (backward_list, forward_list)

if __name__ == '__main__':

    my_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    my_array = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    (backward_list, forward_list) = sliding_window(my_array, 5)

    for ele in forward_list:
        print(ele)
