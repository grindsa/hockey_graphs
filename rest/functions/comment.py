# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Comment

def comment_get(logger, fkey, fvalue, vlist=('name', 'de', 'en')):
    """ get info for a specifc match_id """
    logger.debug('comment_get({0}:{1})'.format(fkey, fvalue))

    try:
        if len(vlist) == 1:
            comment = list(Comment.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))[0]
        else:
            comment_dic = Comment.objects.filter(**{fkey: fvalue}).values(*vlist)[0]
    except:
        comment = {}

    return comment
