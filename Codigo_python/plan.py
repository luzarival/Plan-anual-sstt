"""
Contenido del Plan Anual de SST que el aplicativo expone en la sección "Plan Anual".

Se incluye la estructura propuesta del plan y el cuadro de objetivos, metas e
indicadores, de modo que quien consulta un indicador pueda ver de inmediato de
qué objetivo del plan proviene. Esa trazabilidad objetivo -> meta -> indicador
es la razón de ser de esta sección.
"""

ESTRUCTURA_PLAN = [
    ("1. Introducción", []),
    ("2. Objetivo y alcance del Plan", []),
    ("3. Marco legal y documentos de referencia", []),
    ("4. Caracterización de Pana Autos", [
        "4.1. Descripción de la organización",
        "4.2. Estructura de áreas y subáreas",
        "4.3. Procesos y actividades por subárea",
        "4.4. Grupos de exposición similar (GES)",
    ]),
    ("5. Diagnóstico de la gestión de SST", [
        "5.1. Línea base del SG-SST",
        "5.2. Estadísticas de accidentabilidad del periodo anterior",
        "5.3. Resultados de inspecciones, observaciones y hallazgos",
        "5.4. Cumplimiento del Programa Anual del periodo anterior",
        "5.5. Salud ocupacional y ausentismo",
        "5.6. Brechas identificadas y lineamientos para el periodo 2026",
    ]),
    ("6. Política de Seguridad y Salud en el Trabajo", []),
    ("7. Identificación de peligros, evaluación de riesgos y controles", [
        "7.1. Metodología IPERC",
        "7.2. Riesgos prioritarios por área y subárea",
        "7.3. Mapa de riesgos",
        "7.4. Controles operacionales y procedimientos aplicables",
    ]),
    ("8. Objetivos, metas e indicadores", [
        "8.1. Objetivos generales y específicos",
        "8.2. Metas del periodo",
        "8.3. Alineamiento política – objetivo – meta – indicador – programa",
    ]),
    ("9. Organización, responsabilidades y liderazgo en SST", [
        "9.1. Responsabilidades por nivel jerárquico",
        "9.2. Comité de Seguridad y Salud en el Trabajo",
        "9.3. Reglamento Interno de Seguridad y Salud en el Trabajo",
        "9.4. Liderazgo visible de la línea de mando",
        "9.5. Recursos asignados a la gestión de SST",
    ]),
    ("10. Participación, consulta y comunicación", [
        "10.1. Participación y consulta de los trabajadores",
        "10.2. Matriz y cronograma de comunicación",
        "10.3. Reporte de actos y condiciones inseguras",
    ]),
    ("11. Programas anuales de Seguridad y Salud en el Trabajo", [
        "11.1. Programa Anual de Seguridad y Salud en el Trabajo",
        "11.2. Programa Anual de Capacitación en SST",
        "11.3. Programa Anual de Preparación y Respuesta ante Emergencias",
        "11.4. Programa Anual de Salud Ocupacional",
        "11.5. Programa Anual de Inspecciones y Observaciones Preventivas",
        "11.6. Programa Anual de Monitoreos de Higiene Ocupacional",
        "11.7. Cronograma general y articulación entre programas",
    ]),
    ("12. Gestión de contratistas, proveedores y terceros", []),
    ("13. Investigación de incidentes, accidentes y enfermedades ocupacionales", []),
    ("14. Sistema de indicadores y evaluación del desempeño", [
        "14.1. Estructura general del sistema de indicadores",
        "14.2. Indicadores de resultado",
        "14.3. Indicadores preventivos",
        "14.4. Indicadores de capacitación",
        "14.5. Indicadores de preparación y respuesta ante emergencias",
        "14.6. Indicadores de liderazgo y participación",
        "14.7. Indicadores de gestión del sistema",
        "14.8. Metas, criterios de evaluación y niveles de alerta",
        "14.9. Herramienta computacional para el procesamiento y análisis de indicadores SST",
        "14.10. Seguimiento mensual, análisis de tendencias y reporte al CSST",
    ]),
    ("15. Cumplimiento legal y auditorías", [
        "15.1. Evaluación del cumplimiento legal",
        "15.2. Auditoría interna",
        "15.3. Auditoría externa",
        "15.4. Seguimiento de resultados",
    ]),
    ("16. Presupuesto anual de SST", []),
    ("17. Mejora continua y revisión por la Dirección", [
        "17.1. Acciones correctivas, preventivas y oportunidades de mejora",
        "17.2. Evaluación de eficacia",
        "17.3. Revisión por la Dirección",
    ]),
    ("18. Control de documentos y mantenimiento de registros", []),
]

