from class_LIFE11 import LIFE11
from class_VGIA11 import VGIA11

if __name__ == "__main__":
    print("*** History *** \n")
    # 1000 * 2
    initial_balance = 1000.0000
    
    life11 = LIFE11(initial_balance)
    ganancia_life11 = life11.history()
    
    vgia11 = VGIA11(initial_balance)
    ganancia_vgia11 = vgia11.history()
    
    ganancia = ganancia_life11 + ganancia_vgia11
    saldo_final = initial_balance * 2 + ganancia
    porciento = ganancia * 100 / (initial_balance * 2)
    
    print(f"Saldo inicial: {initial_balance * 2} - LIFE11 = {initial_balance} VGIA11 = {initial_balance}")
    print(f"Saldo Final: {saldo_final} = {initial_balance * 2} + {ganancia_life11}(LIFE11) + {ganancia_vgia11} (VGIA11)")
    print("{:.2f} %".format(porciento))