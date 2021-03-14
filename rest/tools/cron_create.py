#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" create daly cron-entries for tippspiel """
# pylint: disable=C0413, E0401, R0914
from __future__ import absolute_import
import os
import sys
import time
from datetime import datetime, timedelta
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
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    match_list_today = matchdays_get(logger, None, 'date', today)
    match_list_yesterday = matchdays_get(logger, None, 'date', yesterday)

    # initialize the crontab
    cron = CronTab(tabfile=filename, user=False)

    # remove all entries
    cron.remove_all()

    # create an entry for the script
    self = cron.new(command=me_script, comment='daily check if we need to create contab entries', user='root')
    self.hour.on(1)
    self.minute.on(5)

    # create cron-entry to check facebook-token
    tkchk = cron.new(command=path + '/fb_token_chk.py -t 7 -i /var/www/hockey_graphs/rest/tools/conf/fb-ua-token.json', comment='check expiry of facebook token', user='root')
    tkchk.hour.on(1)
    tkchk.minute.on(5)

    # create cron-entry to update player data
    pupd = cron.new(command=path + '/players_update.py', comment='update player information', user='root')
    pupd.dow.on('MON', 'WED', 'FRI')
    pupd.hour.on(1)
    pupd.minute.on(15)

    # create cron-entry to update match data
    mupd = cron.new(command=path + '/match_import.py -s 3', comment='update match_information', user='root')
    mupd.dow.on('MON', 'WED', 'FRI')
    mupd.hour.on(1)
    mupd.minute.on(20)

    ltime = time.strftime("%d.%m.%Y")

    # we have matches today and need to create the cron_entries for polling
    if match_list_today or match_list_yesterday:

        message = ltime+' hockey_graphs: crontab entries created for:'

        if match_list_today:
        # we need timestamp from first and last match to estimate the range from cron
            if 'matches' in match_list_today[today]:
                (fhour, _fmin) = datetime.fromtimestamp(match_list_today[today]['matches'][0]['date_uts'], tz=tzone).strftime("%H:%M").split(':')
                (lhour, _lmin) = datetime.fromtimestamp(match_list_today[today]['matches'][-1]['date_uts'], tz=tzone).strftime("%H:%M").split(':')

                # create cron-entry to get live statistics
                lstats = cron.new(command=path + '/matchdata_update.py -o', comment='update match statistics', user='root')
                lstats.hour.during(int(fhour), int(lhour)+3).every(1)
                lstats.minute.every(2)

                # start export server
                svc_st = cron.new(command='service highcharts start', comment='start export server', user='root')
                svc_st.hour.on(int(fhour)-1)
                svc_st.minute.on(0)

                # stop messenger
                svc_end = cron.new(command='service highcharts stop', comment='stop export server', user='root')
                svc_end.hour.on(23)
                svc_end.minute.on(45)

                # create cron-entry for tweeter.py
                lstats = cron.new(command=path + '/tweeter.py -i 24', comment='tweet statistics', user='root')
                lstats.hour.during(int(fhour), int(lhour)+3).every(1)
                lstats.minute.every(5)

                # create cron-entry to get live statistics
                ltag = cron.new(command=path + '/tag_fetcher.py -i 24 -b 4', comment='update twitter tags', user='root')
                ltag.hour.during(int(fhour)-1, int(lhour)+3).every(1)
                ltag.minute.every(10)

                # update shifts at 11:05pm
                shifts = cron.new(command=path+'/matchdata_update.py -i 24 --shifts --hgs /var/www/hockey_graphs/hgs_data --save /var/www/hockey_graphs/data --gitrepo', comment='update shifts', user='root')
                shifts.hour.on(23)
                shifts.minute.on(5)

                # update twitter tags at 11:00pm
                tag = cron.new(command=path+'/tag_fetcher.py -i 24 -b 4 --save /var/www/hockey_graphs/data', comment='update twitter tags', user='root')
                tag.hour.on(23)
                tag.minute.on(0)

                # update teamstats at 11pm
                teamstats = cron.new(command=path+'/teamstat_load.py -i 24 --xgdata /var/www/hockey_graphs/rest/tools/conf/xg_model_data.json --xgweights /var/www/hockey_graphs/rest/tools/conf/xg_weights.json', comment='teamstats', user='root')
                teamstats.hour.on(23)
                teamstats.minute.on(5)

                # update fbook group at 11pm
                teamstats = cron.new(command=path+'/tweet_summary.py', comment='matchday summary into facebook hockeygraphs', user='root')
                teamstats.hour.on(23)
                teamstats.minute.on(5)

                message = '{0}{1}'.format(message, today)

        if match_list_yesterday:
            if 'matches' in match_list_yesterday[yesterday]:
                # update shifts at 11pm
                ndshifts = cron.new(command=path+'/matchdata_update.py -i 30 --save /var/www/hockey_graphs/data --gitrepo', comment='update shifts', user='root')
                ndshifts.hour.on(3, 9, 15)
                ndshifts.minute.on(0)

                # update teamstats at 11pm
                ndteamstats = cron.new(command=path+'/teamstat_load.py -i 30 --xgdata /var/www/hockey_graphs/rest/tools/conf/xg_model_data.json --xgweights /var/www/hockey_graphs/rest/tools/conf/xg_weights.json', comment='teamstats', user='root')
                ndteamstats.hour.on(3, 9, 15)
                ndteamstats.minute.on(5)

                ndtag = cron.new(command=path+'/tag_fetcher.py -i 24 -b 4 --save /var/www/hockey_graphs/data', comment='update twitter tags', user='root')
                ndtag.hour.on(3)
                ndtag.minute.on(0)

                message = '{0}, {1}'.format(message, yesterday)

        if(hasattr(settings, 'WA_ADMIN_NUMBER') and hasattr(settings, 'WA_SRV') and hasattr(settings, 'WA_PORT')):
            # send whatsapp message
            # message = ltime+' hockey_graphs: crontab entries created for matchday: {0}'.format(today)
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
