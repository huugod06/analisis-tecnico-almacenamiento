import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuración de la app
st.set_page_config(page_title="Análisis Técnico - Almacenamiento", layout="wide")

# --- Cargar datos ---
DATA_PATH = Path("data/tech_comparison.csv")
df = pd.read_csv(DATA_PATH)

# --- 1. Escenario ---
st.title("📑 Análisis Técnico de Soluciones de Almacenamiento")
st.header("1. Descripción del Escenario")
st.markdown("""
La empresa cliente presenta **problemas en su infraestructura actual**:
- Lentitud en el acceso a los datos.
- Dificultad para escalar con el crecimiento.
- Costes de mantenimiento elevados.

El objetivo es comparar diferentes tecnologías (HDD, SSD, Cintas y Nube) 
y proponer una solución híbrida que combine rendimiento, coste y escalabilidad.
""")

# --- 2. Criterios ---
st.header("2. Criterios de Evaluación")
criterios = [
    "Velocidad de Lectura/Escritura",
    "Capacidad Total",
    "Costo por GB",
    "Fiabilidad (MTBF)",
    "Consumo Energético",
    "Seguridad (Cifrado)",
    "Escalabilidad"
]
for c in criterios:
    st.checkbox(c, value=True)

# --- 3. Comparación ---
st.header("3. Comparación de Tecnologías")
st.dataframe(df)

# --- Métricas derivadas ---
df["Cost_per_TB_USD"] = df["Cost_per_GB_USD"] * 1000
df["Estimated_Annual_Cost_USD"] = df["Capacity_TB"] * df["Cost_per_TB_USD"] + df["Annual_maintenance_USD"]
st.subheader("Métricas Derivadas")
st.dataframe(df[["Technology","Cost_per_TB_USD","Estimated_Annual_Cost_USD"]])

# --- 4. Gráficos comparativos ---
st.header("4. Análisis Gráfico Comparativo")

# Velocidades
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=df["Technology"], y=df["Read_MBps"], name="Lectura"))
fig1.add_trace(go.Bar(x=df["Technology"], y=df["Write_MBps"], name="Escritura"))
fig1.update_layout(barmode="group", title="Velocidad de Lectura/Escritura")
st.plotly_chart(fig1, use_container_width=True)

# Radar: Fiabilidad, Seguridad, Escalabilidad
fig2 = go.Figure()
for i, row in df.iterrows():
    fig2.add_trace(go.Scatterpolar(
        r=[row["MTBF_hours"]/df["MTBF_hours"].max()*5, row["Security_score"], row["Scalability_score"]],
        theta=["Fiabilidad","Seguridad","Escalabilidad"],
        fill="toself",
        name=row["Technology"]
    ))
fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,5])))
st.plotly_chart(fig2, use_container_width=True)

# Costos
fig3 = px.bar(df, x="Technology", y="Estimated_Annual_Cost_USD", title="Coste Anual Estimado")
st.plotly_chart(fig3, use_container_width=True)

# --- 5. Conclusiones ---
st.header("Conclusiones Técnicas")
st.success("""
👉 Se recomienda una **solución híbrida**:
- **SSD** para cargas críticas.
- **HDD** para datos de uso frecuente.
- **Cintas y Nube** para respaldo y escalabilidad.

Esta estrategia optimiza costes, mejora el rendimiento y asegura la continuidad del negocio.
""")
