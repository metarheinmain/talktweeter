import json
import os
from datetime import datetime

import dateutil.parser
import pytz
import requests
import twitter

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, JSON_URL, TIMEZONE


def ellipsize(s, l):
    if len(s) > l:
        return s[:l - 1] + '…'
    else:
        return s


def build_tweet(talk):
    template = 'Next up in {room}: »{talk}« by {speaker}'
    shorter_template = 'Next up in {room}: »{talk}«'
    speakers = ', '.join([s['name'] for s in talk['persons']])

    if speakers:
        tweet = template.format(room=talk['room'], talk=talk['title'], speaker=speakers)

        if len(tweet) > 140:
            max_title_length = 140 - (len(tweet) - len(talk['title']))
            if max_title_length > 40:
                tweet = template.format(room=talk['room'], talk=ellipsize(talk['title'], max_title_length),
                                        speaker=speakers)
            else:
                tweet = shorter_template.format(room=talk['room'], talk=talk['title'])

                if len(tweet) > 140:
                    max_title_length = 140 - (len(tweet) - len(talk['title']))
                    tweet = shorter_template.format(room=talk['room'], talk=ellipsize(talk['title'], max_title_length))

    else:
        tweet = shorter_template.format(room=talk['room'], talk=talk['title'])

        if len(tweet) > 140:
            max_title_length = 140 - (len(tweet) - len(talk['title']))
            tweet = shorter_template.format(room=talk['room'], talk=ellipsize(talk['title'], max_title_length))

    if len(tweet) > 140:
        tweet = tweet[:139] + '…'
    return tweet


def main():
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

    cache = {'sent': []}
    if os.path.exists('cache.json'):
        with open('cache.json', 'r') as f:
            cache = json.load(f)

    jdata = requests.get(JSON_URL).json()
    to_send = []

    for day in jdata['schedule']['conference']['days']:
        for room, talks in day['rooms'].items():
            for talk in talks:
                d = dateutil.parser.parse(talk['date']).astimezone(tz)

                if d < now or (d - now).seconds > 60 * 10:
                    continue

                if talk['guid'] in cache['sent']:
                    continue

                to_send.append(talk)

    for talk in to_send:
        api.PostUpdate(build_tweet(talk))
        cache['sent'].append(talk['guid'])

    with open('cache.json', 'w') as f:
        json.dump(cache, f)

main()
