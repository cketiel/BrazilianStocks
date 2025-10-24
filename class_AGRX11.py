import pandas as pd
import json
import math

class AGRX11:
    json_file = "AGRX11.json"  
    filter_date = "2023-03-17"
    def __init__(self, initial_balance = 1000.0000) -> None:
        self.initial_balance = initial_balance
        try:
            with open(AGRX11.json_file, 'r') as file:
                data = json.load(file)
                self.data = data
                self.time_series = pd.DataFrame(data["Weekly Adjusted Time Series"]).T
                # Convertir el diccionario en un DataFrame de Pandas
                df_time_series = pd.DataFrame(data["Weekly Adjusted Time Series"]).T

                # Convertir las columnas relevantes a tipos numéricos
                df_time_series["7. dividend amount"] = pd.to_numeric(df_time_series["7. dividend amount"], errors="coerce")
                df_time_series["4. close"] = pd.to_numeric(df_time_series["4. close"], errors="coerce")

                # Convertir el índice (fechas) a tipo datetime
                df_time_series.index = pd.to_datetime(df_time_series.index)

                # Filtrar por fecha
                df_filtered = df_time_series[df_time_series.index >= AGRX11.filter_date]
                
                # Ordenar por fecha en orden ascendente
                df_sorted = df_filtered.sort_index()
                self.df_sorted = df_sorted
               
        except FileNotFoundError:
            Log.error("Config file not found. Ensure a properly formatted 'config.json' file exists in the root directory.")
            sys.exit()

    
    def history(self):
        #initial_balance = 1000.0000
        initial_balance = self.initial_balance
        balance = initial_balance
        only_first_time = True
        cant_agrx11 = 0
        cant_ncra11 = 0
        dividend_agrx11 = 0
        dividend_ncra11 = 0
        total = 0
        cant = 0

        df_sorted = self.df_sorted
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
                    print(f"Inicio(Compra Inicial AGRX11) - Balance: {balance} AGRX11={cant_ncra11}")
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
                print(f"Recompra de {int_part} cuotas - Balance: {balance} AGRX11={cant_ncra11} Proventos = {dividend}")
                

        print("----------")
        print(f"FII: AGRX11 Cantidad de Meses({cant})")
        saldo_final = balance + cant_ncra11 * close_value #+ cant_agrx11 * price
        total_dividend = dividend_ncra11 #+ dividend_agrx11
        ganancia = saldo_final - initial_balance
        porciento = ganancia * 100 / initial_balance
        porciento = round(porciento, 2) # print("{:.2f}".format(porciento))
        trading = ganancia - total_dividend
        
        print("Saldo inicial:", initial_balance)
        
        print("Saldo final:", saldo_final)
        print("Ganancia:", ganancia)
        print("% respecto a Saldo Inicial:", porciento)
        
        print("Total dividendo:", total_dividend)
        print("Trading:", trading)
        print("----------")
        
        return ganancia