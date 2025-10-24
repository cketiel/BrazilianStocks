from class_NCRA11 import NCRA11
from class_AGRX11 import AGRX11

from class_LIFE11 import LIFE11

if __name__ == "__main__":
    print("*** History *** \n")
    # 1000 * 2
    initial_balance = 1000.0000
    
    ncra11 = NCRA11(initial_balance)
    ganancia_ncra11 = ncra11.history()
    
    agrx11 = AGRX11(initial_balance)
    ganancia_agrx11 = agrx11.history()
    
    ganancia = ganancia_ncra11 + ganancia_agrx11
    saldo_final = initial_balance * 2 + ganancia
    porciento = ganancia * 100 / (initial_balance * 2)
    
    print(f"Saldo inicial: {initial_balance * 2} - NCRA11 = {initial_balance} AGRX11 = {initial_balance}")
    print(f"Saldo Final: {saldo_final} = {initial_balance * 2} + {ganancia_ncra11}(NCRA11) + {ganancia_agrx11} (AGRX11)")
    print("{:.2f} %".format(porciento))
    
    
    
    life11 = LIFE11(initial_balance)
    ganancia_life11 = life11.history()