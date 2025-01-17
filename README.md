# Proyecto de Visualización de Datos de Energías Renovables y Combustibles Fósiles

Este proyecto forma parte del trabajo final de la asignatura **Visualización, Procesamiento y Almacenamiento de Datos**.
El proyecto consiste en una aplicación interactiva para analizar y visualizar datos energéticos globales.

Desarrollado por **Carmen Linares Vázquez**, **María Millán Gordillo** y **Pablo Téllez López**.

---

## Descripción

El proyecto permite explorar la generación de energía eléctrica en función de fuentes renovables y no renovables a nivel global, así como comparar tendencias entre países y analizar la situación de la Unión Europea.

La aplicación incluye diferentes secciones para **Generación de energía a lo largo de los años**, **Comparativas**, **Energía en la Unión Europea** y un **Mapa de energía interactivo** para visualizar la generación eléctrica a nivel global.

---

## Ejecución

Para ejecutar la aplicación, usar el siguiente comando:

```bash
streamlit run main.py
```

---

## Dataset

El conjunto de datos utilizado proviene de [Kaggle: Global Energy Generation & Capacity (IMF)](https://www.kaggle.com/datasets/pinuto/global-energy-generation-and-capacity-imf). Contiene información sobre:

- Generación de energía (GWh) por país.
- Tecnologías utilizadas (hidroeléctrica, combustibles fósiles, solar, eólica, etc.).
- Capacidad instalada por país y tecnología.
- Datos anuales desde el año 2000 hasta 2022.

---

## Estructura del Proyecto

El código se organiza en un archivo principal:

- **`main.py`**: Contiene la aplicación principal de Streamlit.

Otros archivos:

- **`requirements.txt`**: Lista de dependencias y librerías necesarias para ejecutar el proyecto.
- **`imagen_introduccion.webp`**: Imagen utilizada en la interfaz de la aplicación.

---

## Funcionalidades

### 1. Generación de energía a lo largo de los años

- Selecciona un país y una tecnología específica para visualizar los datos.
- Elige un rango de años para analizar tendencias.
- Analiza la energía generada en función de la fuenta.
- Muestra la capacidad instalada de energías renovables.

### 2. Comparativas

- Compara países seleccionados.
- Analiza tipos de energía renovable, no renovable o el total.
- Representa comparaciones porcentuales entre la generación y la capacidad instalada por tecnología.

### 3. Energía en la Unión Europea

- Filtra datos por países de la Unión Europea.
- Visualiza la distribución porcentual entre los países.
- Analiza tecnologías específicas o el total.

### 4. Mapa de Energía Interactivo

- Representa la generación de energía eléctrica por país en un mapa global.
- Permite filtrar por tipo de energía y seleccionar un año específico.
- Incluye una escala de colores para facilitar la interpretación visual de los datos.

---

## Autores

- **Carmen Linares Vázquez**
- **María Millán Gordillo**
- **Pablo Téllez López**
