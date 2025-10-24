import requests
from api_key import key
import json
import os

FII = "NCRA11"
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={FII}.SAO&apikey={key}'
r = requests.get(url)
data = r.json()

print(data)
FILE_NAME = "NCRA11.json"
FILE_PATH = os.path.join("json", FILE_NAME)

with open(FILE_PATH, 'w') as file:
    json.dump(data, file, indent=2)