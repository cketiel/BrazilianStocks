import argparse
import os
import json
import requests
from api_key import key

# Function to print the content of the second parameter
def print_content(parameter):
    print(f"Ticket: {parameter}")

def get_data(ticket, frequency):
    FII = ticket
    if frequency == 'd':
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={FII}.SAO&outputsize=full&apikey={key}'
    else:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={FII}.SAO&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data
   
def save(ticket, data):
    FILE_NAME = f"{ticket}.json"
    FILE_PATH = os.path.join("json", FILE_NAME)

    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

def main():
    # Configure command-line argument parsing with a help message
    parser = argparse.ArgumentParser(description='Process command-line arguments for ticket information.')
    
    # Add the "--t" argument, expecting a ticket as the second parameter
    parser.add_argument('--t', dest='ticket', help='Specify a ticket.')
    
    parser.add_argument('--f', dest='frequency', help='Specify a frequency.', default='w')

    # Parse command-line arguments
    args = parser.parse_args()

    # Check if the "--t" argument and the second parameter are provided
    if args.ticket:
        if args.frequency:
            print_content(args.ticket + "_" + args.frequency)
            save(args.ticket + "_" + args.frequency, get_data(args.ticket, args.frequency))
        else:
            print_content(args.ticket)
            save(args.ticket, get_data(args.ticket))
    else:
        # If "--t" or the second parameter is missing, show the help message
        parser.print_help()

if __name__ == "__main__":
    main()
