import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Gestión de Ejercicios", layout="centered")

# --- Función para crear el DataFrame base ---
def get_default_df():
    return pd.DataFrame({
        "id_ejercicio": [1, 2, 3, 4],
        "ejercicio": ["Sentadilla", "Press de banca", "Peso muerto", "Plancha"],
        "grupo muscular": ["Piernas", "Pecho", "Espalda", "Abdominales"],
        "objetivo": ["Fuerza", "Hipertrofia", "Fuerza", "Resistencia"],
        "duracion": [60, 45, 90, 120]
    })

# --- Cargar o inicializar el DataFrame ---
if "df_ejercicios" not in st.session_state:
    st.session_state.df_ejercicios = get_default_df()

df = st.session_state.df_ejercicios

st.title("🏋️ Gestión de Ejercicios")

# --- Mostrar DataFrame actual ---
st.subheader("📋 Lista de ejercicios")
st.dataframe(df, use_container_width=True)

# --- Formulario para agregar ejercicio ---
st.subheader("➕ Agregar nuevo ejercicio")

with st.form("form_ejercicio"):
    ejercicio = st.text_input("Nombre del ejercicio")
    grupo = st.selectbox("Grupo muscular", ["Piernas", "Pecho", "Espalda", "Hombros", "Bíceps", "Tríceps", "Abdominales", "Glúteos"])
    objetivo = st.selectbox("Objetivo", ["Fuerza", "Hipertrofia", "Resistencia", "Rehabilitación"])
    duracion = st.number_input("Duración (en segundos)", min_value=10, max_value=600, step=5)
    
    submitted = st.form_submit_button("Agregar")

    if submitted:
        nuevo_id = df["id_ejercicio"].max() + 1 if not df.empty else 1
        nuevo_ejercicio = {
            "id_ejercicio": nuevo_id,
            "ejercicio": ejercicio,
            "grupo muscular": grupo,
            "objetivo": objetivo,
            "duracion": duracion
        }
        st.session_state.df_ejercicios = pd.concat([df, pd.DataFrame([nuevo_ejercicio])], ignore_index=True)
        st.success(f"Ejercicio '{ejercicio}' agregado con éxito.")

# --- Botón para descargar Excel ---
st.subheader("⬇️ Descargar en Excel")

def descargar_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Ejercicios")
    output.seek(0)
    return output

excel_data = descargar_excel(st.session_state.df_ejercicios)

st.download_button(
    label="📥 Descargar Excel",
    data=excel_data,
    file_name="ejercicios.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
