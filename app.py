import streamlit as st
#Streamlit es una Libreria de Python para hacer Dashboards
#Los Dashboards son Tableros de mando donde vemos los datos por ejemplo: en forma de Graficos, Tablas o KPIs
import pandas as pd
#Pandas es una Libreria de Python para trabajar con datos de manera eficiente y estructurada
from io import StringIO
#sirve para tratar una cadena de texto como un archivo

st.set_page_config(page_title="Gestion de Ejercicios", layout="centered")
#set_page_config sirve para configurar el titulo de la aplicacion web, en este caso le pusimos 'Gestion de Ejercicios'


st.title("🏋️😇😇😇😇😇😇😇")
#st.title sirve para poner un texto en forma de Titulo en este caso pusimos 'Gestion de ejercicios con CSV'

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
        # Crear estructura vacía
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

with st.form("form_agregar"):
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
        st.success(f"✅ Ejercicio '{ejercicio}' agregado con éxito.")

# --- Formulario para modificar ejercicios ---
st.subheader("✏️ Modificar ejercicio existente")

if not df.empty:
    ids_disponibles = df["id_ejercicio"].tolist()
    id_modificar = st.selectbox("Selecciona el ID del ejercicio a modificar", ids_disponibles)

    ejercicio_seleccionado = df[df["id_ejercicio"] == id_modificar].iloc[0]

    with st.form("form_modificar"):
        nuevo_nombre = st.text_input("Nombre del ejercicio", value=ejercicio_seleccionado["ejercicio"])
        nuevo_grupo = st.selectbox("Grupo muscular", ["Piernas", "Pecho", "Espalda", "Hombros", "Bíceps", "Tríceps", "Abdominales", "Glúteos"], index=["Piernas", "Pecho", "Espalda", "Hombros", "Bíceps", "Tríceps", "Abdominales", "Glúteos"].index(ejercicio_seleccionado["grupo muscular"]))
        nuevo_objetivo = st.selectbox("Objetivo", ["Fuerza", "Hipertrofia", "Resistencia", "Rehabilitación"], index=["Fuerza", "Hipertrofia", "Resistencia", "Rehabilitación"].index(ejercicio_seleccionado["objetivo"]))
        nueva_duracion = st.number_input("Duración (en segundos)", min_value=10, max_value=600, step=5, value=int(ejercicio_seleccionado["duracion"]))
        
        modificado = st.form_submit_button("Guardar cambios")

        if modificado:
            idx = df[df["id_ejercicio"] == id_modificar].index[0]
            st.session_state.df_ejercicios.at[idx, "ejercicio"] = nuevo_nombre
            st.session_state.df_ejercicios.at[idx, "grupo muscular"] = nuevo_grupo
            st.session_state.df_ejercicios.at[idx, "objetivo"] = nuevo_objetivo
            st.session_state.df_ejercicios.at[idx, "duracion"] = nueva_duracion
            st.success(f"✅ Ejercicio con ID {id_modificar} modificado correctamente.")
else:
    st.info("Primero debes cargar o agregar ejercicios para modificarlos.")

# --- Descargar CSV ---
st.subheader("⬇️ Descargar datos como CSV")

csv_data = st.session_state.df_ejercicios.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Descargar CSV",
    data=csv_data,
    file_name="ejercicios_actualizados.csv",
    mime="text/csv"
)


