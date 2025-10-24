# Generate a CSV for each .txt in ticket_group/ → named list_<filename>.csv.
# Additionally, generate a single master CSV that combines all tickets from all groups. Generates master CSV (master_list.csv) with all tickets combined.
# Maintains on-screen logs of tickets with errors. Prints logs of tickets with errors for easy review.
# Handles empty files or errors fetching individual tickets.

# AlphaVantage free: maximum 5 requests per minute. The script will add an automatic delay between requests to respect that limit.
# Retries automatically tickets that fail until all succeed.
# Logs progress and errors in real time.
# Handles empty or invalid responses gracefully.
# Concurrent downloads with ThreadPoolExecutor → faster than sequential.
# Creates failed_tickets.txt for tickets that could not be downloaded.
# Summary printed at the end: groups, total tickets, failures, CSVs.

import requests
from api_key import key
import pandas as pd
from io import StringIO
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Folders
ticket_folder = "ticket_group"
csv_folder = "csv"
failed_file_path = os.path.join(csv_folder, "failed_tickets.txt")

# API configuration
API_REQUESTS_PER_MINUTE = 5
WAIT_TIME = 60 / API_REQUESTS_PER_MINUTE  # seconds per request
MAX_WORKERS = 2  # Number of concurrent threads
RETRIES = 3       # Number of retries per ticket

# Ensure the CSV output folder exists
os.makedirs(csv_folder, exist_ok=True)

# List all .txt files in ticket_folder
ticket_files = [f for f in os.listdir(ticket_folder) if f.endswith(".txt")]

# Master DataFrame for all tickets
master_table = pd.DataFrame()
all_failed_tickets = []

# Function to fetch a ticket with retries
def fetch_ticket(ticket, retries=RETRIES):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticket}.SAO&apikey={key}&datatype=csv'
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            row = pd.read_csv(StringIO(r.text))
            if row.empty:
                raise ValueError("Empty CSV received from API")
            return row
        except Exception as e:
            print(f"Error fetching {ticket} (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(WAIT_TIME)
            else:
                print(f"Failed to fetch {ticket} after {retries} attempts.")
                return None

# Function to process a single ticket and return (ticket_name, DataFrame)
def process_ticket(ticket):
    row = fetch_ticket(ticket)
    return (ticket, row)

# Loop through each ticket file
for ticket_file in ticket_files:
    ticket_path = os.path.join(ticket_folder, ticket_file)
    
    # Read tickets from the txt file
    with open(ticket_path, "r") as f:
        tickets = [line.strip().upper() for line in f if line.strip()]
    
    if not tickets:
        print(f"Skipping {ticket_file}, no tickets found.")
        continue

    print(f"\nProcessing group: {ticket_file} with {len(tickets)} tickets...")

    # Create DataFrame for this group
    table = pd.DataFrame()
    remaining_tickets = tickets.copy()
    group_failed_tickets = []

    # Retry loop until all tickets are processed
    while remaining_tickets:
        failed_tickets = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_ticket, ticket): ticket for ticket in remaining_tickets}
            for future in as_completed(futures):
                ticket = futures[future]
                row = future.result()[1]
                if row is not None:
                    table = pd.concat([table, row], ignore_index=True)
                    master_table = pd.concat([master_table, row], ignore_index=True)
                    print(f"{ticket} downloaded successfully.")
                else:
                    failed_tickets.append(ticket)
                time.sleep(WAIT_TIME)  # Respect API limit

        remaining_tickets = failed_tickets
        group_failed_tickets.extend(failed_tickets)
        if remaining_tickets:
            print(f"{len(remaining_tickets)} tickets failed, retrying...")

    # Build output CSV filename for this group
    base_name = os.path.splitext(ticket_file)[0]  # remove .txt
    csv_file_name = f"list_{base_name}.csv"
    csv_path = os.path.join(csv_folder, csv_file_name)

    # Save CSV for this group
    table.to_csv(csv_path, index=False)
    print(f"CSV saved: {csv_path}\n")

    # Add failed tickets of this group to global list
    all_failed_tickets.extend(group_failed_tickets)

# Save the master CSV combining all tickets
master_csv_path = os.path.join(csv_folder, "master_list.csv")
master_table.to_csv(master_csv_path, index=False)
print(f"Master CSV saved: {master_csv_path}")

# Save failed tickets to a text file
if all_failed_tickets:
    with open(failed_file_path, "w") as f:
        for ticket in all_failed_tickets:
            f.write(ticket + "\n")
    print(f"Failed tickets saved to: {failed_file_path}")
else:
    print("All tickets downloaded successfully. No failures.")

# Final summary
print("\n===== Summary =====")
print(f"Total groups processed: {len(ticket_files)}")
print(f"Total tickets downloaded: {len(master_table)}")
print(f"Total failed tickets: {len(all_failed_tickets)}")
print(f"CSV files generated in folder: {csv_folder}")
print("===================")