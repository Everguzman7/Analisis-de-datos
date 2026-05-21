# Análisis de resultados Saber 11

## Integrantes
- Ever Rodríguez
- Carlos Lozano
- Miguel Labrado

## Descripción del proyecto
Este proyecto analiza resultados de Saber 11 para identificar factores institucionales y familiares asociados al puntaje global alto. Además, se desarrolla un modelo de Machine Learning para clasificar estudiantes con probabilidad de obtener `PUNT_GLOBAL >= 300`.

## Pregunta de investigación
¿Qué variables del colegio, del estudiante y del hogar se relacionan con la probabilidad de obtener un puntaje global alto en Saber 11?

## Dataset
Archivo utilizado:

`data/Vista_Resultados_unicos_Saber_11_20260521.csv`

Resumen:
- 36.613 registros.
- 51 columnas.
- 23.474 registros con puntaje global disponible.
- Variable objetivo: `puntaje_alto`.

## Estructura del repositorio
```text
data/              Dataset del proyecto
dashboard/         Dashboard interactivo en Streamlit
figures/           Gráficos generados
notebooks/         Notebooks de limpieza, EDA y modelo
outputs/           Métricas y resultados del modelo
presentacion/      Presentación final
reports/           Informe final
src/               Código fuente del análisis y modelo

## Modelo de Machine Learning
Tipo: Clasificación.
Algoritmo: Random Forest.
Librería: scikit-learn.
Variable objetivo: puntaje_alto.
Criterio: PUNT_GLOBAL >= 300.

##Resultados del modelo

Accuracy: 0.6948
Precision: 0.4455
Recall: 0.7178
F1-score: 0.5498

## Conclusiones
El análisis muestra que variables del colegio, del estudiante y del hogar ayudan a identificar patrones asociados al desempeño alto en Saber 11. El modelo funciona como una primera aproximación exploratoria y debe interpretarse como apoyo al análisis, no como una herramienta definitiva de decisión individual.

##Limitaciones
No todos los registros tienen PUNT_GLOBAL.
El modelo identifica asociaciones, no causalidad.
El umbral de 300 puntos puede ajustarse.
El dataset se concentra principalmente en Boyacá.

##Entregables
Presentación final: presentacion/presentacion_final_saber11.pptx
Informe final: reports/informe_final.md
Dashboard: dashboard/app.py
Modelo: src/train_model.py
Notebooks: notebooks/


