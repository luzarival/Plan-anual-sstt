"""
Catálogos maestros del Sistema de Gestión de SST de Pana Autos.

Jerarquía respetada en todo el aplicativo:
    PANA AUTOS -> ÁREA -> SUBÁREA -> ACTIVIDAD/PROCESO -> PELIGRO/RIESGO -> CONTROL

Nota: las áreas y subáreas provienen del listado organizacional de Pana Autos.
La asignación de qué subárea pertenece a qué área no fue provista, por lo que el
aplicativo permite combinar cualquier área con cualquier subárea. Cuando se
disponga del organigrama definitivo, basta con completar MAPEO_AREA_SUBAREA
para que los formularios filtren automáticamente.
"""

AREAS = [
    "HONDA AUTOS",
    "HONDA MOTOS",
    "HONDA CORPORATIVO",
    "CORPORATIVO",
    "GENERAL",
]

SUBAREAS = [
    "CORPORATIVO MOTOS HONDA",
    "VENTAS",
    "HONDA CORPORATIVO",
    "POSVENTA",
    "GENERAL",
    "MARKETING",
    "OPERACIONES",
    "HONDA MOTOS",
    "ALMACEN",
]

# Completar cuando se cuente con el organigrama oficial.
# Formato: {"HONDA AUTOS": ["VENTAS", "POSVENTA", ...], ...}
MAPEO_AREA_SUBAREA = {}


def subareas_de(area: str):
    """Devuelve las subáreas de un área. Si no hay mapeo definido, devuelve todas."""
    return MAPEO_AREA_SUBAREA.get(area, SUBAREAS)


MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre",
]

# Grupos de Exposición Similar propuestos para el rubro automotriz.
# Son una propuesta de trabajo: deben validarse contra el IPERC vigente.
GES = [
    "Técnicos de taller mecánico",
    "Técnicos de planchado y pintura",
    "Personal de almacén y logística",
    "Asesores de servicio y posventa",
    "Asesores de venta y showroom",
    "Personal administrativo",
]

TIPOS_EVENTO = [
    "Incidente",
    "Incidente peligroso",
    "Accidente leve",
    "Accidente incapacitante",
    "Accidente mortal",
    "Enfermedad ocupacional",
]

# Eventos que suman al numerador del Índice de Frecuencia
EVENTOS_FRECUENCIA = ["Accidente incapacitante", "Accidente mortal"]

TIPOS_PROGRAMA = [
    "Inspecciones",
    "Capacitación",
    "Simulacros",
    "Salud ocupacional",
    "Monitoreos ocupacionales",
    "Observaciones preventivas",
]

# Metas del periodo. Base: objetivos y metas del Plan Anual de SST de Pana Autos.
# 'sentido' indica si conviene que el valor sea alto ("mayor") o bajo ("menor").
METAS = {
    "indice_accidentabilidad": {
        "etiqueta": "Índice de accidentabilidad",
        "meta": 0.50,
        "sentido": "menor",
        "unidad": "",
        "familia": "Resultado",
    },
    "cumplimiento_inspecciones": {
        "etiqueta": "Cumplimiento de inspecciones",
        "meta": 90.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Preventivo",
    },
    "cierre_observaciones": {
        "etiqueta": "Cierre de observaciones",
        "meta": 90.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Preventivo",
    },
    "indicador_combinado_inspecciones": {
        "etiqueta": "Indicador combinado inspecciones/observaciones",
        "meta": 90.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Preventivo",
    },
    "cierre_acciones_correctivas": {
        "etiqueta": "Cierre de acciones correctivas (OPS/NC)",
        "meta": 90.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Preventivo",
    },
    "cumplimiento_capacitacion": {
        "etiqueta": "Cumplimiento del programa de capacitación",
        "meta": 90.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Capacitación",
    },
    "cobertura_capacitacion": {
        "etiqueta": "Cobertura de trabajadores capacitados",
        "meta": 90.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Capacitación",
    },
    "eficacia_capacitacion": {
        "etiqueta": "Eficacia de la capacitación",
        "meta": 80.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Capacitación",
    },
    "horas_capacitacion_trabajador": {
        "etiqueta": "Horas de capacitación por trabajador",
        "meta": 4.0,
        "sentido": "mayor",
        "unidad": "h",
        "familia": "Capacitación",
    },
    "cumplimiento_simulacros": {
        "etiqueta": "Simulacros ejecutados",
        "meta": 100.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Emergencias",
    },
    "brigadistas_capacitados": {
        "etiqueta": "Brigadistas capacitados",
        "meta": 100.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Emergencias",
    },
    "equipos_emergencia_operativos": {
        "etiqueta": "Equipos de emergencia operativos",
        "meta": 95.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Emergencias",
    },
    "cumplimiento_liderazgo": {
        "etiqueta": "Cumplimiento de actividades de liderazgo",
        "meta": 90.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Liderazgo",
    },
    "cumplimiento_legal": {
        "etiqueta": "Cumplimiento legal",
        "meta": 95.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Gestión",
    },
    "procedimientos_revisados": {
        "etiqueta": "Procedimientos revisados o actualizados",
        "meta": 100.0,
        "sentido": "mayor",
        "unidad": "%",
        "familia": "Gestión",
    },
}

# Umbral de alerta: por debajo (o por encima, según sentido) de este porcentaje
# de la meta el indicador se marca en rojo; entre este valor y la meta, en ámbar.
UMBRAL_ALERTA = 0.85
