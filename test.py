import pandas as pd
import os
import config
import json

data = pd.read_csv('query_result.csv')
data.to_json(path_or_buf='./data.json', orient='values')
data = data.to_dict('records')
with open('./data1.json', 'w') as outfile:
    json.dump(data, outfile)
print(data.head())
