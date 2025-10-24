import pandas as pd
import json
import math

def get_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def get_price(data, target_date):
    

    # Convertir el diccionario en un DataFrame de Pandas
    df_time_series = pd.DataFrame(data["Weekly Adjusted Time Series"]).T

    # Convertir las columnas relevantes a tipos numéricos
    df_time_series["4. close"] = pd.to_numeric(df_time_series["4. close"], errors="coerce")

    # Convertir el índice (fechas) a tipo datetime
    df_time_series.index = pd.to_datetime(df_time_series.index)

    # Obtener el valor de "4. close" para la fecha deseada
    try:
        close_value = df_time_series.loc[target_date, "4. close"]
        return close_value
    except KeyError:
        print(f"No data available for the date {target_date}")
        return None
        
def get_date_value(data, filter_date):
    result = [None, None, None]
    
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
    
    for i in range(6):
        close_value = df_sorted.iloc[i]["4. close"]
        dividend_amount = df_sorted.iloc[i]["7. dividend amount"]
        
        # Sumar el valor de "4. close" cuando "7. dividend amount" es mayor que 0
        if dividend_amount > 0:
            target_date = df_sorted.index[i]
            result[0] = target_date
            result[1] = close_value
            result[2] = dividend_amount
            return result
            

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


    initial_balance = 1000.0000
    balance = initial_balance
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
                print(f"Inicio(Compra Inicial NCRA11) - Balance: {balance} AGRX11={cant_agrx11} NCRA11={cant_ncra11}")
            total += close_value
            cant +=1
            #print(f"Sub-Total: {total} -> Venta: {close_value}")
            
            balance = balance + cant_ncra11 * close_value + dividend_amount * cant_ncra11
            dividend_ncra11 += (dividend_amount * cant_ncra11)
            
            print(f"Venta NCRA11 - Balance = {balance} -> ({cant_ncra11} * {close_value} + {dividend_amount * cant_ncra11}) Cantidad * Precio + Provento")
            cant_ncra11 = 0
            
            target_date = df_sorted.index[i]
            data = get_data("AGRX11.json")
            price = get_price(data, target_date)
            div = balance/price
            decimal_part, int_part = math.modf(div)
            cant_agrx11 = int_part
            balance = decimal_part * price
            
            print(f"Compra de {cant_agrx11} AGRX11 a {price} -> Balance = {balance}")
            
            # Venta AGRX11
            arr_date_value = get_date_value(data, target_date)
            date = arr_date_value[0]
            value = arr_date_value[1]
            dividend = arr_date_value[2]
            balance = balance + cant_agrx11 * value + dividend * cant_agrx11
            dividend_agrx11 += (dividend * cant_agrx11)
            
            print(f"Venta AGRX11 - Balance = {balance} -> ({cant_agrx11} * {value} + {dividend * cant_agrx11}) Cantidad * Precio + Provento")
            cant_agrx11 = 0
            
            # Compra NCRA11
            target_date = date
            data = get_data("ncra11.json")
            price = get_price(data, target_date)
            div = balance/price
            decimal_part, int_part = math.modf(div)
            cant_ncra11 = int_part
            balance = decimal_part * price
            
            print(f"Compra de {cant_ncra11} NCRA11 a {price} -> Balance = {balance}")
            

    print("----------")
    print("Meses:", cant)
    #print("Total:", total)
    
    saldo_final = balance + cant_ncra11 * close_value + cant_agrx11 * price
    total_dividend = dividend_ncra11 + dividend_agrx11
    ganancia = saldo_final - initial_balance
    porciento = ganancia * 100 / initial_balance
    trading = ganancia - total_dividend
    
    print("Saldo inicial:", initial_balance)
    
    print("Saldo final:", saldo_final)
    print("Ganancia:", ganancia)
    print("% respecto a Saldo Inicial:", porciento)
    print("Total dividendo:", total_dividend)
    print("Trading:", trading)
    
    print("----------")
    print("Dividend AGRX11:", dividend_agrx11)
    print("Dividend NCRA11:", dividend_ncra11)
    
    print("Dividend Amount Sum:", dividend_sum)

if __name__ == "__main__":
    json_file = "ncra11.json"  # Reemplaza con el nombre de tu archivo JSON
    filter_date = "2023-03-17"
    calculate_total(json_file, filter_date)