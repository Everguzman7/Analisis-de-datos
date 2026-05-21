# Presentacion final del proyecto

## 1. Portada

**Titulo:** Analisis de resultados Saber 11  
**Estudiante:** Ever rodriguez, Carlos lozano, Miguel labradoe 
**Curso:** Analitica de Datos  
**Milestone:** Presentacion final del proyecto

**En este proyecto analizamos resultados de Saber 11 para entender que caracteristicas del colegio, del estudiante y del hogar se relacionan con un mejor desempeño academico.

## 2. Contexto del Problema
Saber 11 es una de las pruebas mas importantes para los estudiantes en Colombia, porque resume parte de su desempeño academico y puede influir en oportunidades de acceso a educacion superior.

Sin embargo, los resultados no dependen solamente del estudiante. Tambien pueden relacionarse con condiciones institucionales, familiares y de acceso a recursos.

Pregunta central:
Que variables institucionales y familiares se asocian con la probabilidad de obtener un puntaje global alto?


## 3. Objetivo del proyecto

Objetivo general:
Analizar resultados Saber 11 y construir un modelo de Machine Learning que clasifique estudiantes con probabilidad de obtener puntaje global alto.

Objetivos especificos:

- Limpiar y preparar la base de datos.
- Explorar patrones en los puntajes y variables del contexto.
- Identificar diferencias por colegio, jornada, acceso a internet y variables familiares.
- Entrenar y evaluar un modelo de clasificacion con scikit-learn.
- Comunicar conclusiones, recomendaciones y limitaciones del analisis.


## 4. Dataset utilizado

- Fuente: archivo `Vista_Resultados_unicos_Saber_11_20260521.csv`.
- Registros totales: 36.613.
- Columnas: 51.
- Registros con puntaje global disponible: 23.474.
- Variable objetivo: `puntaje_alto`.
Variable objetivo:
Creamos la variable puntaje_alto, donde:

1: estudiante con PUNT_GLOBAL >= 300.
0: estudiante con PUNT_GLOBAL < 300.

## 5. Preparacion y limpieza de datos

- Se cargaron los datos con codificacion UTF-8.
- Se convirtieron columnas de puntaje a numericas.
- Se revisaron valores faltantes.
- Se eliminaron registros sin `PUNT_GLOBAL` para el entrenamiento.
- Se creo la variable objetivo con umbral de 300 puntos.
Decision importante:
No usamos los puntajes por area como predictores principales, porque esos puntajes hacen parte del resultado global y podrian hacer que el modelo dependa de informacion demasiado directa.

## 6. Analisis exploratorio

El analisis exploratorio se centro en responder tres preguntas:

- Como se distribuye el puntaje global?
- Existen diferencias segun caracteristicas del colegio?
- Las variables familiares muestran relacion con el desempeno?

Graficos principales:
- Distribucion del puntaje global.
- Puntaje global por naturaleza del colegio.
- Puntaje global segun acceso a internet.
- Comparacion por jornada.


## 7. Hallazgos principales
Los principales hallazgos fueron:

- El puntaje global promedio se ubica alrededor de 270 puntos.
- Cerca del 26% de los registros validos alcanza 300 puntos o mas.
- La mayoria de registros analizados corresponde a Boyaca, especialmente a municipios como Sogamoso.
- Las variables del colegio y del hogar ayudan a contextualizar las diferencias de desempeno.
- El acceso a recursos tecnologicos, como internet o computador, es una variable relevante para - - analizar brechas academicas.

Nota:
El puntaje global alto no debe verse como un resultado aislado, sino como parte de un contexto educativo y familiar.

## 8. Modelo de Machine Learning
Como parte del repositorio se desarrollo un dashboard en Streamlit.

El dashboard permite:

- Filtrar por periodo, naturaleza del colegio y jornada.
- Ver metricas generales del puntaje global.
- Comparar promedios por naturaleza del colegio.
- Explorar diferencias por jornada y acceso a internet.
- Revisar una muestra de los datos filtrados.


## 9. Modelo de Machine Learning
El problema se abordo como una tarea de clasificacion.

Modelo utilizado: Random Forest Classifier.
Libreria: scikit-learn.
Variable objetivo: puntaje_alto.
Clase positiva: estudiantes con PUNT_GLOBAL >= 300.

Variables predictoras:

- Caracteristicas del colegio: naturaleza, jornada, area, calendario y ubicacion.
- Caracteristicas del estudiante: genero, residencia y nacionalidad.
- Variables familiares: educacion de los padres, estrato, acceso a internet, computador, automovil, lavadora y personas en el hogar.



## 10. Evaluacion del modelo
El modelo fue evaluado con un conjunto de prueba del 20% de los datos.

Metricas obtenidas:

Accuracy: 0.6948.
Precision para puntaje alto: 0.4455.
Recall para puntaje alto: 0.7178.
F1-score para puntaje alto: 0.5498.
Lectura del resultado:
El modelo identifica una parte importante de los estudiantes con puntaje alto. Su mayor fortaleza es el recall, porque logra detectar muchos casos positivos. Sin embargo, tambien genera falsos positivos, por lo que debe interpretarse como una herramienta exploratoria y no como una decision definitiva.

## 11. Interpretacion general
El modelo y el analisis muestran que las variables institucionales y familiares aportan informacion para explicar diferencias en los resultados.

Esto no significa que una variable cause directamente un puntaje alto o bajo. Lo que podemos afirmar es que existen patrones y asociaciones utiles para orientar preguntas educativas.

Interpretacion principal:
El desempeno academico esta relacionado con una combinacion de factores: entorno institucional, condiciones familiares y acceso a recursos.



## 12. Recomendaciones 
A partir del analisis, proponemos:

- Fortalecer el acceso a recursos tecnologicos, especialmente internet y computador.
- Revisar diferencias de desempeno entre jornadas y tipos de colegio.
- Usar el dashboard para identificar grupos que requieren mayor acompanamiento.
- Complementar el analisis con informacion academica adicional, como asistencia, notas internas o programas de apoyo.
- Usar el modelo como apoyo para detectar patrones, no como herramienta de clasificacion individual definitiva.


## 13. limitaciones

El proyecto tiene algunas limitaciones importantes:

- No todos los registros tienen PUNT_GLOBAL, por lo que no todos se usaron para entrenar.
- El modelo identifica asociaciones, no relaciones causales.
- Algunas variables categoricas tienen valores faltantes o inconsistentes.
- El umbral de 300 puntos es una decision del proyecto y podria modificarse.
- El dataset se concentra principalmente en Boyaca, por lo que los resultados no necesariamente representan todo el pais
## 14. conclusiones 
Este proyecto integro limpieza de datos, analisis exploratorio, visualizacion, dashboard interactivo y Machine Learning.

La principal conclusion es que el desempeno en Saber 11 puede analizarse mejor cuando se considera el contexto completo del estudiante. Las variables del colegio y del hogar permiten encontrar patrones que ayudan a entender diferencias de rendimiento.

El modelo desarrollado es una primera aproximacion util. Aunque no reemplaza el juicio educativo, permite apoyar el analisis y abrir nuevas preguntas para mejorar el acompanamiento academico.

## 15. Cierre 
Con este proyecto demostramos el proceso completo de analitica de datos:

Entender un problema.
Preparar datos reales.
Explorar patrones.
Construir un modelo.
Evaluar resultados.
Comunicar hallazgos a una audiencia.
## Nota:
La analitica de datos no solo sirve para predecir, sino tambien para comprender mejor una realidad y tomar mejores decisiones.
