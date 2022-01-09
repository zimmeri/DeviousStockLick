from flask import Flask, request
from flask_restful import Resource
from pathlib import Path

import pandas as pd
from dependencies.generateStocks import generateStocks

class Generate(Resource):
    def get(self):
        file = Path("./dependencies/stockCSV/targetSP.csv")
        if file.is_file():
            data = pd.read_csv(file)
            return data.to_json(), 200
        else:
            return {'message': 'No target file'}, 418

    def post(self):
        n = request.get_json()['n']
        message, code = generateStocks(n)
        return message, code
