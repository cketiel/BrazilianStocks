import pandas as pd
import json
import math

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


    balance = 10000.0000
    only_first_time = True
    cant_agrx11 = 0
    cant_ncra11 = 0
    dividend_agrx11 = 0
    dividend_ncra11 = 0
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
            div = balance/close_value
            if only_first_time == True:
                decimal_part, int_part = math.modf(div)
                cant_ncra11 = int_part
                balance = decimal_part * close_value
                only_first_time = False
                print(f"Inicio(Compra Inicial NCRA11) - Balance: {balance} NCRA11={cant_ncra11}")
            total += close_value
            cant +=1
            
            dividend = dividend_amount * cant_ncra11
            balance = balance + dividend
            dividend_ncra11 += dividend
            
            # Recompra
            div = balance/close_value
            decimal_part, int_part = math.modf(div)
            cant_ncra11 += int_part
            balance = decimal_part * close_value
            print(f"Recompra de {int_part} cuotas - Balance: {balance} NCRA11={cant_ncra11} Proventos = {dividend}")
            

    print("----------")
    print("Cantidad:", cant)
    print("Dividend NCRA11:", dividend_ncra11)
    
    print("Dividend Amount Sum:", dividend_sum)

if __name__ == "__main__":
    json_file = "ncra11.json"  # Reemplaza con el nombre de tu archivo JSON
    filter_date = "2023-03-17"
    calculate_total(json_file, filter_date)