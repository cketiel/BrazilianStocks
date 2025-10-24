import os
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from api_key import key

# List of tickets
TICKERS = ["AGRX11", "CACR11", "DCRA11", "LIFE11", "NCRA11", "RURA11", "VGIA11", "VGIR11"]

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
    log_message(f"Processing {ticket_name}")
    data = fetch_data(ticket, frequency)
    save_json(ticket_name, data)
    # Wait dynamically to respect API rate limit
    time.sleep(WAIT_TIME)
    return ticket_name

# Main function
def main():
    log_message("Starting batch download with rate-limit compliance...")
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = []
        for ticket in TICKERS:
            for freq in FREQUENCIES:
                futures.append(executor.submit(process_ticket, ticket, freq))
        for future in as_completed(futures):
            result = future.result()
            log_message(f"Completed {result}")
    log_message("All JSON files have been generated successfully.")

if __name__ == "__main__":
    main()