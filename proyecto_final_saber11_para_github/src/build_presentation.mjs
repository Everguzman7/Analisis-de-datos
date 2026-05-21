const {
  Presentation,
  PresentationFile,
  column,
  row,
  grid,
  text,
  chart,
  rule,
  fill,
  hug,
  fixed,
  wrap,
  fr,
  auto,
} = await import("@oai/artifact-tool");
const fs = await import("node:fs/promises");

const presentation = Presentation.create({
  slideSize: { width: 1920, height: 1080 },
});

const colors = {
  ink: "#17212B",
  muted: "#52616B",
  green: "#94B82D",
  blue: "#2563A8",
  red: "#D1495B",
  sand: "#F6F7F2",
  line: "#D7DED8",
};

function addSlide(title, subtitle, bodyNodes) {
  const slide = presentation.slides.add();
  slide.compose(
    column(
      {
        name: "root",
        width: fill,
        height: fill,
        padding: { x: 96, y: 72 },
        gap: 28,
      },
      [
        text(title, {
          name: "title",
          width: fill,
          height: hug,
          style: { fontSize: 52, bold: true, color: colors.ink },
        }),
        subtitle
          ? text(subtitle, {
              name: "subtitle",
              width: wrap(1280),
              height: hug,
              style: { fontSize: 28, color: colors.muted },
            })
          : rule({ name: "title-rule", width: fixed(220), stroke: colors.green, weight: 6 }),
        ...bodyNodes,
      ],
    ),
    { frame: { left: 0, top: 0, width: 1920, height: 1080 }, baseUnit: 8 },
  );
}

function bulletBlock(items) {
  return column(
    { name: "bullets", width: fill, height: hug, gap: 18 },
    items.map((item, index) =>
      row(
        { name: `bullet-${index + 1}`, width: fill, height: hug, gap: 18 },
        [
          text("•", {
            name: `dot-${index + 1}`,
            width: fixed(28),
            height: hug,
            style: { fontSize: 31, bold: true, color: colors.green },
          }),
          text(item, {
            name: `bullet-text-${index + 1}`,
            width: wrap(1320),
            height: hug,
            style: { fontSize: 29, color: colors.ink },
          }),
        ],
      ),
    ),
  );
}

function metric(label, value, note) {
  return column(
    { name: `metric-${label}`, width: fill, height: hug, gap: 8 },
    [
      text(value, {
        width: fill,
        height: hug,
        style: { fontSize: 54, bold: true, color: colors.blue },
      }),
      text(label, {
        width: fill,
        height: hug,
        style: { fontSize: 22, bold: true, color: colors.ink },
      }),
      text(note, {
        width: fill,
        height: hug,
        style: { fontSize: 18, color: colors.muted },
      }),
    ],
  );
}

addSlide(
  "Analisis de resultados Saber 11",
  "Proyecto final de Analitica de Datos | Milestone 3",
  [
    rule({ name: "cover-rule", width: fixed(360), stroke: colors.green, weight: 8 }),
    text("Objetivo: analizar factores institucionales y familiares asociados al puntaje global alto.", {
      name: "cover-claim",
      width: wrap(1260),
      height: hug,
      style: { fontSize: 38, color: colors.ink },
    }),
    text("Ever Guzman", {
      name: "author",
      width: fill,
      height: hug,
      style: { fontSize: 26, color: colors.muted },
    }),
  ],
);

addSlide(
  "Problema y pregunta",
  "Saber 11 permite estudiar diferencias de desempeno academico con datos reales.",
  [
    bulletBlock([
      "Problema: no todos los estudiantes tienen las mismas condiciones institucionales y familiares.",
      "Pregunta: que variables se relacionan con la probabilidad de obtener puntaje global alto?",
      "Enfoque: clasificar puntaje alto usando variables del colegio, estudiante y hogar.",
    ]),
  ],
);

addSlide(
  "Dataset usado",
  "Vista_Resultados_unicos_Saber_11_20260521.csv",
  [
    grid(
      { name: "metrics", width: fill, height: hug, columns: [fr(1), fr(1), fr(1)], columnGap: 56 },
      [
        metric("Registros totales", "36.613", "Base completa"),
        metric("Columnas", "51", "Colegio, estudiante, familia y puntajes"),
        metric("Registros modelables", "23.474", "Con PUNT_GLOBAL disponible"),
      ],
    ),
    text("Variable objetivo: puntaje_alto = 1 cuando PUNT_GLOBAL >= 300.", {
      name: "target-note",
      width: wrap(1200),
      height: hug,
      style: { fontSize: 30, color: colors.ink },
    }),
  ],
);

