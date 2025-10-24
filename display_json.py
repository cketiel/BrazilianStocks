import json
from tabulate import tabulate  

def read_json_and_display_content(json_file):
    # Leer el contenido del archivo JSON
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extraer la información relevante del JSON
    meta_data = data.get("Meta Data", {})
    time_series = data.get("Weekly Adjusted Time Series", {})

    # Mostrar la información de Meta Data de forma tabulada
    print("Meta Data:")
    meta_data_table = [[key, meta_data[key]] for key in meta_data]
    print(tabulate(meta_data_table, headers=["Key", "Value"], tablefmt="grid"))

    # Mostrar la información de Weekly Adjusted Time Series de forma tabulada
    print("\nWeekly Adjusted Time Series:")
    time_series_table = []
    for date in time_series:
        row = [date]
        for col in time_series[date]:
            row.append(time_series[date].get(col, 'N/A'))
        
        time_series_table.append(row)
        
    # en una sola linea de codigo   
    time_series_table2 = [[date] + [time_series[date][col] for col in time_series[date]] for date in time_series]
    
    # primer elemento del diccionario
    [d, values] = first_element = next(iter(time_series.items()))
    
    headers = ["Date"] + [col for col in values]
    print(tabulate(time_series_table2, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    json_file = "ncra11.json"  # Reemplaza con el nombre de tu archivo JSON
    read_json_and_display_content(json_file)