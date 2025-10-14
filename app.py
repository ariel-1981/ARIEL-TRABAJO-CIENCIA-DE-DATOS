import streamlit as st
import pandas as pd

# Crear datos de ejemplo
data = {
    "id_ejercicio": [1, 2, 3, 4],
    "ejercicio": ["Sentadilla", "Press de banca", "Peso muerto", "Plancha"],
    "grupo muscular": ["Piernas", "Pecho", "Espalda", "Abdominales"],
    "objetivo": ["Fuerza", "Hipertrofia", "Fuerza", "Resistencia"],
    "duracion": [60, 45, 90, 120]  # segundos o minutos, según tu necesidad
}

# Crear el DataFrame
df_ejercicios = pd.DataFrame(data)

# Mostrar el DataFrame en Streamlit
st.title("Tabla de Ejercicios")
st.dataframe(df_ejercicios)
