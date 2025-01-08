import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
data = pd.read_csv('Renewable_Energy.csv')

# Título
st.title('Proyecto de Energías Renovables')

# Seleccionar un rango de años
years = st.slider('Años', 2000, 2023, (2000, 2023))

# Crear dos columnas para la selección de tipo de energía y países
col1, col2 = st.columns(2)

with col1:
    # Seleccionar tipo de energía usando segmented control
    energy_type_options = ['Renovable', 'No Renovable', 'Total']
    selected_energy_type = st.segmented_control(
        'Seleccionar Tipo de Energía',
        options=energy_type_options,
        default='Total'
    )

with col2:
    # Seleccionar países usando multiselect
    country_options = data['Country'].unique()
    selected_countries = st.multiselect(
        'Seleccionar Países',
        options=country_options,
        default=['Spain', 'France', 'Portugal']
    )

# Filtrar las columnas por el rango de años seleccionado
selected_columns = [f'F{year}' for year in range(years[0], years[1] + 1)]

# Filtrar por tipo de energía
if selected_energy_type == 'Renovable':
    filtered_data = data[data['Energy_Type'] == 'Total Renewable']
elif selected_energy_type == 'No Renovable':
    filtered_data = data[data['Energy_Type'] == 'Total Non-Renewable']
else:
    filtered_data = data

# Crear el gráfico de líneas
st.subheader(f'Evolución de la Energía {selected_energy_type} Generada ({years[0]}-{years[1]})')

fig, ax = plt.subplots(figsize=(12, 8))

# Graficar una línea para cada país seleccionado
for country in selected_countries:
    country_data = filtered_data[filtered_data['Country'] == country]
    aggregated_data = country_data[selected_columns].sum().T
    years_index = [int(col[1:]) for col in aggregated_data.index]  # Convertir nombres de columnas a años
    ax.plot(
        years_index,
        aggregated_data.values,
        label=f"{country}"
    )

# Personalizar el gráfico
ax.set_title(f"Evolución de la Energía {selected_energy_type} Generada ({years[0]}-{years[1]})", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Cantidad de Energía (GWh)", fontsize=12)
ax.legend(title="País")
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)
