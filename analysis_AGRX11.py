import pandas as pd
import json

def calculate_total(json_file, filter_date):
    # Leer el contenido del archivo JSON
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Convertir el diccionario en un DataFrame de Pandas
    df_time_series = pd.DataFrame(data["Weekly Adjusted Time Series"]).T

    # Convertir las columnas relevantes a tipos numéricos
    df_time_series["7. dividend amount"] = pd.to_numeric(df_time_series["7. dividend amount"], errors="coerce")
    df_time_series["4. close"] = pd.to_numeric(df_time_series["4. close"], errors="coerce")

    # Convertir el índice (fechas) a tipo datetime
    df_time_series.index = pd.to_datetime(df_time_series.index)

    # Filtrar por fecha
    df_filtered = df_time_series[df_time_series.index >= filter_date]
    
    # Ordenar por fecha en orden ascendente
    df_sorted = df_filtered.sort_index()

    # Inicializar la variable 'total'
    total = 0
    cant = 0
    dividend_sum = df_sorted["7. dividend amount"].sum()

    # Iterar sobre las filas y actualizar la variable 'total'
    for i in range(len(df_sorted)):
        close_value = df_sorted.iloc[i]["4. close"]
        dividend_amount = df_sorted.iloc[i]["7. dividend amount"]

        # Sumar el valor de "4. close" cuando "7. dividend amount" es mayor que 0
        if dividend_amount > 0:
            total += close_value
            cant +=1
            print(f"Sub-Total: {total} -> Venta: {close_value}")
            
            # Restar el valor de "4. close" del elemento que representa 2 semanas después
            if i + 2 < (len(df_sorted) - 1):
                compra = df_sorted.iloc[i + 2]["4. close"]
                total -= compra
                print(f"Sub-Total: {total} -> Compra: {compra}")

    print("----------")
    print("Cantidad:", cant)
    print("Total:", total)
    print("Dividend Amount Sum:", dividend_sum)

if __name__ == "__main__":
    json_file = "AGRX11.json"  # Reemplaza con el nombre de tu archivo JSON
    #filter_date = "2022-08-12"
    filter_date = "2023-03-10"
    calculate_total(json_file, filter_date)