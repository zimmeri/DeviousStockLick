import os
import errno
import datetime
import numpy as np
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen


class Headline():
    def __init__(self, targets):
        targets = targets.Symbol.to_numpy()
        links = pd.DataFrame()
        for target in targets:
            newsList = self.requestTargets(target)
            newsList['target'] = target
            links = links.append(newsList)
        self.links = links.reset_index(drop=True)
            #if not os.path.exists('data/' +(datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')):
            #    os.mkdir('data/' +(datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
            #links.to_csv('data/' +(datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') + '/headlines.csv')

    def getHeadline(self):
        return self.links

    def getNews(self, html):
        try:
            news = pd.read_html(str(html), attrs = {'class': 'fullview-news-outer'})[0]
            links = []
            for a in html.find_all('a', class_="tab-link-news"):
                links.append(a['href'])
            news.columns = ['Date', 'text']
            news['Link'] = links
            return news
        except Exception as e:
            raise Exception(500, 'Headline getNews()')


    #this needs to be fine tuned and expanded. Need more news data, and only data that happened in the last 24 hours
    def requestTargets(self, target):
        try:
            url = ("http://finviz.com/quote.ashx?t=" + target.lower())
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            html = soup(webpage, "html.parser")
            return self.getNews(html)
        except Exception as e:
            raise Exception(404, 'Finviz link not found')
