# -*- coding: utf-8 -*-
""" list of functions for shots """
# pylint: disable=E0401, C0413
import sys
import os
import re
import twitter
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hockey_graphs.settings")
import django
django.setup()
from rest.models import Socialnetworkevent
from rest.functions.helper import date_to_uts_utc

def _tweet_clean(text):
    """" clean tweets (remove hashtages and links) tweets """
    # regexp = r'https://t.co\S+|pic\.twitter\.com\S+|@\S+|#\S+'
    regexp = r'https://t.co\S+|pic\.twitter\.com\S+|@\S+'
    text_cleaned = re.sub(regexp, '', text)
    text_cleaned = re.sub(r'\s{2}', '', text_cleaned)

    return text_cleaned

def eventspermin_combine(logger, socialnetworksevents_list, home_twitter_name, visitor_twitter_name):
    """ add team to database """
    logger.debug('eventspermin_combine()')

    tweet_sec_list = {}
    for event in socialnetworksevents_list:
        # ignore tweets from team twitter accounts
        if not event['name_alternate'].lower() in [home_twitter_name.lower(), visitor_twitter_name.lower(), 'delrefsde']:
            tweet_sec_list[event['created_uts']] = event

    return tweet_sec_list

def socialnetworkevent_add(logger, fkey, fvalue, data_dic):
    """ add team to database """
    logger.debug('socialnetwork_add({0}:{1})'.format(fkey, fvalue))
    try:
        # add event
        obj, _created = Socialnetworkevent.objects.update_or_create(**{fkey: fvalue}, defaults=data_dic)
        obj.save()
        result = obj.id
    except BaseException as err_:
        logger.critical('error in socialnetwork_add(): {0}'.format(err_))
        result = None
    logger.debug('socialnetwork_add({0}:{1}) ended with {2}'.format(fkey, fvalue, result))
    return result

def socialnetworkevent_get(logger, fkey, fvalue, vlist=('match', 'source', 'name', 'name_alternate', 'created_at', 'created_uts', 'text_raw')):
    """ get info for a specifc match_id """
    logger.debug('socialnetwork_get({0}:{1})'.format(fkey, fvalue))
    try:
        if len(vlist) == 1:
            socialnetwork_list = list(Socialnetworkevent.objects.filter(**{fkey: fvalue}).values_list(vlist[0], flat=True))
        else:
            socialnetwork_list = list(Socialnetworkevent.objects.filter(**{fkey: fvalue}).values(*vlist))
    except BaseException:
        socialnetwork_list = []

    return socialnetwork_list

def tags_build(logger, home_team, visitor_team):
    """" get build taglist """
    logger.debug('tags_build()')
    result = ['#{0}vs{1}'.format(home_team.lower(), visitor_team.lower()), '#{0}{1}'.format(home_team.lower(), visitor_team.lower())]
    return result

def twitter_login(logger, consumer_key, consumer_secret, oauth_token, oauth_token_secret, domain=None):
    """ oauth login """
    logger.debug('_oauth_login()')
    # Creating the authentification
    auth = twitter.oauth.OAuth(oauth_token,
                               oauth_token_secret,
                               consumer_key,
                               consumer_secret)
    # create twitter instance
    if domain:
        twitter_api = twitter.Twitter(domain=domain, auth=auth)
    else:
        twitter_api = twitter.Twitter(auth=auth)

    return twitter_api

def twitter_image_upload(logger, twitter_api, img_list):
    """ upload image to twitter """
    logger.debug('twitter_image_upload()')

    id_list = []
    for img in img_list:
        if img:
            logger.debug('upload_img({0})\n'.format(img))
            try:
                with open(img, 'rb') as imagefile:
                    imagedata = imagefile.read()
                    id_list.append(twitter_api.media.upload(media=imagedata)['media_id_string'])
            except BaseException as err_:
                print(err_)
    return id_list

def tweets_get(logger, twitter_api, hashtag_list):
    """" get tweets """
    logger.debug('tweets_get()')

    tweet_list = []
    for hashtag in hashtag_list:
        # Get tweets for hashtag
        querystring = '{0} -filter:retweets'.format(hashtag)
        query = twitter_api.search.tweets(q=querystring, count=100, exclude_replies=False, tweet_mode="extended")
        for tweet_ in sorted(query['statuses'], key=lambda i: i['id'], reverse=False):
            tweet_uts = date_to_uts_utc(tweet_['created_at'])
            text_cleaned = _tweet_clean(tweet_['full_text'])
            tweet_list.append({
                'name': tweet_['user']['name'],
                'screen_name': tweet_['user']['screen_name'],
                'id': tweet_['id'], 'uts': tweet_uts,
                'text_cleaned': text_cleaned,
                'text_raw': tweet_['full_text'],
                'hashtag': hashtag,
                'created_at': tweet_['created_at']
            })

    return tweet_list

