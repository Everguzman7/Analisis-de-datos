# Informe final: Analisis de resultados Saber 11

## 1. Introduccion

Este proyecto analiza resultados de Saber 11 con el fin de identificar patrones asociados al desempeno academico. La base incluye informacion del colegio, caracteristicas del estudiante, variables familiares y puntajes por area.

## 2. Problema

El desempeno en Saber 11 puede estar relacionado con factores institucionales y familiares. Comprender estas relaciones permite orientar recomendaciones para mejorar acompanamiento academico, acceso a recursos y estrategias educativas.

## 3. Objetivo general

Construir un analisis de datos y un modelo de Machine Learning que clasifique si un estudiante tiene probabilidad de obtener un puntaje global alto en Saber 11.

## 4. Objetivos especificos

- Limpiar y preparar la base de resultados Saber 11.
- Describir la distribucion de puntajes y variables relevantes.
- Comparar resultados segun caracteristicas del colegio y del hogar.
- Entrenar un modelo de clasificacion con scikit-learn.
- Evaluar el modelo con metricas apropiadas.
- Proponer recomendaciones a partir de los hallazgos.

## 5. Datos

La base contiene 36.613 registros y 51 columnas. Para el modelo se usan los registros con `PUNT_GLOBAL` disponible. La variable objetivo se construye asi:

```text
puntaje_alto = 1 si PUNT_GLOBAL >= 300
puntaje_alto = 0 si PUNT_GLOBAL < 300
```

## 6. Metodologia

1. Carga del archivo CSV con codificacion UTF-8.
2. Conversion de columnas de puntaje a formato numerico.
3. Revision de valores nulos.
4. Analisis exploratorio de puntajes.
5. Creacion de la variable objetivo `puntaje_alto`.
6. Separacion entrenamiento/prueba con `train_test_split`.
7. Preprocesamiento con imputacion y One-Hot Encoding.
8. Entrenamiento de modelo Random Forest.
9. Evaluacion con accuracy, precision, recall, F1 y matriz de confusion.

## 7. Hallazgos iniciales

- El puntaje global promedio esta alrededor de 270 en los registros validos.
- Aproximadamente una cuarta parte de los registros con puntaje global supera el umbral de 300 puntos.
- Existen variables con valores faltantes, especialmente en puntajes de algunas areas y variables familiares.
- La mayor parte de los registros corresponde a Boyaca y especialmente a municipios como Sogamoso.

## 8. Modelo de Machine Learning

El modelo propuesto es un Random Forest de clasificacion. Se escogio porque permite trabajar con relaciones no lineales y variables categoricas transformadas mediante One-Hot Encoding.

Variables usadas:

- Caracteristicas del colegio: naturaleza, jornada, calendario, ubicacion, genero, area.
- Caracteristicas del estudiante: genero, residencia, nacionalidad.
- Caracteristicas familiares: educacion de madre/padre, estrato, acceso a internet, computador, automovil, lavadora, personas en el hogar.

No se usan los puntajes por area como predictores principales para evitar que el modelo dependa de variables que ya forman parte del resultado final.

## 9. Resultados del modelo

Los resultados se generaron ejecutando:

```bash
python src/train_model.py
```

Metricas obtenidas en el conjunto de prueba:

- Accuracy: 0.6948.
- Precision para puntaje alto: 0.4455.
- Recall para puntaje alto: 0.7178.
- F1-score para puntaje alto: 0.5498.
- Matriz de confusion: 2.387 verdaderos negativos, 1.089 falsos positivos, 344 falsos negativos y 875 verdaderos positivos.

Interpretacion: el modelo detecta una parte importante de los estudiantes con puntaje alto, pero todavia genera falsos positivos. Esto es aceptable como modelo inicial exploratorio, aunque se puede mejorar ajustando variables, umbral y algoritmo.

## 10. Limitaciones

- La base tiene registros sin `PUNT_GLOBAL`, por lo que no todos pueden usarse para entrenar el modelo.
- El modelo identifica asociaciones, no causalidad.
- Algunas variables pueden tener sesgos de reporte o categorias incompletas.
- El umbral de 300 puntos es una decision analitica; puede ajustarse segun el criterio del profesor o del proyecto.

## 11. Recomendaciones

- Fortalecer estrategias de acompanamiento a estudiantes con menor acceso a recursos tecnologicos.
- Revisar diferencias de desempeno por jornada, naturaleza del colegio y municipio.
- Usar el modelo como apoyo exploratorio, no como herramienta definitiva de decision individual.
- Complementar con analisis cualitativo o informacion institucional para interpretar mejor los resultados.

## 12. Conclusiones

El proyecto muestra que es posible integrar limpieza, analisis exploratorio, visualizacion y Machine Learning para estudiar resultados Saber 11. La informacion institucional y familiar permite construir un modelo predictivo inicial y generar recomendaciones orientadas a mejorar el acompanamiento academico.
