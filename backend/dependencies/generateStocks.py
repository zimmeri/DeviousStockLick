import pandas as pd

def generateStocks(n):
    try:
        data = pd.read_csv('dependencies/stockCSV/fullSP.csv', names=['Symbol', 'Name', 'Industry']).sample(n)
        data.to_csv('dependencies/stockCSV/targetSP.csv', index=False)
        return {'message': 'Target stocks generated'}, 200
    except:
        return {'message': 'Target stocks failed to generate'}, 418
