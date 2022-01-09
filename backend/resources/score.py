from flask import Flask, request
from flask_restful import Resource
from pathlib import Path

import os
import errno
import pandas as pd
from dependencies.model import Model
from dependencies.twitter import Twitter
from dependencies.headline import Headline

class Score(Resource):
    def get(self):
        file = Path("./dependencies/stockCSV/targetSP.csv")
        if file.is_file():
            data = pd.read_csv(file)
            return data.to_json(), 200
        else:
            return {'message': 'No target file'}, 418

    def post(self):
        n = request.get_json()['n']
        targets = self.getTargets()
        headlines = Headline(targets).getHeadline()
        tweets = Twitter(targets,n).getTwitter()
        print(headlines, tweets)
        model = Model(targets, tweets, headlines)
        #saves to data database here, one with all the data and their sentiment, another with the actual scores
        sentiments = model.getSentiments()
        scores = model.getScores()
        return {'message': 'Tweets and Headlines saved'}, 200

    def getTargets(self):
        file = Path("./dependencies/stockCSV/targetSP.csv")
        if file.is_file():
            data = pd.read_csv(file, header=0)
            return data
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)
