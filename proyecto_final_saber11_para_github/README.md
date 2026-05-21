# Analisis de resultados Saber 11

Proyecto final de Analitica de Datos.

## Problema

El proyecto analiza resultados historicos de Saber 11 para identificar patrones asociados al desempeno academico de estudiantes. El objetivo principal es construir un modelo de Machine Learning que estime si un estudiante pertenece al grupo de puntaje global alto a partir de variables del colegio y del contexto familiar.

## Pregunta de analisis

Que caracteristicas institucionales y familiares se relacionan con la probabilidad de obtener un puntaje global alto en Saber 11?

## Dataset

Archivo usado:

`data/Vista_Resultados_unicos_Saber_11_20260521.csv`

Resumen inicial:

- 36.613 registros.
- 51 columnas.
- 23.474 registros con `PUNT_GLOBAL` disponible.
- Variable objetivo del modelo: `puntaje_alto`, creada como `PUNT_GLOBAL >= 300`.

## Estructura del repositorio

```text
.
├── data/
│   └── Vista_Resultados_unicos_Saber_11_20260521.csv
├── figures/
│   └── graficos generados por el analisis
├── notebooks/
│   ├── 01_limpieza_eda.ipynb
│   └── 02_modelo_machine_learning.ipynb
├── outputs/
│   └── metricas y predicciones generadas
├── presentacion/
│   └── presentacion_final.md
├── reports/
│   └── informe_final.md
├── src/
│   ├── eda_saber11.py
│   └── train_model.py
├── requirements.txt
└── README.md
```

## Como ejecutar

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecutar analisis exploratorio:

```bash
python src/eda_saber11.py
```

3. Entrenar y evaluar el modelo:

```bash
python src/train_model.py
```

## Modelo propuesto

Se plantea un modelo de clasificacion con scikit-learn:

- Entrada: variables del colegio, ubicacion y contexto familiar.
- Salida: `puntaje_alto`.
- Criterio: 1 si `PUNT_GLOBAL >= 300`, 0 en caso contrario.
- Algoritmo base: Random Forest.
- Metricas: accuracy, precision, recall, F1 y matriz de confusion.

## Entregables del milestone

- Presentacion final: `presentacion/presentacion_final.md`.
- Informe final: `reports/informe_final.md`.
- Codigo documentado: `src/`.
- Notebooks guia: `notebooks/`.
- Resultados del modelo: `outputs/`.

