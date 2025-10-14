import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Gestión de Ejercicios", layout="centered")

st.title("🏋️ Gestión de Ejercicios con CSV")

# --- Cargar CSV desde el usuario ---
st.subheader("📂 Cargar archivo CSV")

uploaded_file = st.file_uploader("Selecciona un archivo CSV", type="csv")

if "df_ejercicios" not in st.session_state:
    if uploaded_file is not None:
        try:
            st.session_state.df_ejercicios = pd.read_csv(uploaded_file)
            st.success("✅ CSV cargado correctamente.")
        except Exception as e:
            st.error(f"❌ Error al leer el archivo: {e}")
            st.session_state.df_ejercicios = pd.DataFrame()
    else:
        # Cargar DataFrame por defecto si no se sube archivo
        st.session_state.df_ejercicios = pd.DataFrame(columns=[
            "id_ejercicio", "ejercicio", "grupo muscular", "objetivo", "duracion"
        ])

df = st.session_state.df_ejercicios

# --- Mostrar tabla actual ---
st.subheader("📋 Lista de ejercicios")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No hay datos cargados todavía.")

# --- Formulario para agregar ejercicios ---
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
        st.session_state.df_ejercicios = pd.concat(
            [df, pd.DataFrame([nuevo_ejercicio])],
            ignore_index=True
        )
        st.success(f"Ejercicio '{ejercicio}' agregado con éxito.")

# --- Descargar CSV ---
st.subheader("⬇️ Descargar datos como CSV")

csv_data = st.session_state.df_ejercicios.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Descargar CSV",
    data=csv_data,
    file_name="ejercicios.csv",
    mime="text/csv"
)

