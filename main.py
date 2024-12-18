# Importar librerias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
data = pd.read_csv('Renewable_Energy.csv')

# Agrupa los datos por Energy_Type, quédate con los valores que sean Total Renewable y sumalos
data = data.groupby('Energy_Type').get_group('Total Renewable')

# Encabezado
st.header('Proyecto de Energias Renovables')

# Título
st.title('Renewable Energy')

# Subtítulo
st.write('Datos de energias renovables')

# Mostrar datos
st.write(data)

st.write('Hello world!')