ANEXOS_PLAN = [
    "Anexo 1. Línea base del SG-SST",
    "Anexo 2. Estadísticas de accidentabilidad del periodo anterior",
    "Anexo 3. Matriz de objetivos, metas e indicadores",
    "Anexo 4. Matriz IPERC y riesgos prioritarios por área y subárea",
    "Anexo 5. Mapa de riesgos",
    "Anexo 6. Programa Anual de Seguridad y Salud en el Trabajo",
    "Anexo 7. Programa Anual de Capacitación en SST",
    "Anexo 8. Programa Anual de Preparación y Respuesta ante Emergencias",
    "Anexo 9. Programa Anual de Salud Ocupacional",
    "Anexo 10. Programa Anual de Inspecciones y Observaciones Preventivas",
    "Anexo 11. Programa Anual de Monitoreos de Higiene Ocupacional por GES",
    "Anexo 12. Ficha técnica de indicadores SST",
    "Anexo 13. Herramienta computacional para el procesamiento de indicadores SST",
    "Anexo 14. Presupuesto anual detallado por centro de costo",
]

# Objetivos del Plan Anual de SST de Pana Autos y su vínculo con los indicadores
# que este aplicativo calcula.
OBJETIVOS = [
    {
        "objetivo": "Identificar y evaluar los riesgos y prevenir lesiones ocupacionales",
        "meta": "Reducir en 50 % el índice de accidentabilidad respecto al periodo anterior",
        "indicador": "Índice de accidentabilidad",
        "clave": "indice_accidentabilidad",
        "responsable": "SST / CSST",
    },
    {
        "objetivo": "Realizar inspecciones y gestionar el cierre de observaciones",
        "meta": "≥ 90 % de cumplimiento",
        "indicador": "Indicador combinado inspecciones/observaciones",
        "clave": "indicador_combinado_inspecciones",
        "responsable": "SST",
    },
    {
        "objetivo": "Garantizar que los trabajadores sean capacitados en prevención de riesgos",
        "meta": "≥ 90 % de cumplimiento del programa",
        "indicador": "Cumplimiento del programa de capacitación",
        "clave": "cumplimiento_capacitacion",
        "responsable": "SST / Gestión Humana",
    },
    {
        "objetivo": "Asegurar la preparación y respuesta ante emergencias",
        "meta": "100 % de simulacros ejecutados",
        "indicador": "Simulacros ejecutados",
        "clave": "cumplimiento_simulacros",
        "responsable": "SST / Brigadas",
    },
    {
        "objetivo": "Fortalecer el liderazgo visible de la línea de mando",
        "meta": "≥ 90 % de actividades de liderazgo ejecutadas",
        "indicador": "Cumplimiento de actividades de liderazgo",
        "clave": "cumplimiento_liderazgo",
        "responsable": "Gerencia y jefaturas",
    },
    {
        "objetivo": "Cumplir la legislación vigente en materia de SST",
        "meta": "≥ 95 % de cumplimiento legal",
        "indicador": "Cumplimiento legal",
        "clave": "cumplimiento_legal",
        "responsable": "SST",
    },
    {
        "objetivo": "Mantener actualizados los documentos del SG-SST",
        "meta": "100 % de procedimientos revisados",
        "indicador": "Procedimientos revisados o actualizados",
        "clave": "procedimientos_revisados",
        "responsable": "SST",
    },
    {
        "objetivo": "Realizar el seguimiento de cierre de las OPS/NC",
        "meta": "90 % de acciones cerradas",
        "indicador": "Cierre de acciones correctivas (OPS/NC)",
        "clave": "cierre_acciones_correctivas",
        "responsable": "SST",
    },
]

FORMULAS = [
    ("Índice de frecuencia (IF)",
     "(Accidentes incapacitantes + accidentes fatales) × 10⁶ / horas-hombre trabajadas"),
    ("Índice de severidad (IS)",
     "(Días perdidos + días cargados) × 10⁶ / horas-hombre trabajadas"),
    ("Índice de accidentabilidad (IA)",
     "(Índice de frecuencia × Índice de severidad) / 1000"),
    ("Tasa de incidencia de enfermedades",
     "N.° de diagnósticos relacionados al trabajo × 100 / N.° total de trabajadores"),
    ("Indicador combinado de inspecciones",
     "(Inspecciones ejecutadas / programadas) × 0,5 + (Observaciones cerradas / totales) × 0,5"),
    ("Cumplimiento de programa",
     "Actividades ejecutadas × 100 / actividades programadas"),
    ("Cobertura de capacitación",
     "Trabajadores capacitados × 100 / trabajadores convocados"),
    ("Eficacia de capacitación",
     "Trabajadores aprobados × 100 / trabajadores capacitados"),
]
