import requests
from api_key import key
import pandas as pd
from io import StringIO

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
#url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo'

# Format Json
url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=BBAS3.SAO&apikey={key}'
r = requests.get(url)
data = r.json()

print(data)

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey={key}'
r = requests.get(url)
data = r.json()

print(data["Meta Data"])

# Format csv
url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey={key}&datatype=csv'
r = requests.get(url)

print(r.text)

url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=ITUB3.SAO&apikey={key}&datatype=csv'
r = requests.get(url)

table = pd.read_csv(StringIO(r.text))
print(table)
#display(table)

# show many stoks in table
stoks = ["ITUB3", "ABEV3", "BBAS3"]
table = pd.DataFrame()
for stok in stoks:
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stok}.SAO&apikey={key}&datatype=csv'
    r = requests.get(url)
    row = pd.read_csv(StringIO(r.text))
    table = pd.concat([table, row])
print(table)

# Earnings
url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey={key}'
r = requests.get(url)
data = r.json()

print(data)