import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# CARGAR DATOS
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

col1, col2 = st.columns([2, 1])

with col1:
    # Título y descripción
    st.title('Energías Renovables y Combustibles Fósiles')
    st.markdown(
        """
        Este proyecto analiza la generación de energía eléctrica en distintos territorios 
        y las fuentes renovables y no renovables que se utilizan.
        """
    )

with col2:
    # Imagen en la segunda columna
    st.image("imagen_introduccion.webp", width=200, caption="Energía sostenible")

# Diferentes páginas
opcion = st.sidebar.radio("Selecciona un tipo de visualización:", ["Energía a lo largo de los años", "Comparativas", "Energía en la UE", "Mapa de Energía"])

# GRAFICOS MARIA
if opcion == "Comparativas":
    # Seleccionar un rango de años
    years = st.slider('Años', 2000, 2022, (2000, 2022))

    # Crear dos columnas para la selección de tipo de energía y países
    col1, col2 = st.columns(2)

    with col1:
        # Seleccionar tipo de energía usando segmented control
        energy_type_options = ['Renovable', 'No Renovable', 'Total']
        selected_energy_type = st.segmented_control(
            'Seleccionar Tipo de Fuente',
            options=energy_type_options,
            default='Total'
        )

    with col2:
        # Seleccionar países usando multiselect
        country_options = generation['Country'].unique()
        selected_countries = st.multiselect(
            'Seleccionar Países',
            options=country_options,
            default=['Spain', 'France', 'Portugal']
        )

    # Filtrar las columnas por el rango de años seleccionado
    selected_columns = [f'F{year}' for year in range(years[0], years[1] + 1)]

    # Filtrar por tipo de energía
    if selected_energy_type == 'Renovable':
        filtered_data = generation[generation['Energy_Type'] == 'Total Renewable']
    elif selected_energy_type == 'No Renovable':
        filtered_data = generation[generation['Energy_Type'] == 'Total Non-Renewable']
    else:
        filtered_data = generation

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
            marker='o',
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

    # Grafico 2
    st.subheader('Comparación Porcentual entre las Fuentes de Energía')
    st.markdown(''' Se representa el porcentaje que supone cada fuente en 
                cuanto a la producción de energía y el porcentaje que supone la capacidad
                de su instalación''')
    
    # Crear un desplegable en Streamlit para seleccionar el país
    selected_country = st.selectbox('Seleccionar País', options=country_options, index=0)

    # Filtrar los datos para el país seleccionado
    filtered_generation = generation[generation['Country'] == selected_country]
    filtered_capacity = capacity[capacity['Country'] == selected_country]

    # Calcular el porcentaje de cada tipo de tecnología en el dataset generation para el país seleccionado
    filtered_generation['Total_Generation'] = filtered_generation[selected_columns].sum(axis=1)
    total_generation_country = filtered_generation['Total_Generation'].sum()
    generation_percentage_country = filtered_generation.groupby('Technology')['Total_Generation'].sum() / total_generation_country * 100

    # Calcular el porcentaje de cada tipo de tecnología en el dataset capacity para el país seleccionado
    filtered_capacity['Total_Capacity'] = filtered_capacity[selected_columns].sum(axis=1)
    total_capacity_country = filtered_capacity['Total_Capacity'].sum()
    capacity_percentage_country = filtered_capacity.groupby('Technology')['Total_Capacity'].sum() / total_capacity_country * 100

    # Crear un DataFrame con los porcentajes para el país seleccionado
    comparison_df_country = pd.DataFrame({
        'Technology': generation_percentage_country.index,
        'Generation_Percentage': generation_percentage_country.values,
        'Capacity_Percentage': capacity_percentage_country.values
    }).reset_index(drop=True)

    # Crear el gráfico de barras para el país seleccionado
    fig, ax = plt.subplots(figsize=(12, 8))
    comparison_df_country.plot(kind='bar', x='Technology', ax=ax)
    ax.set_title(f'Comparación de Porcentajes entre Generación y Capacidad por Tecnología en {selected_country}')
    ax.set_xlabel('Tecnología')
    ax.set_ylabel('Porcentaje (%)')
    ax.legend(['Generación', 'Capacidad'])
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    

#GRAFICO CARMEN

