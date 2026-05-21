from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "Vista_Resultados_unicos_Saber_11_20260521.csv"
METRICS_PATH = ROOT / "outputs" / "metricas_modelo.json"
PREDICTIONS_PATH = ROOT / "outputs" / "muestra_predicciones.csv"

TARGET_THRESHOLD = 300


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    df["PUNT_GLOBAL"] = pd.to_numeric(df["PUNT_GLOBAL"], errors="coerce")
    return df


@st.cache_data
def load_metrics() -> dict:
    if not METRICS_PATH.exists():
        return {}
    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data
def load_predictions_sample() -> pd.DataFrame:
    if not PREDICTIONS_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(PREDICTIONS_PATH, encoding="utf-8-sig")


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")

    filtered = df.copy()

    depto_col = "COLE_DEPTO_UBICACION"
    municipio_col = "COLE_MCPIO_UBICACION"
    naturaleza_col = "COLE_NATURALEZA"

    if depto_col in filtered.columns:
        deptos = sorted(filtered[depto_col].dropna().astype(str).unique().tolist())
        selected_depto = st.sidebar.selectbox("Departamento", ["Todos"] + deptos)
        if selected_depto != "Todos":
            filtered = filtered[filtered[depto_col].astype(str) == selected_depto]

    if municipio_col in filtered.columns:
        municipios = sorted(filtered[municipio_col].dropna().astype(str).unique().tolist())
        selected_municipio = st.sidebar.selectbox("Municipio", ["Todos"] + municipios)
        if selected_municipio != "Todos":
            filtered = filtered[filtered[municipio_col].astype(str) == selected_municipio]

    if naturaleza_col in filtered.columns:
        natur_options = sorted(filtered[naturaleza_col].dropna().astype(str).unique().tolist())
        selected_natur = st.sidebar.multiselect("Naturaleza colegio", natur_options, default=natur_options)
        if selected_natur:
            filtered = filtered[filtered[naturaleza_col].astype(str).isin(selected_natur)]

    return filtered


def show_overview(df_total: pd.DataFrame, valid: pd.DataFrame) -> None:
    st.subheader("Resumen del dataset")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros filtrados", f"{len(df_total):,}".replace(",", "."))
    col2.metric("Registros con PUNT_GLOBAL", f"{len(valid):,}".replace(",", "."))
    if len(valid) > 0:
        col3.metric("Promedio PUNT_GLOBAL", f"{valid['PUNT_GLOBAL'].mean():.2f}")
        col4.metric(
            "Puntaje alto (>= 300)",
            f"{(valid['PUNT_GLOBAL'] >= TARGET_THRESHOLD).mean() * 100:.2f}%",
        )
    else:
        col3.metric("Promedio PUNT_GLOBAL", "N/A")
        col4.metric("Puntaje alto (>= 300)", "N/A")


def show_eda(valid: pd.DataFrame) -> None:
    st.subheader("Análisis exploratorio")
    if valid.empty:
        st.warning("No hay datos con PUNT_GLOBAL para los filtros seleccionados.")
        return

    fig_hist, ax_hist = plt.subplots(figsize=(9, 4))
    sns.histplot(valid["PUNT_GLOBAL"], bins=30, kde=True, color="#2f6f9f", ax=ax_hist)
    ax_hist.axvline(
        TARGET_THRESHOLD,
        color="#d1495b",
        linestyle="--",
        label=f"Umbral: {TARGET_THRESHOLD}",
    )
    ax_hist.set_title("Distribución de puntaje global")
    ax_hist.set_xlabel("Puntaje global")
    ax_hist.set_ylabel("Cantidad")
    ax_hist.legend()
    st.pyplot(fig_hist)

    if "COLE_NATURALEZA" in valid.columns:
        fig_box, ax_box = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=valid, x="COLE_NATURALEZA", y="PUNT_GLOBAL", color="#8ab17d", ax=ax_box)
        ax_box.set_title("Puntaje por naturaleza del colegio")
        ax_box.set_xlabel("Naturaleza")
        ax_box.set_ylabel("Puntaje global")
        st.pyplot(fig_box)

    if "FAMI_TIENEINTERNET" in valid.columns:
        summary = (
            valid.groupby("FAMI_TIENEINTERNET", dropna=False)["PUNT_GLOBAL"]
            .agg(["count", "mean", "median"])
            .sort_values("mean", ascending=False)
            .round(2)
        )
        st.markdown("**Puntaje global según acceso a internet**")
        st.dataframe(summary, use_container_width=True)


def show_model_section() -> None:
    st.subheader("Resultados del modelo")
    metrics = load_metrics()

    if not metrics:
        st.warning("No se encontró `outputs/metricas_modelo.json`. Ejecuta primero `python src/train_model.py`.")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", metrics.get("accuracy", "-"))
    col2.metric("Precision", metrics.get("precision", "-"))
    col3.metric("Recall", metrics.get("recall", "-"))
    col4.metric("F1", metrics.get("f1", "-"))

    st.markdown("**Matriz de confusión**")
    matriz = metrics.get("matriz_confusion", [])
    if matriz:
        conf_df = pd.DataFrame(matriz, index=["Real: No alto", "Real: Alto"], columns=["Pred: No alto", "Pred: Alto"])
        st.dataframe(conf_df, use_container_width=True)

    reporte = metrics.get("reporte_clasificacion")
    if reporte:
        st.markdown("**Reporte de clasificación**")
        st.code(reporte)

    pred_sample = load_predictions_sample()
    if not pred_sample.empty:
        st.markdown("**Muestra de predicciones (200 filas)**")
        st.dataframe(pred_sample.head(50), use_container_width=True)


st.set_page_config(page_title="Dashboard Saber 11", layout="wide")
st.title("Dashboard del proyecto final - Saber 11")
st.caption("Milestone 3: integración de EDA, modelo de Machine Learning y comunicación ejecutiva.")

df_raw = load_data()
df = apply_filters(df_raw)
valid = df.dropna(subset=["PUNT_GLOBAL"]).copy()

tab1, tab2, tab3 = st.tabs(["Resumen", "EDA", "Modelo"])
with tab1:
    show_overview(df, valid)
with tab2:
    show_eda(valid)
with tab3:
    show_model_section()
