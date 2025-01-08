# Importar librerias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
data = pd.read_csv('Renewable_Energy.csv')

# Dividir el dataset en dos según la columna 'Indicator'
grouped_data = data.groupby('Indicator')

# Crear dos datasets separados
generation = grouped_data.get_group('Electricity Generation')
capacity = grouped_data.get_group('Electricity Installed Capacity')

# Eliminar las columnas especificadas de ambos datasets
columns_to_drop = ['Source', 'CTS_Name', 'CTS_Code', 'CTS_Full_Descriptor', 'Indicator']
generation.drop(columns=columns_to_drop, inplace=True)
capacity.drop(columns=columns_to_drop, inplace=True)

# Crear un desplegable en Streamlit para seleccionar el país
st.subheader('Generación de energía por territorio según el tipo de energía')
paises = data['Country'].unique().tolist()
pais_seleccionado = st.selectbox('Selecciona un país', paises)

# Filtrar los datos para el país seleccionado
datos_pais = generation[generation['Country'] == pais_seleccionado]

# Seleccionar el rango de años
years = [f'F{year}' for year in range(2000, 2023)]
year_range = st.slider('Selecciona el rango de años', 2000, 2022, (2000, 2022))
years_selected = [f'F{year}' for year in range(year_range[0], year_range[1] + 1)]

# Generar gráficos en Streamlit
for _, fila in datos_pais.iterrows():
    energia = fila[years_selected]
    tecnologia = fila['Technology']
    st.write(f'Electricity Generation (GWh) in {pais_seleccionado} - {tecnologia}')
    st.bar_chart(energia)
    





