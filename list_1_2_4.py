import requests
from api_key import key
import pandas as pd
from io import StringIO
import os

# List of stocks
stoks = ["RURA11", "LIFE11", "DCRA11", "NCRA11"]

# Create DataFrame
table = pd.DataFrame()

# Ensure the "csv" folder exists
output_folder = "csv"
os.makedirs(output_folder, exist_ok=True)

# Fetch data and concatenate
for stok in stoks:
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stok}.SAO&apikey={key}&datatype=csv'
    r = requests.get(url)
    row = pd.read_csv(StringIO(r.text))
    table = pd.concat([table, row], ignore_index=True)

# Path to save CSV
csv_file_path = os.path.join(output_folder, "list_1_2_4.csv")

# Save DataFrame to CSV
table.to_csv(csv_file_path, index=False)

print(f"CSV file saved successfully at: {csv_file_path}")