addSlide(
  "Metodologia",
  "Flujo aplicado al proyecto.",
  [
    bulletBlock([
      "Carga del CSV con codificacion UTF-8 y conversion de puntajes a numeros.",
      "Revision de valores nulos y seleccion de registros con puntaje global.",
      "Analisis exploratorio: distribucion de puntajes y comparaciones por variables clave.",
      "Modelo de clasificacion con scikit-learn: preprocesamiento, entrenamiento y evaluacion.",
    ]),
  ],
);

addSlide(
  "Distribucion de resultados",
  "El puntaje global promedio fue 269,95 y la mediana 269.",
  [
    chart({
      name: "target-chart",
      chartType: "bar",
      width: fill,
      height: fixed(520),
      config: {
        title: { text: "Distribucion segun umbral de 300 puntos" },
        categories: ["No alto", "Alto"],
        series: [{ name: "Estudiantes", values: [17380, 6094] }],
      },
    }),
    text("Aproximadamente 25,96% de los registros validos alcanzan 300 puntos o mas.", {
      name: "chart-note",
      width: wrap(1200),
      height: hug,
      style: { fontSize: 28, color: colors.muted },
    }),
  ],
);

addSlide(
  "Modelo de Machine Learning",
  "Random Forest de clasificacion con preprocesamiento de variables categoricas.",
  [
    bulletBlock([
      "Predictores: colegio, ubicacion, genero, nacionalidad y variables familiares.",
      "No se usan los puntajes por area como predictores principales para evitar dependencia directa del resultado.",
      "Entrenamiento: 18.779 registros. Prueba: 4.695 registros.",
      "Metrica central: F1-score y recall para la clase de puntaje alto.",
    ]),
  ],
);

addSlide(
  "Resultados del modelo",
  "El modelo identifica una parte importante de estudiantes con puntaje alto.",
  [
    grid(
      { name: "model-metrics", width: fill, height: hug, columns: [fr(1), fr(1), fr(1), fr(1)], columnGap: 38 },
      [
        metric("Accuracy", "0,6948", "Desempeno global"),
        metric("Precision", "0,4455", "Clase puntaje alto"),
        metric("Recall", "0,7178", "Clase puntaje alto"),
        metric("F1-score", "0,5498", "Clase puntaje alto"),
      ],
    ),
    text("Matriz de confusion: 2.387 VN, 1.089 FP, 344 FN y 875 VP.", {
      name: "confusion",
      width: wrap(1300),
      height: hug,
      style: { fontSize: 28, color: colors.ink },
    }),
  ],
);

addSlide(
  "Recomendaciones",
  "El modelo debe usarse como apoyo exploratorio, no como decision definitiva individual.",
  [
    bulletBlock([
      "Fortalecer acompanamiento a estudiantes con menor acceso a recursos tecnologicos.",
      "Revisar diferencias por jornada, naturaleza del colegio y municipio.",
      "Complementar el analisis cuantitativo con informacion institucional y academica.",
      "Mejorar el modelo probando otros algoritmos y validando variables con criterio educativo.",
    ]),
  ],
);

addSlide(
  "Limitaciones y cierre",
  "El proyecto integra limpieza, EDA, visualizacion, Machine Learning y comunicacion de resultados.",
  [
    bulletBlock([
      "Hay registros sin PUNT_GLOBAL, por eso no todos se usan para entrenar.",
      "El modelo muestra asociaciones, no causalidad.",
      "El umbral de 300 puntos puede ajustarse segun el criterio de evaluacion.",
      "Siguiente paso: preparar discurso de 15-20 minutos y subir el repositorio completo.",
    ]),
  ],
);

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save("presentacion/presentacion_final_saber11.pptx");

try {
  const preview = await presentation.export({ format: "png" });
  await fs.writeFile(
    "presentacion/preview_presentacion_final.png",
    Buffer.from(await preview.arrayBuffer()),
  );
} catch (error) {
  console.warn("No se pudo exportar preview PNG:", error.message);
}

console.log("presentacion/presentacion_final_saber11.pptx");
