#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" create daly cron-entries for tippspiel """
# pylint: disable=C0413, E0401, R0914
from __future__ import absolute_import
import os
import sys
import time
from datetime import datetime
from crontab import CronTab
from pytz import timezone

# import django
import django
# we need this to load the django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
django.setup()

# import project settings
from django.conf import settings
from wa_hack_cli import simple_send
from rest.functions.helper import logger_setup
from rest.functions.matchday import matchdays_get

# from wa_hack_cli import simple_send
TIMEZONE = timezone('Europe/Berlin')

def create_cron_entries(logger, tzone):
    """ create cron entries moved into a function as i was to lazy to change the variables to upper style """
    logger.debug('create_cron_entries()')

    # filename
    filename = '/etc/cron.d/hockey_graphs'

    # current directory and filename
    path = os.path.dirname(os.path.realpath(__file__))
    me_script = os.path.realpath(__file__)

    # unix timestamp
    uts_now = int(time.time())

    # get matches of the day
    # today = '2020-02-16'
    today = datetime.fromtimestamp(uts_now, tz=tzone).strftime("%Y-%m-%d")
    match_list = matchdays_get(logger, None, 'date', today)

    # initialize the crontab
    cron = CronTab(tabfile=filename, user=False)

    # remove all entries
    cron.remove_all()

    # create an entry for the script
    self = cron.new(command=me_script, comment='daily check if we need to create contab entries', user='root')
    self.hour.on(1)
    self.minute.on(5)

    # we have matches today and need to create the cron_entries for polling
    if match_list:

        # we need timestamp from first and last match to estimate the range from cron
        if 'matches' in match_list[today]:
            (fhour, _fmin) = datetime.fromtimestamp(match_list[today]['matches'][0]['date_uts'], tz=tzone).strftime("%H:%M").split(':')
            (lhour, _lmin) = datetime.fromtimestamp(match_list[today]['matches'][-1]['date_uts'], tz=tzone).strftime("%H:%M").split(':')

            # create cron-entry to get live statistics
            lstats = cron.new(command=path + '/matchdata_update.py', comment='update match statistics', user='root')
            lstats.hour.during(int(fhour), int(lhour)+3).every(1)
            lstats.minute.every(2)

            # update shifts at 11pm
            shifts = cron.new(command=path+'/shifts_update.py', comment='update shifts', user='root')
            shifts.hour.on(23)
            shifts.minute.on(00)

            if(hasattr(settings, 'WA_ADMIN_NUMBER') and hasattr(settings, 'WA_SRV') and hasattr(settings, 'WA_PORT')):

                # send whatsapp message
                ltime = time.strftime("%d.%m.%Y")
                message = ltime+' hockey_graphs: crontab entries created for matchday: {0}'.format(today)
                try:
                    simple_send(settings.WA_SRV, settings.WA_PORT, settings.WA_ADMIN_NUMBER, message)
                except BaseException:
                    pass

    cron.write(filename)

if __name__ == "__main__":

    # initialize debug mode and logger
    DEBUG = False
    LOGGER = logger_setup(DEBUG)

    TIMEZONE = timezone('Europe/Berlin')
    # create cron entries
    create_cron_entries(LOGGER, TIMEZONE)
