"""
Capa de datos del aplicativo. Persistencia en archivos CSV dentro de /datos.

Se eligió CSV a propósito: los archivos son legibles, se abren en Excel y se
pueden entregar como evidencia del trabajo sin necesidad de instalar un motor
de base de datos. Cambiar a SQLite más adelante solo exigiría reemplazar las
funciones cargar_* y guardar_*.
"""

from __future__ import annotations

import os
import random

import pandas as pd

RUTA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")

ARCHIVOS = {
    "eventos": "eventos.csv",
    "horas": "horas_hombre.csv",
    "programas": "programas.csv",
    "capacitacion": "capacitacion.csv",
    "liderazgo": "liderazgo.csv",
    "gestion": "gestion.csv",
}

ESQUEMAS = {
    "eventos": ["fecha", "mes", "area", "subarea", "ges", "tipo_evento",
                "descripcion", "parte_afectada", "dias_perdidos", "dias_cargados",
                "estado_investigacion"],
    "horas": ["mes", "area", "subarea", "n_trabajadores", "horas_hombre"],
    "programas": ["mes", "area", "subarea", "tipo_programa", "actividad",
                  "programado", "ejecutado", "responsable"],
    "capacitacion": ["mes", "area", "subarea", "tema", "programadas", "ejecutadas",
                     "trabajadores_convocados", "trabajadores_capacitados",
                     "trabajadores_aprobados", "horas_dictadas"],
    "liderazgo": ["mes", "area", "actividad", "programado", "ejecutado", "responsable"],
    "gestion": ["mes", "requisitos_legales_total", "requisitos_legales_cumplidos",
                "procedimientos_total", "procedimientos_revisados",
                "acciones_creadas", "acciones_cerradas"],
}


def _ruta(clave: str) -> str:
    return os.path.join(RUTA_DATOS, ARCHIVOS[clave])


def asegurar_directorio() -> None:
    os.makedirs(RUTA_DATOS, exist_ok=True)


def cargar(clave: str) -> pd.DataFrame:
    """Carga un conjunto de datos; devuelve un DataFrame vacío con el esquema si no existe."""
    asegurar_directorio()
    ruta = _ruta(clave)
    if not os.path.exists(ruta):
        return pd.DataFrame(columns=ESQUEMAS[clave])
    df = pd.read_csv(ruta)
    for col in ESQUEMAS[clave]:
        if col not in df.columns:
            df[col] = None
    return df[ESQUEMAS[clave]]


def guardar(clave: str, df: pd.DataFrame) -> None:
    asegurar_directorio()
    df.to_csv(_ruta(clave), index=False)


def agregar_fila(clave: str, fila: dict) -> pd.DataFrame:
    df = cargar(clave)
    nueva = pd.DataFrame([{c: fila.get(c) for c in ESQUEMAS[clave]}])
    df = pd.concat([df, nueva], ignore_index=True)
    guardar(clave, df)
    return df


def eliminar_fila(clave: str, indice: int) -> pd.DataFrame:
    df = cargar(clave)
    if 0 <= indice < len(df):
        df = df.drop(df.index[indice]).reset_index(drop=True)
        guardar(clave, df)
    return df


def hay_datos() -> bool:
    return os.path.exists(_ruta("horas"))


# ---------------------------------------------------------------------------
# Datos de demostración
# ---------------------------------------------------------------------------

