from pathlib import Path
import json

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "Vista_Resultados_unicos_Saber_11_20260521.csv"
OUTPUTS_DIR = ROOT / "outputs"

TARGET_COLUMN = "PUNT_GLOBAL"
TARGET_THRESHOLD = 300

FEATURE_COLUMNS = [
    "PERIODO",
    "COLE_AREA_UBICACION",
    "COLE_BILINGUE",
    "COLE_CALENDARIO",
    "COLE_CARACTER",
    "COLE_DEPTO_UBICACION",
    "COLE_GENERO",
    "COLE_JORNADA",
    "COLE_MCPIO_UBICACION",
    "COLE_NATURALEZA",
    "COLE_SEDE_PRINCIPAL",
    "ESTU_DEPTO_RESIDE",
    "ESTU_GENERO",
    "ESTU_MCPIO_RESIDE",
    "ESTU_NACIONALIDAD",
    "ESTU_PAIS_RESIDE",
    "ESTU_PRIVADO_LIBERTAD",
    "FAMI_CUARTOSHOGAR",
    "FAMI_EDUCACIONMADRE",
    "FAMI_EDUCACIONPADRE",
    "FAMI_ESTRATOVIVIENDA",
    "FAMI_PERSONASHOGAR",
    "FAMI_TIENEAUTOMOVIL",
    "FAMI_TIENECOMPUTADOR",
    "FAMI_TIENEINTERNET",
    "FAMI_TIENELAVADORA",
]


def load_model_data() -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    df[TARGET_COLUMN] = pd.to_numeric(df[TARGET_COLUMN], errors="coerce")
    df = df.dropna(subset=[TARGET_COLUMN]).copy()
    df["puntaje_alto"] = (df[TARGET_COLUMN] >= TARGET_THRESHOLD).astype(int)
    return df[FEATURE_COLUMNS], df["puntaje_alto"]


def build_pipeline() -> Pipeline:
    categorical_features = [column for column in FEATURE_COLUMNS if column != "PERIODO"]
    numeric_features = ["PERIODO"]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categoricas",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
            (
                "numericas",
                Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]),
                numeric_features,
            ),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=12,
        min_samples_leaf=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=1,
    )

    return Pipeline(steps=[("preprocesamiento", preprocessor), ("modelo", model)])


def main() -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)

    X, y = load_model_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    metrics = {
        "target": f"{TARGET_COLUMN} >= {TARGET_THRESHOLD}",
        "total_registros_modelo": int(len(X)),
        "registros_entrenamiento": int(len(X_train)),
        "registros_prueba": int(len(X_test)),
        "clase_positiva_puntaje_alto": int(y.sum()),
        "porcentaje_clase_positiva": round(float(y.mean() * 100), 2),
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
        "matriz_confusion": confusion_matrix(y_test, predictions).tolist(),
        "reporte_clasificacion": classification_report(
            y_test,
            predictions,
            target_names=["No alto", "Alto"],
            zero_division=0,
        ),
    }

    with open(OUTPUTS_DIR / "metricas_modelo.json", "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, ensure_ascii=False)

    prediction_sample = X_test.copy()
    prediction_sample["real_puntaje_alto"] = y_test.values
    prediction_sample["prediccion_puntaje_alto"] = predictions
    prediction_sample.head(200).to_csv(
        OUTPUTS_DIR / "muestra_predicciones.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Modelo entrenado y evaluado.")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
