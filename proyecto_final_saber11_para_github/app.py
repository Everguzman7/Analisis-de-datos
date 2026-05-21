from pathlib import Path
import streamlit as st
import pandas as pd
import json
import plotly.express as px
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

BASE = Path(__file__).resolve().parent
OUT = BASE / "outputs"

st.set_page_config(page_title="Dashboard Saber 11", layout="wide")
st.title("Dashboard Saber 11 — Predicciones de puntaje alto")


@st.cache_data
def load_data():
    df = None
    metrics = {}
    csv_path = OUT / "muestra_predicciones.csv"
    json_path = OUT / "metricas_modelo.json"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                metrics = json.load(f)
        except Exception:
            metrics = {}
    return df, metrics


df, metrics = load_data()


if df is None:
    st.warning("No se encontró `outputs/muestra_predicciones.csv`. Coloca el CSV en `proyecto_final_saber11_para_github/outputs/` o ejecuta `train_model.py` para generarlo.")
else:
    # Sidebar: filtros
    st.sidebar.header("Filtros")
    # Período
    periodo_vals = sorted(df['PERIODO'].dropna().unique().tolist()) if 'PERIODO' in df.columns else []
    sel_periodo = st.sidebar.multiselect('Período', periodo_vals, default=periodo_vals)

    # Municipio: permitir elegir columna
    muni_cols = [c for c in ['ESTU_MCPIO_RESIDE','COLE_MCPIO_UBICACION'] if c in df.columns]
    muni_col = st.sidebar.selectbox('Columna municipio', muni_cols) if muni_cols else None
    sel_munis = []
    if muni_col:
        muni_vals = sorted(df[muni_col].dropna().unique().tolist())
        sel_munis = st.sidebar.multiselect('Municipios', muni_vals, default=muni_vals[:10])

    # Naturaleza colegio
    if 'COLE_NATURALEZA' in df.columns:
        nat_vals = sorted(df['COLE_NATURALEZA'].dropna().unique().tolist())
        sel_naturaleza = st.sidebar.multiselect('Naturaleza del colegio', nat_vals, default=nat_vals)
    else:
        sel_naturaleza = []

    # Internet
    if 'FAMI_TIENEINTERNET' in df.columns:
        inet_vals = sorted(df['FAMI_TIENEINTERNET'].dropna().unique().tolist())
        sel_inet = st.sidebar.multiselect('Tiene internet', inet_vals, default=inet_vals)
    else:
        sel_inet = []

    # Mostrar solo discrepancias
    only_mismatch = st.sidebar.checkbox('Mostrar solo discrepancias (real != pred)', value=False)

    # Aplicar filtros
    filtered = df.copy()
    if sel_periodo:
        filtered = filtered[filtered['PERIODO'].isin(sel_periodo)]
    if muni_col and sel_munis:
        filtered = filtered[filtered[muni_col].isin(sel_munis)]
    if sel_naturaleza:
        filtered = filtered[filtered['COLE_NATURALEZA'].isin(sel_naturaleza)]
    if sel_inet:
        filtered = filtered[filtered['FAMI_TIENEINTERNET'].isin(sel_inet)]
    if only_mismatch and {'real_puntaje_alto','prediccion_puntaje_alto'}.issubset(filtered.columns):
        filtered = filtered[filtered['real_puntaje_alto'] != filtered['prediccion_puntaje_alto']]

    # Resumen rápido
    st.subheader("Resumen rápido")
    cols = st.columns([2,1])
    with cols[0]:
        st.markdown("### Primeras filas (filtrado)")
        st.dataframe(filtered.head(100))
    with cols[1]:
        st.markdown("### Tamaño del conjunto")
        st.metric("Filas (filtrado)", len(filtered))
        st.metric("Columnas", len(filtered.columns))

    # Métricas del modelo (global y filtrado)
    st.markdown("---")
    st.subheader("Métricas del modelo")
    if metrics:
        st.markdown("**Métricas guardadas (global)**")
        st.json(metrics)
    else:
        st.info("No se encontró `metricas_modelo.json` en `outputs/`.")

    # Calcular métricas para el subset filtrado si hay etiquetas
    if {'real_puntaje_alto','prediccion_puntaje_alto'}.issubset(filtered.columns) and len(filtered) > 0:
        y_true = filtered['real_puntaje_alto']
        y_pred = filtered['prediccion_puntaje_alto']
        try:
            acc = accuracy_score(y_true, y_pred)
            prec = precision_score(y_true, y_pred, zero_division=0)
            rec = recall_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric('Accuracy', f"{acc:.3f}")
            m2.metric('Precision', f"{prec:.3f}")
            m3.metric('Recall', f"{rec:.3f}")
            m4.metric('F1', f"{f1:.3f}")
        except Exception:
            st.write('No se pudieron calcular métricas para el subset filtrado.')

    # Descarga del subset filtrado
    st.markdown('---')
    st.subheader('Exportar')
    if len(filtered) > 0:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button('Descargar CSV filtrado', data=csv, file_name='subset_predicciones.csv', mime='text/csv')
    else:
        st.info('No hay datos para exportar con los filtros actuales.')

    # Visualizaciones
    st.markdown('---')
    st.subheader('Visualizaciones')
    c1, c2 = st.columns(2)
    with c1:
        if 'prediccion_puntaje_alto' in filtered.columns:
            fig = px.histogram(filtered, x='prediccion_puntaje_alto', title='Distribución: predicción puntaje alto')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info('Columna `prediccion_puntaje_alto` no encontrada.')
    with c2:
        if 'real_puntaje_alto' in filtered.columns:
            fig2 = px.histogram(filtered, x='real_puntaje_alto', title='Distribución: real puntaje alto')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info('Columna `real_puntaje_alto` no encontrada.')

    if 'FAMI_TIENEINTERNET' in filtered.columns and {'real_puntaje_alto','prediccion_puntaje_alto'}.issubset(filtered.columns):
        st.markdown('### Puntaje alto por acceso a Internet (filtrado)')
        agg = filtered.groupby('FAMI_TIENEINTERNET')[['real_puntaje_alto','prediccion_puntaje_alto']].mean().reset_index()
        fig3 = px.bar(agg, x='FAMI_TIENEINTERNET', y=['real_puntaje_alto','prediccion_puntaje_alto'], barmode='group', labels={'value':'Proporción','FAMI_TIENEINTERNET':'Tiene internet'}, title='Puntaje alto: real vs predicho (por internet)')
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('---')
    st.subheader('Explora por columna')
    cat_cols = filtered.select_dtypes(include=['object']).columns.tolist()
    default_choices = [c for c in ['COLE_NATURALEZA','COLE_AREA_UBICACION','ESTU_GENERO'] if c in cat_cols]
    sel = st.selectbox('Elige columna categórica', default_choices + cat_cols)
    if sel and sel in filtered.columns:
        ct = filtered[sel].value_counts().reset_index()
        ct.columns = [sel, 'count']
        fig4 = px.bar(ct.head(20), x=sel, y='count', title=f'Distribución de {sel} (filtrado)')
        st.plotly_chart(fig4, use_container_width=True)

    st.caption('Dashboard interactivo: usa la barra lateral para filtrar y exportar subsets.')