def generar_datos_ejemplo(semilla: int = 7) -> None:
    """
    Crea un juego de datos ficticio y coherente para demostrar el aplicativo.

    IMPORTANTE: estos datos son simulados, no corresponden a la operación real
    de Pana Autos. Sirven únicamente para probar los cálculos y la visualización.
    """
    from catalogos import AREAS, GES, MESES, SUBAREAS, TIPOS_PROGRAMA

    rnd = random.Random(semilla)
    asegurar_directorio()

    combinaciones = [
        ("HONDA AUTOS", "VENTAS", 78),
        ("HONDA AUTOS", "POSVENTA", 96),
        ("HONDA AUTOS", "OPERACIONES", 64),
        ("HONDA MOTOS", "HONDA MOTOS", 42),
        ("HONDA CORPORATIVO", "HONDA CORPORATIVO", 38),
        ("CORPORATIVO", "MARKETING", 22),
        ("CORPORATIVO", "ALMACEN", 47),
        ("GENERAL", "GENERAL", 37),
    ]

    # --- Horas-hombre -----------------------------------------------------
    filas_horas = []
    for mes in MESES:
        for area, subarea, dotacion in combinaciones:
            filas_horas.append({
                "mes": mes,
                "area": area,
                "subarea": subarea,
                "n_trabajadores": dotacion,
                "horas_hombre": dotacion * rnd.randint(184, 200),
            })
    guardar("horas", pd.DataFrame(filas_horas))

    # --- Eventos ----------------------------------------------------------
    catalogo_eventos = [
        ("Incidente", "Casi contacto con vehículo en maniobra de patio", "No aplica", 0, 0),
        ("Incidente", "Derrame menor de aceite en zona de taller", "No aplica", 0, 0),
        ("Incidente peligroso", "Falla de elevador hidráulico con vehículo montado", "No aplica", 0, 0),
        ("Accidente leve", "Corte superficial en mano al manipular herramienta", "Mano", 0, 0),
        ("Accidente leve", "Contusión en pie por caída de autoparte", "Pie", 0, 0),
        ("Accidente leve", "Proyección de partícula a los ojos en esmerilado", "Ojo", 0, 0),
        ("Accidente incapacitante", "Atrapamiento de dedo en desmontaje de neumático", "Dedo", 12, 0),
        ("Accidente incapacitante", "Lumbalgia por manipulación manual de carga", "Espalda", 9, 0),
        ("Accidente incapacitante", "Caída al mismo nivel por piso húmedo en taller", "Rodilla", 7, 0),
        ("Enfermedad ocupacional", "Trastorno musculoesquelético relacionado al trabajo", "Espalda", 0, 0),
    ]

    filas_eventos = []
    for i, mes in enumerate(MESES, start=1):
        # más eventos en los primeros meses para que la tendencia sea visible
        cantidad = rnd.randint(2, 6) if i <= 6 else rnd.randint(1, 4)
        for _ in range(cantidad):
            area, subarea, _ = rnd.choice(combinaciones)
            tipo, desc, parte, dias, cargados = rnd.choice(catalogo_eventos)
            filas_eventos.append({
                "fecha": f"2026-{i:02d}-{rnd.randint(1, 28):02d}",
                "mes": mes,
                "area": area,
                "subarea": subarea,
                "ges": rnd.choice(GES),
                "tipo_evento": tipo,
                "descripcion": desc,
                "parte_afectada": parte,
                "dias_perdidos": dias,
                "dias_cargados": cargados,
                "estado_investigacion": rnd.choice(["Cerrada", "Cerrada", "En proceso"]),
            })
    guardar("eventos", pd.DataFrame(filas_eventos))

    # --- Programas --------------------------------------------------------
    actividades = {
        "Inspecciones": ["Inspección planeada de taller", "Inspección de equipos de emergencia",
                         "Inspección preoperacional de montacargas"],
        "Simulacros": ["Simulacro de sismo", "Simulacro de incendio en taller",
                       "Simulacro de derrame de sustancias peligrosas"],
        "Salud ocupacional": ["Exámenes médicos ocupacionales", "Campaña de pausas activas",
                              "Evaluación de riesgo psicosocial"],
        "Monitoreos ocupacionales": ["Monitoreo de ruido", "Monitoreo de agentes químicos",
                                     "Evaluación ergonómica de puestos"],
        "Observaciones preventivas": ["Observación preventiva de conducta",
                                      "Reporte de actos y condiciones inseguras"],
        "Capacitación": ["Ejecución del programa anual de capacitación"],
    }

    filas_prog = []
    for mes in MESES:
        for tipo in TIPOS_PROGRAMA:
            for actividad in actividades[tipo]:
                for area, subarea, _ in rnd.sample(combinaciones, 4):
                    programado = rnd.randint(1, 4)
                    ejecutado = max(0, programado - rnd.choice([0, 0, 0, 1, 1, 2]))
                    filas_prog.append({
                        "mes": mes, "area": area, "subarea": subarea,
                        "tipo_programa": tipo, "actividad": actividad,
                        "programado": programado, "ejecutado": ejecutado,
                        "responsable": rnd.choice(["Jefe de SST", "Supervisor de área",
                                                   "CSST", "Médico ocupacional"]),
                    })
    guardar("programas", pd.DataFrame(filas_prog))

    # --- Capacitación -----------------------------------------------------
    temas = [
        "IPERC, actos y condiciones subestándar", "Uso correcto de EPP",
        "Manejo manual de cargas e higiene postural", "Riesgos químicos",
        "Primeros auxilios", "Protección auditiva", "Ergonomía y pausas activas",
        "Procedimiento frente a incidentes y accidentes", "Cuidado de manos",
    ]
    filas_cap = []
    for mes in MESES:
        for area, subarea, dotacion in rnd.sample(combinaciones, 5):
            convocados = rnd.randint(int(dotacion * 0.4), dotacion)
            capacitados = int(convocados * rnd.uniform(0.72, 0.99))
            aprobados = int(capacitados * rnd.uniform(0.80, 1.0))
            programadas = rnd.randint(1, 3)
            filas_cap.append({
                "mes": mes, "area": area, "subarea": subarea,
                "tema": rnd.choice(temas),
                "programadas": programadas,
                "ejecutadas": max(0, programadas - rnd.choice([0, 0, 1])),
                "trabajadores_convocados": convocados,
                "trabajadores_capacitados": capacitados,
                "trabajadores_aprobados": aprobados,
                "horas_dictadas": round(rnd.uniform(1.0, 3.0), 1),
            })
    guardar("capacitacion", pd.DataFrame(filas_cap))

    # --- Liderazgo --------------------------------------------------------
    act_liderazgo = [
        "Visita de gerencia a instalaciones (SST)",
        "Participación de jefaturas en inspecciones",
        "Charla de seguridad dictada por supervisor",
        "Reunión mensual de seguridad con la línea de mando",
    ]
    filas_lid = []
    for mes in MESES:
        for area in AREAS:
            for actividad in act_liderazgo:
                programado = rnd.randint(1, 3)
                filas_lid.append({
                    "mes": mes, "area": area, "actividad": actividad,
                    "programado": programado,
                    "ejecutado": max(0, programado - rnd.choice([0, 0, 0, 1])),
                    "responsable": rnd.choice(["Gerencia", "Jefatura de área",
                                               "Supervisor"]),
                })
    guardar("liderazgo", pd.DataFrame(filas_lid))

    # --- Gestión del sistema ---------------------------------------------
    filas_gest = []
    creadas_acum = 0
    for mes in MESES:
        creadas = rnd.randint(4, 12)
        creadas_acum += creadas
        filas_gest.append({
            "mes": mes,
            "requisitos_legales_total": 34,
            "requisitos_legales_cumplidos": rnd.randint(30, 34),
            "procedimientos_total": 27,
            "procedimientos_revisados": rnd.randint(20, 27),
            "acciones_creadas": creadas,
            "acciones_cerradas": max(0, creadas - rnd.choice([0, 1, 1, 2, 3])),
        })
    guardar("gestion", pd.DataFrame(filas_gest))


def borrar_todo() -> None:
    """Elimina los archivos de datos. Útil para reiniciar una demostración."""
    for clave in ARCHIVOS:
        ruta = _ruta(clave)
        if os.path.exists(ruta):
            os.remove(ruta)
