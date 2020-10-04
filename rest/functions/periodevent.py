# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Periodevent

def periodevent_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('periodevent_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add event
        obj, _created = Periodevent.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in periodevent_add(): {0}'.format(err_))
        result = None
    logger.debug('periodevent_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result