if opcion == 'Energía a lo largo de los años':

    # Crear un desplegable en Streamlit para seleccionar el país
    st.subheader('Generación de Energía Eléctrica por territorio')
    st.markdown(''' Los datos están representados a lo largo de los años y divididos según la
                fuente de energía o el total. ''')
    
    side1, side2 = st.columns(2)

    with side1:
        paises = data['Country'].unique().tolist()
        pais_seleccionado = st.selectbox('Seleccionar Territorio', paises)

    # Filtrar los datos para el país seleccionado
    datos_pais = generation[generation['Country'] == pais_seleccionado]

    with side2: 
        # Seleccionar la tecnologia
        tech = ["Todas"] + list(datos_pais['Technology'].dropna().unique())
        tech_selected = st.selectbox('Seleccionar Tipo de Fuente', options=tech)

    # Filtrar los datos para el país seleccionado
    datos_pais = generation[generation['Country'] == pais_seleccionado]

    # Seleccionar el rango de años
    year_range = st.slider('Seleccionar Rango de Años', 2000, 2022, (2000, 2022))
    years_selected = [f'F{year}' for year in range(year_range[0], year_range[1] + 1)]
    years_label = [year for year in range(year_range[0], year_range[1] + 1)]

    # Filtrar los datos para la tecnología seleccionada
    if tech_selected != "Todas":
        datos_pais_tech = datos_pais[datos_pais['Technology'] == tech_selected][years_selected]
        # Generar gráfico de barras para la tecnología seleccionada
        st.write(f'Generación de Energía Eléctrica en {pais_seleccionado} - {tech_selected}')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=datos_pais_tech, color='olivedrab')
        ax.set_ylim(datos_pais_tech.min().min() * 0.9, datos_pais_tech.max().max() * 1.1)
        ax.set_xticklabels(years_label, rotation=45)
        st.pyplot(fig)
    
    
    else: 
        st.write(f'Generación de Energía Eléctrica en {pais_seleccionado} - Total')
        datos_pais_tech = datos_pais[years_selected].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=datos_pais_tech, color='olivedrab')
        ax.set_ylim(datos_pais_tech.min().min() * 0.9, datos_pais_tech.max().max() * 1.1)
        ax.set_xticklabels(years_label, rotation=45)
        st.pyplot(fig)
    
    # Grafico total

    # Calcular el total de generación de energía para el rango de años seleccionado
    datos_pais['Total'] = datos_pais[years_selected].sum(axis=1)

    # Cambiar el nombre de la tecnología
    datos_pais['Technology'] = datos_pais['Technology'].replace('Hydropower (excl. Pumped Storage)', 'Hydropower')

    st.subheader(f'Total de Energía Generada en función de la Fuente')

    # Crear un checkbox para incluir o excluir la tecnología 'Fossil Fuels'
    incluir_fossil_fuels = st.checkbox('Incluir Combustibles Fósiles', value=True)

    # Filtrar los datos según la selección del checkbox
    if not incluir_fossil_fuels:
        datos_pais = datos_pais[datos_pais['Technology'] != 'Fossil fuels']

    # Calcular el porcentaje de cada tecnología
    datos_pais['Percentage'] = (datos_pais['Total'] / datos_pais['Total'].sum()) * 100


    # Crear dos columnas para los gráficos
    columna1, columna2 = st.columns([1,2])

    # Gráfico circular de porcentajes en la primera columna
    with columna1:
        st.markdown("#### Porcentual")
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(datos_pais['Percentage'], labels=datos_pais['Technology'], autopct='%1.1f%%', startangle=90, pctdistance=0.85, labeldistance=1.1, colors=sns.color_palette("Set3"))
        st.pyplot(fig)

    # Gráfico de barras con los totales en la segunda columna
    with columna2:
        st.markdown("#### Total")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=datos_pais, x='Technology', y='Total', color='red')
        ax.set_xlabel('Technology')
        ax.set_ylabel('Total (GWh)')
        ax.set_xticklabels(datos_pais['Technology'], rotation=45)
        st.pyplot(fig)

    # Grafica capacidad instalada 

    capacidad_pais = capacity[capacity['Country'] == pais_seleccionado]
    # Eliminar la tecnología 'Fossil fuels' de capacidad_pais
    capacidad_pais = capacidad_pais[capacidad_pais['Technology'] != 'Fossil fuels']

    # Sumar todas las columnas seleccionadas (years_selected)
    capacidad_pais_sum = capacidad_pais[years_selected].sum()

    # Crear una representación de la suma en función de los años
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=years_label, y=capacidad_pais_sum.values, marker='o', ax=ax, color='olivedrab')
    ax.set_title(f'Capacidad Instalada de Energías Renovables en {pais_seleccionado}')
    ax.set_xlabel('Año')
    ax.set_ylabel('Capacidad Instalada (MW)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)



#GRAFICO PABLO

if opcion == "Energía en la UE":

    # Crear gráfico de barras con st.bar_chart
    st.subheader(f"Distribución porcentual de la Generación de Energía Eléctrica en la UE (2000 - 2022)")

    # Lista de países de la Unión Europea
    eu_countries = [
        "Austria", "Belgium", "Bulgaria", "Croatia, Rep. of", "Cyprus", "Czech Rep.",
        "Denmark", "Estonia, Rep. of", "Finland", "France", "Germany", "Greece", "Hungary",
        "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands, The",
        "Poland, Rep. of", "Portugal", "Romania", "Slovak Rep.", "Slovenia, Rep. of", "Spain", "Sweden"
    ]

    # Filtrar datos para países de la UE
    eu_data = generation[generation['Country'].isin(eu_countries)]

    # Selección de países
    country_options = ["Todos"] + eu_countries
    selected_countries = st.multiselect('Seleccionar Países', options=country_options, default="Todos")

    # Selección de tecnología
    technology_options = ["Todas"] + list(generation['Technology'].dropna().unique())
    selected_technology = st.selectbox('Seleccionar Tipo de Fuente', options=technology_options)

    if selected_technology != "Todas":
        eu_data = eu_data[eu_data['Technology'] == selected_technology]

    # Selección de rango de años
    year_columns = [col for col in eu_data.columns if col.startswith('F')]
    years = [int(col[1:]) for col in year_columns]
    year_range = st.slider('Seleccionar Rango de Años', min_value=min(years), max_value=max(years) - 1, value=(min(years), max(years) - 1))
    selected_columns = [f'F{year}' for year in range(year_range[0], year_range[1] + 1)]

    # Calcular el total de generación de energía para los países de la UE en el rango de años seleccionado
    eu_data['Total_Generation'] = eu_data[selected_columns].sum(axis=1)
    total_generation_eu = eu_data['Total_Generation'].sum()

    # Calcular el porcentaje de cada país
    eu_data['Percentage'] = (eu_data['Total_Generation'] / total_generation_eu) * 100

    if "Todos" not in selected_countries:
        eu_data = eu_data[eu_data['Country'].isin(selected_countries)]

    # Ordenar por porcentaje
    eu_data_sorted = eu_data.sort_values(by='Percentage', ascending=False)

    # Preparar datos para st.bar_chart
    chart_data = eu_data_sorted[['Country', 'Percentage', 'Technology']]
    chart_data = chart_data.sort_values(by='Percentage', ascending=False)

    # Mostrar gráfico en Streamlit
    st.bar_chart(chart_data, x='Country', y='Percentage', color='Technology', use_container_width=True)

# MAPA PABLO

if opcion == "Mapa de Energía":

    # Configurar la página de Streamlit
    st.subheader("Mapa Interactivo de Generación de Electricidad por País")

    # Sección de filtros en la barra lateral
    st.sidebar.header("Filtros")

    # Crear un filtro para seleccionar el año (columnas que comienzan con "F"), eliminando la "F"
    year_options = {col: col[1:] for col in generation.columns if col.startswith("F") and col != "F2023"}  # Crear un diccionario sin incluir "F2023"
    year = st.sidebar.selectbox("Selecciona el año:", options=year_options.values())
    selected_year = [key for key, value in year_options.items() if value == year][0]  # Obtener la clave original con "F"

    # Crear un filtro para seleccionar el tipo de energía
    energy_type = st.sidebar.selectbox("Selecciona el tipo de energía:", generation["Energy_Type"].unique())

    # Filtrar datos según los criterios seleccionados y asegurarse de que la columna CTS_Name sea "Electricity Generation"
    filtered_data_map = generation[(generation["Energy_Type"] == energy_type)]

    # Verificar si hay datos disponibles después del filtrado
    if filtered_data_map.empty:
        # Mostrar un mensaje de advertencia si no hay datos
        st.warning("No hay datos disponibles para los filtros seleccionados.")
    else:
        # Preparar los datos para el mapa
        map_data = filtered_data_map.groupby(["Country", "ISO3"])[selected_year].sum().reset_index()  # Agrupar por país y sumar valores
        map_data = map_data.rename(columns={selected_year: "Electricity_Generation"})  # Renombrar la columna del año para claridad

        # Crear un mapa coroplético usando Plotly Express
        fig = px.choropleth(
            map_data,
            locations="ISO3",  # Código ISO de los países para ubicarlos en el mapa
            color="Electricity_Generation",  # Color según la generación de electricidad
            hover_name="Country",  # Nombre del país al pasar el ratón por encima
            color_continuous_scale="Viridis",  # Escala de colores continua
            title=f"Generación de Electricidad ({year}) - {energy_type}",  # Título dinámico del gráfico
            labels={"Electricity_Generation": "Generación (GWh)"},  # Etiqueta para la leyenda
        )

        # Personalizar la apariencia del mapa con un rango ajustado
        fig.update_coloraxes(cmin=0, cmax=map_data["Electricity_Generation"].quantile(0.9))  # Ajustar rango máximo al percentil 95

        # Personalizar la apariencia del mapa
        fig.update_geos(
            showcoastlines=True,  # Mostrar líneas costeras
            coastlinecolor="LightGray",  # Color de las líneas costeras
            showland=True,  # Mostrar la tierra
            landcolor="White"  # Color de la tierra
        )

        # Mostrar el gráfico en la aplicación
        st.plotly_chart(fig, use_container_width=True)

    # Mostrar una nota informativa para el usuario
    st.info("Selecciona diferentes filtros en el panel lateral para explorar los datos.")
