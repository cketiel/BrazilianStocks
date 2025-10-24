import pandas as pd
import json

def read_json_and_display_content(json_file):
    # Read the content of the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Convert the dictionary into Pandas DataFrames
    df_meta_data = pd.DataFrame(data["Meta Data"].items(), columns=["Key", "Value"])
    df_time_series = pd.DataFrame(data["Weekly Adjusted Time Series"]).T

    # Display Meta Data information on the screen
    print("Meta Data:")
    print(df_meta_data)

    # Display Weekly Adjusted Time Series information on the screen
    print("\nWeekly Adjusted Time Series:")
    print(df_time_series)

if __name__ == "__main__":
    json_file = "ncra11.json"  # Replace with the name of your JSON file
    read_json_and_display_content(json_file)