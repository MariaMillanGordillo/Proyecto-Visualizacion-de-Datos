# Importar librerias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
data = pd.read_csv('Renewable_Energy.csv')

# Encabezado
st.header('Proyecto de Energias Renovables')

# Título
st.title('Renewable Energy')

# Subtítulo
st.write('Datos de energias renovables')

# Mostrar datos
st.write(data)

# Agrupar los datos por tecnología y sumar los valores totales para todos los años
technology_distribution = data.groupby('Technology')[['F2000', 'F2001', 'F2002', 'F2003', 'F2004', 'F2005',
                                                       'F2006', 'F2007', 'F2008', 'F2009', 'F2010', 'F2011',
                                                       'F2012', 'F2013', 'F2014', 'F2015', 'F2016', 'F2017',
                                                       'F2018', 'F2019', 'F2020', 'F2021', 'F2022', 'F2023']].sum()

# Sumar los valores totales por tecnología a través de los años
technology_distribution['Total'] = technology_distribution.sum(axis=1)
technology_distribution = technology_distribution.sort_values(by='Total', ascending=False)

# Crear el gráfico de barras
st.subheader('Cantidad de Energía Generada por Tecnología (2000-2023)')
fig, ax = plt.subplots(figsize=(12, 8))
technology_distribution['Total'].plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)

# Personalizar el gráfico
ax.set_title("Cantidad Total de Energía Generada por Tecnología (2000-2023)", fontsize=14)
ax.set_xlabel("Tecnología", fontsize=12)
ax.set_ylabel("Cantidad Total de Energía (GWh)", fontsize=12)
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)