def _mapping_shifts_add(logger, shift_list):
    """ add period events to mapping list """
    logger.debug('_mapping_shifts_add()')

    # this is the dicrectory containg the mapping between matchtime and realtime
    time_mapping_dic = {}
    for shift in shift_list:
        # print(shift['startTime']['time'], shift['startTime']['realtime'])
        time_mapping_dic[shift['startTime']['time']] = shift['startTime']['realtime']
    return  time_mapping_dic

def _mapping_shots_add(logger, time_mapping_dic, shot_list):
    """ add shots to mapping list """
    logger.debug('_mapping_shots_add()')

    for shot in shot_list:
        if shot['timestamp'] not in time_mapping_dic:
            time_mapping_dic[shot['timestamp']] = shot['real_date']
    return time_mapping_dic

def _mapping_periodevents_add(logger, time_mapping_dic, periodevent_list):
    """ add period events to mapping list """
    logger.debug('time2date_map()')

    # add information from period events:
    for period in periodevent_list:
        for event in periodevent_list[period]:
            if 'data' in event:
                # these are some events (goal) with a mapping between time in game and real time
                if 'realTime' in event['data']:
                    time_mapping_dic[event['time']] = event['data']['realTime']
                # these are penalties who even have to mappings per event - we use both
                if 'time' in event['data'] and isinstance(event['data']['time'], dict):
                    if 'from' in event['data']['time']:
                        if event['data']['time']['from']['scoreboardTime'] not in time_mapping_dic:
                            time_mapping_dic[event['data']['time']['from']['scoreboardTime']] = event['data']['time']['from']['realTime']
                    if 'to' in event['data']['time']:
                        if event['data']['time']['to']['scoreboardTime'] not in time_mapping_dic:
                            time_mapping_dic[event['data']['time']['to']['scoreboardTime']] = event['data']['time']['to']['realTime']
    return time_mapping_dic

def _mapping_uts_convert(logger, time_mapping_dic):
    logger.debug('_mapping_convert()')

    # we need to create an entry per second for faster access the below describes the amount of game seconds (default 3600, OT 3900)
    max_sec = 3600
    # timezone offset
    tz_offset = 3600

    sec_mapping_uts_dic = {}
    for matchtime in time_mapping_dic:
        # convert real_date to uts
        sec_mapping_uts_dic[matchtime] = date_to_uts_utc(time_mapping_dic[matchtime]) - tz_offset
        # adjust game seconds in case of overtime
        if matchtime >= max_sec:
            max_sec = 3900

    # create missing seconds in hash - create an artifical entry by adding one sec to n-1 date (we hopefully have)
    for sec_ in range(0, max_sec+1):
        if sec_ not in sec_mapping_uts_dic:
            sec_mapping_uts_dic[sec_] = sec_mapping_uts_dic[sec_-1] + 1

    return sec_mapping_uts_dic

def _mapping_to_min(logger, sec_mapping_uts_dic):
    """ create a dictionary including a mapping between gametime and realtime (uts) - this is needed to map the tweets """
    logger.debug('_mapping_to_min()')

    min_mapping_uts_dic = {}
    for sec_ in sorted(sec_mapping_uts_dic):
        if sec_ % 60 == 0:
            min_mapping_uts_dic[int(sec_/60)] = sec_mapping_uts_dic[sec_]

    return min_mapping_uts_dic

def time2date_map(logger, shot_list, shift_list, periodevent_list):
    """ create a dictionary including a mapping between gametime and realtime (uts) - this is needed to map the tweets """
    logger.debug('time2date_map()')

    # build initial dictionary based on shifts
    time_mapping_dic = _mapping_shifts_add(logger, shift_list)

    # add shot events to mapping directory
    time_mapping_dic = _mapping_shots_add(logger, time_mapping_dic, shot_list)

    # add period events to mapping dictionary
    time_mapping_dic = _mapping_periodevents_add(logger, time_mapping_dic, periodevent_list)

    # convert "human time" to uts
    sec_mapping_uts_dic = _mapping_uts_convert(logger, time_mapping_dic)

    return sec_mapping_uts_dic
