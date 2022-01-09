import os
import csv
import json
import time
import errno
import datetime
import requests
import datetime
import unicodedata
import dateutil.parser
import pandas as pd
from pathlib import Path


class Twitter():
    def __init__(self, targets, tweetsPerTarget=10):
        self.tweetsPerTarget = tweetsPerTarget
        targets = targets.Symbol
        json_responses = targets.apply(lambda x: [x, self.makeRequest(x + ' lang:en')])
        responses = pd.DataFrame(columns=['target', 'id', 'text'])
        for response in json_responses:
            target = response[0]
            tweetData = response[1]['data']
            for tweet in tweetData:
                responses = responses.append({'target': target, 'id': tweet['id'], 'text': tweet['text'].replace('\n',' ').replace('\r', ' ').replace('\t', ' ').replace('\f', ' ')}, ignore_index=True)
        self.responses = responses

    def getTwitter(self):
        return self.responses

    def auth(self, r):
        r.headers["Authorization"] = f"Bearer {os.getenv('TWITTER_TOKEN')}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def connect_to_endpoint(self, url, params, next_token = None):
        params['next_token'] = next_token
        response = requests.get(url, auth=self.auth, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def create_url(self, keyword, start_date, end_date, max_results = 100):
        search_url = "https://api.twitter.com/2/tweets/search/recent"
        query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'tweet.fields': 'id,text',
                    'user.fields': 'verified',
                    'next_token': {}}
        return (search_url, query_params)

    def getTime(self):
        startTime = (datetime.date.today()- datetime.timedelta(days = 1)).isoformat() + 'T00:00:00Z' ##yesterday
        endTime = datetime.datetime.now().isoformat(timespec='seconds') + 'Z'
        return startTime, endTime


    def makeRequest(self, keyword):
        startTime, endTime = self.getTime()
        url = self.create_url(keyword, startTime,endTime, self.tweetsPerTarget)
        json_response = self.connect_to_endpoint(url[0], url[1])
        return json_response
