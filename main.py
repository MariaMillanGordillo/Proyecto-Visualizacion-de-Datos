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

# Seleccionar un rango de años
years = st.slider('Años', 2000, 2023, (2000, 2023))

# Seleccionar tipos de energía a incluir
energy_type_options = data['Energy_Type'].unique()
selected_energy_types = st.segmented_control('Seleccionar Tipos de Energía a Incluir', energy_type_options, selection_mode = 'multi', default=energy_type_options)

# Filtrar las columnas por el rango de años seleccionado
selected_columns = [f'F{year}' for year in range(years[0], years[1] + 1)]
filtered_data = data[data['Energy_Type'].isin(selected_energy_types)][['Energy_Type'] + selected_columns]

# Agrupar los datos por tipo de energía y sumar los valores totales para el rango de años seleccionado
energy_distribution = filtered_data.groupby('Energy_Type').sum()

# Sumar los valores totales por tipo de energía a través de los años
energy_distribution['Total'] = energy_distribution.sum(axis=1)
energy_distribution = energy_distribution.sort_values(by='Total', ascending=False)

# Crear el gráfico de barras
st.subheader(f'Cantidad de Energía Generada por Tipo de Energía ({years[0]}-{years[1]})')
fig, ax = plt.subplots(figsize=(12, 8))
energy_distribution['Total'].plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)

# Personalizar el gráfico
ax.set_title(f"Cantidad Total de Energía Generada por Tipo de Energía ({years[0]}-{years[1]})", fontsize=14)
ax.set_xlabel("Tipo de Energía", fontsize=12)
ax.set_ylabel("Cantidad Total de Energía (GWh)", fontsize=12)
ax.tick_params(axis='x', rotation=0, labelsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)