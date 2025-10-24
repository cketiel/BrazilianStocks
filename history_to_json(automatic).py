# automatic version
# The script will automatically retry all failed tickets until they are successfully downloaded.
# Maintains logs, summary, skip of existing files, and respect the API limit.
# You won't have to manually rerun the script for failed ones.

import os
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from api_key import key

# Frequencies to fetch
FREQUENCIES = ["d", "w"]

# Output folder
OUTPUT_DIR = "json"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Log file
LOG_FILE = "download_log.txt"

# AlphaVantage free API limit
API_REQUESTS_PER_MINUTE = 5

# Number of concurrent workers
WORKERS = 2

# Calculate wait time per request to comply with rate limit
WAIT_TIME = max(12, (60 / API_REQUESTS_PER_MINUTE) * WORKERS)

# Lists to track summary
processed = []
skipped = []
failed = []

# Logging function
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

# Fetch data with retries
def fetch_data(ticket, frequency, retries=3):
    if frequency == "d":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticket}.SAO&outputsize=full&apikey={key}'
    else:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={ticket}.SAO&apikey={key}'

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "Error Message" in data or "Note" in data:
                raise ValueError(f"API returned an error: {data}")
            return data
        except Exception as e:
            log_message(f"Error fetching {ticket}_{frequency} (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                log_message(f"Retrying in {WAIT_TIME} seconds...")
                time.sleep(WAIT_TIME)
            else:
                log_message(f"Failed to fetch {ticket}_{frequency} after {retries} attempts.")
                return {"error": str(e)}

# Save JSON data
def save_json(ticket_name, data):
    file_path = os.path.join(OUTPUT_DIR, f"{ticket_name}.json")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    log_message(f"Saved {ticket_name}.json")

# Worker function
def process_ticket(ticket, frequency):
    ticket_name = f"{ticket}_{frequency}"
    file_path = os.path.join(OUTPUT_DIR, f"{ticket_name}.json")

    # Skip if JSON already exists
    if os.path.exists(file_path):
        log_message(f"Skipping {ticket_name}, file already exists.")
        skipped.append(ticket_name)
        return ticket_name

    log_message(f"Processing {ticket_name}")
    data = fetch_data(ticket, frequency)
    save_json(ticket_name, data)
    
    # Track failed files
    if "error" in data:
        failed.append(ticket_name)
    else:
        processed.append(ticket_name)

    time.sleep(WAIT_TIME)
    return ticket_name

# Read tickets from file
def read_tickets(file_path="tickets.txt"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found. Create a text file with one ticket per line.")
    with open(file_path, "r") as f:
        tickets = [line.strip().upper() for line in f if line.strip()]
    return tickets

# Save failed tickets to a separate file
def save_failed_tickets():
    if failed:
        with open("failed_tickets.txt", "w") as f:
            for ticket_name in failed:
                f.write(ticket_name + "\n")
        log_message(f"Saved {len(failed)} failed tickets to failed_tickets.txt")

# Main function
def main():
    try:
        tickets = read_tickets()
        log_message(f"Starting batch download for {len(tickets)} tickets...")

        # Continue looping until all tickets are processed successfully
        remaining_tickets = tickets.copy()
        while remaining_tickets:
            failed.clear()
            with ThreadPoolExecutor(max_workers=WORKERS) as executor:
                futures = []
                for ticket in remaining_tickets:
                    for freq in FREQUENCIES:
                        futures.append(executor.submit(process_ticket, ticket, freq))
                for future in as_completed(futures):
                    _ = future.result()
            
            if failed:
                log_message(f"{len(failed)} tickets failed. Retrying after {WAIT_TIME} seconds...")
                remaining_tickets = list({t.split("_")[0] for t in failed})  # extract ticket names
                time.sleep(WAIT_TIME)
            else:
                remaining_tickets = []

        # Summary
        print("\n===== SUMMARY =====")
        print(f"Processed ({len(processed)}): {', '.join(processed) if processed else 'None'}")
        print(f"Skipped ({len(skipped)}): {', '.join(skipped) if skipped else 'None'}")
        print(f"Failed ({len(failed)}): {', '.join(failed) if failed else 'None'}")
        log_message("Batch download completed with summary above.")

        # Save any remaining failed tickets
        save_failed_tickets()

    except Exception as e:
        log_message(f"Fatal error: {e}")

if __name__ == "__main__":
    main()