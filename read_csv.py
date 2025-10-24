import pandas as pd

# Leer el archivo CSV en un DataFrame
df = pd.read_csv('list_1_2_4.csv')
df2 = pd.read_csv('list_2_4.csv')
df1 = pd.read_csv('list_1_3.csv')

# Mostrar el contenido en forma de tabla
print(df)
print(df2)
print(df1)
