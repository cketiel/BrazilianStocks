import requests
from api_key import key
import pandas as pd
from io import StringIO
import os

# Folders
ticket_folder = "ticket_group"
csv_folder = "csv"

# Ensure the CSV output folder exists
os.makedirs(csv_folder, exist_ok=True)

# List all .txt files in ticket_folder
ticket_files = [f for f in os.listdir(ticket_folder) if f.endswith(".txt")]

# Loop through each ticket file
for ticket_file in ticket_files:
    ticket_path = os.path.join(ticket_folder, ticket_file)
    
    # Read tickets from the txt file
    with open(ticket_path, "r") as f:
        tickets = [line.strip().upper() for line in f if line.strip()]
    
    if not tickets:
        print(f"Skipping {ticket_file}, no tickets found.")
        continue

    # Create DataFrame for this group
    table = pd.DataFrame()

    # Fetch data for each ticket
    for ticket in tickets:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticket}.SAO&apikey={key}&datatype=csv'
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            row = pd.read_csv(StringIO(r.text))
            table = pd.concat([table, row], ignore_index=True)
        except Exception as e:
            print(f"Error fetching {ticket}: {e}")

    # Build output CSV filename
    base_name = os.path.splitext(ticket_file)[0]  # remove .txt
    csv_file_name = f"list_{base_name}.csv"
    csv_path = os.path.join(csv_folder, csv_file_name)

    # Save CSV
    table.to_csv(csv_path, index=False)
    print(f"CSV saved: {csv_path}")