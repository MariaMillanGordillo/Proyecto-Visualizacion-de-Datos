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

# Encabezado
st.header('Proyecto de Energias Renovables')

# Título
st.title('Renewable Energy')

# Subtítulo
st.write('Datos de energias renovables')

# Mostrar datos
st.write(data)

# Seleccionar un rango de años
years = st.slider('Años', 2000, 2023, (2000, 2023))

# Seleccionar tecnologías a incluir
technology_options = data['Technology'].unique()
selected_technologies = st.multiselect('Seleccionar Tecnologías a Incluir', technology_options, default=technology_options)

# Filtrar las columnas por el rango de años seleccionado
selected_columns = [f'F{year}' for year in range(years[0], years[1] + 1)]
filtered_data = data[data['Technology'].isin(selected_technologies)][['Technology'] + selected_columns]

# Agrupar los datos por tecnología y sumar los valores totales para el rango de años seleccionado
technology_distribution = filtered_data.groupby('Technology').sum()

# Sumar los valores totales por tecnología a través de los años
technology_distribution['Total'] = technology_distribution.sum(axis=1)
technology_distribution = technology_distribution.sort_values(by='Total', ascending=False)

# Crear el gráfico de barras
st.subheader(f'Cantidad de Energía Generada por Tecnología ({years[0]}-{years[1]})')
fig, ax = plt.subplots(figsize=(12, 8))
technology_distribution['Total'].plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)

# Personalizar el gráfico
ax.set_title(f"Cantidad Total de Energía Generada por Tecnología ({years[0]}-{years[1]})", fontsize=14)
ax.set_xlabel("Tecnología", fontsize=12)
ax.set_ylabel("Cantidad Total de Energía (GWh)", fontsize=12)
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)