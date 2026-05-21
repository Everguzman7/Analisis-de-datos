# Presentacion final del proyecto

## 1. Portada

**Titulo:** Analisis de resultados Saber 11  
**Estudiante:** Ever Guzman  
**Curso:** Analitica de Datos  
**Milestone:** Presentacion final del proyecto

## 2. Problema

Los resultados Saber 11 permiten observar diferencias de desempeno academico entre estudiantes. El problema del proyecto es identificar que variables institucionales y familiares se asocian con un puntaje global alto.

## 3. Objetivo

Analizar resultados Saber 11 y construir un modelo de Machine Learning que clasifique estudiantes con probabilidad de obtener puntaje global alto.

## 4. Dataset

- Fuente: archivo `Vista_Resultados_unicos_Saber_11_20260521.csv`.
- Registros totales: 36.613.
- Columnas: 51.
- Registros con puntaje global disponible: 23.474.
- Variable objetivo: `puntaje_alto`.

## 5. Limpieza y preparacion

- Se cargaron los datos con codificacion UTF-8.
- Se convirtieron columnas de puntaje a numericas.
- Se revisaron valores faltantes.
- Se eliminaron registros sin `PUNT_GLOBAL` para el entrenamiento.
- Se creo la variable objetivo con umbral de 300 puntos.

## 6. Analisis exploratorio

Graficos sugeridos:

- Distribucion del puntaje global.
- Puntaje global por naturaleza del colegio.
- Puntaje global segun acceso a internet.
- Comparacion por jornada o municipio.

## 7. Hallazgos principales

- El puntaje global promedio se ubica alrededor de 270.
- Cerca del 26% de los registros validos alcanza 300 puntos o mas.
- Las variables familiares y del colegio aportan contexto para explicar diferencias de desempeno.

## 8. Modelo de Machine Learning

- Tipo: clasificacion.
- Algoritmo: Random Forest.
- Libreria: scikit-learn.
- Variable objetivo: `puntaje_alto`.
- Predictores: colegio, ubicacion, estudiante y variables familiares.

## 9. Evaluacion

Metricas del modelo:

- Accuracy: 0.6948.
- Precision para puntaje alto: 0.4455.
- Recall para puntaje alto: 0.7178.
- F1-score para puntaje alto: 0.5498.
- Matriz de confusion: [[2387, 1089], [344, 875]].

Lectura: el modelo logra identificar buena parte de los estudiantes con puntaje alto, aunque tambien clasifica algunos estudiantes como alto cuando realmente no lo son.

## 10. Interpretacion

El modelo sirve para identificar patrones generales. No debe interpretarse como una decision definitiva sobre estudiantes individuales.

## 11. Recomendaciones

- Fortalecer acceso a recursos educativos y tecnologicos.
- Revisar diferencias por colegio, jornada y municipio.
- Priorizar acompanamiento academico en grupos con menor probabilidad de puntaje alto.

## 12. Limitaciones

- Hay registros sin puntaje global.
- El modelo muestra asociaciones, no causalidad.
- El umbral de 300 puntos puede ajustarse.
- Algunas variables categoricas tienen valores faltantes o inconsistentes.

## 13. Cierre

Este proyecto integra limpieza, analisis exploratorio, visualizacion, Machine Learning y comunicacion de resultados, cumpliendo los componentes principales del milestone final.
