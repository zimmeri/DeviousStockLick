import datetime
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


class Model():
    def __init__(self, targets, tweets, headlines):
        alpha = 0.3
        sentiments = pd.DataFrame()
        pipe = self.modelPipe()
        sentiments = sentiments.append(self.buildSentiments(tweets,pipe,'text', 'tweet'))
        sentiments = sentiments.append(self.buildSentiments(headlines, pipe, 'text', 'headline'))
        self.sentiments = sentiments.reset_index(drop=True)
        scores = pd.DataFrame()
        for target in targets:
            scores = scores.append(self.buildScore(target, sentiments), ignore_index=True)
        scores['combined'] = scores['tweets']*alpha + scores['headlines']*(1-alpha)
        scores['alpha'] = alpha
        scores = self.buyShares(scores)
        self.scores = scores

    def getSentiments(self):
        return self.sentiments

    def getScores(self):
        return self.scores

    def modelPipe(self):
        tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
        model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
        pipe = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        return pipe

    def buildSentiments(self, data, pipe, column, typ):
        sent = pd.DataFrame(columns=['target','label','score', 'text'])
        for row in data.iterrows():
            try:
                out = pipe(row[1][column])[0]
                out['target'] = row[1]['target']
                out['type'] = typ
                out['text'] = row[1]['text']
                sent = sent.append(out, ignore_index=True)
            except:
                print(f'Warning: sentiment not round{row[1][column]}')
        return sent

    def buildScore(self, target, sentiments):
        tweets = sentiments[sentiments['type'] == 'tweet']
        tweets = tweets[tweets['target'] == target]
        headlines = sentiments[sentiments['type'] == 'headline']
        headlines = headlines[headlines['target'] == target]
        tweets['score'] = tweets.apply(lambda x: self.posNegNeut(x) , axis=1)
        headlines['score'] = headlines.apply(lambda x: self.posNegNeut(x) , axis=1)
        return{'target': target, 'tweets': tweets['score'].mean(), 'headlines':headlines['score'].mean()}

    def posNegNeut(self, x):
        if x['label'] == 'neutral':
            return 0
        elif x['label'] == 'negative':
            return x['score']*-1
        else:
            return x['score']

    def buyShares(self,scores):
        scores['combinedBuy'] = scores.apply(lambda x: self.shareConf(x, 'combined'), axis=1)
        scores['tweetBuy'] = scores.apply(lambda x: self.shareConf(x, 'tweets'), axis=1)
        scores['headlineBuy'] = scores.apply(lambda x: self.shareConf(x, 'headlines'), axis=1)
        return scores

    def shareConf(self, x, target):
        if x[target] < .1:
            return 0
        elif x[target] < .2:
            return 10
        elif x[target] < .3:
            return 20
        elif x[target] < .4:
            return 30
        elif x[target] < .5:
            return 40
        else:
            return 50
