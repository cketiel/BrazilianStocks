import pandas as pd
import os

# Folder containing CSV files
csv_folder = "csv"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]

# Loop through each CSV file and display its content
for csv_file in csv_files:
    csv_path = os.path.join(csv_folder, csv_file)
    
    try:
        df = pd.read_csv(csv_path)
        print(f"\n===== Contents of {csv_file} =====")
        print(df)
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
