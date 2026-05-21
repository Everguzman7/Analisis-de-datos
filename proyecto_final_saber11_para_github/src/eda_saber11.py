from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "Vista_Resultados_unicos_Saber_11_20260521.csv"
FIGURES_DIR = ROOT / "figures"
OUTPUTS_DIR = ROOT / "outputs"

SCORE_COLUMNS = [
    "PUNT_INGLES",
    "PUNT_MATEMATICAS",
    "PUNT_SOCIALES_CIUDADANAS",
    "PUNT_C_NATURALES",
    "PUNT_LECTURA_CRITICA",
    "PUNT_GLOBAL",
]


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    for column in SCORE_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    OUTPUTS_DIR.mkdir(exist_ok=True)

    df = load_data()
    valid = df.dropna(subset=["PUNT_GLOBAL"]).copy()
    valid["puntaje_alto"] = (valid["PUNT_GLOBAL"] >= 300).astype(int)

    summary = pd.DataFrame(
        {
            "valor": [
                len(df),
                df.shape[1],
                len(valid),
                int(valid["puntaje_alto"].sum()),
                round(valid["puntaje_alto"].mean() * 100, 2),
                round(valid["PUNT_GLOBAL"].mean(), 2),
                round(valid["PUNT_GLOBAL"].median(), 2),
            ]
        },
        index=[
            "registros_totales",
            "columnas",
            "registros_con_puntaje_global",
            "estudiantes_puntaje_alto",
            "porcentaje_puntaje_alto",
            "promedio_punt_global",
            "mediana_punt_global",
        ],
    )
    summary.to_csv(OUTPUTS_DIR / "resumen_dataset.csv", encoding="utf-8-sig")

    missing = (
        df.isna()
        .mean()
        .sort_values(ascending=False)
        .mul(100)
        .round(2)
        .reset_index()
    )
    missing.columns = ["columna", "porcentaje_nulos"]
    missing.to_csv(OUTPUTS_DIR / "valores_nulos.csv", index=False, encoding="utf-8-sig")

    score_summary = valid[SCORE_COLUMNS].describe().round(2)
    score_summary.to_csv(OUTPUTS_DIR / "estadisticas_puntajes.csv", encoding="utf-8-sig")

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(9, 5))
    sns.histplot(valid["PUNT_GLOBAL"], bins=30, kde=True, color="#2f6f9f")
    plt.axvline(300, color="#d1495b", linestyle="--", label="Umbral puntaje alto: 300")
    plt.title("Distribucion del puntaje global Saber 11")
    plt.xlabel("Puntaje global")
    plt.ylabel("Cantidad de estudiantes")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "distribucion_puntaje_global.png", dpi=160)
    plt.close()

    by_nature = (
        valid.groupby("COLE_NATURALEZA", dropna=False)["PUNT_GLOBAL"]
        .agg(["count", "mean", "median"])
        .sort_values("mean", ascending=False)
        .round(2)
    )
    by_nature.to_csv(OUTPUTS_DIR / "puntaje_por_naturaleza_colegio.csv", encoding="utf-8-sig")

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=valid, x="COLE_NATURALEZA", y="PUNT_GLOBAL", color="#8ab17d")
    plt.title("Puntaje global por naturaleza del colegio")
    plt.xlabel("Naturaleza del colegio")
    plt.ylabel("Puntaje global")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "puntaje_por_naturaleza.png", dpi=160)
    plt.close()

    by_internet = (
        valid.groupby("FAMI_TIENEINTERNET", dropna=False)["PUNT_GLOBAL"]
        .agg(["count", "mean", "median"])
        .sort_values("mean", ascending=False)
        .round(2)
    )
    by_internet.to_csv(OUTPUTS_DIR / "puntaje_por_internet.csv", encoding="utf-8-sig")

    print("Analisis exploratorio finalizado.")
    print(summary)


if __name__ == "__main__":
    main()

