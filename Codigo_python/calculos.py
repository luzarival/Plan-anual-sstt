"""
Cálculo de índices e indicadores de Seguridad y Salud en el Trabajo.

Las fórmulas de accidentabilidad reproducen las establecidas en el capítulo de
Estadísticas del Plan Anual de SST de Pana Autos (SO-SO07-DO-003):

    Índice de frecuencia (IF)      = (Acc. incapacitantes + Acc. fatales) x 10^6 / HH
    Índice de severidad (IS)       = (Días perdidos + días cargados) x 10^6 / HH
    Índice de accidentabilidad (IA)= (IF x IS) / 1000
    Tasa de prevalencia/incidencia = N.° de diagnósticos relacionados al trabajo x 100 / N.° trabajadores
    Indicador combinado            = (Insp. ejecutadas/programadas)*0,5 + (Obs. cerradas/totales)*0,5

Todas las funciones son puras: reciben números o DataFrames y no tocan disco ni
interfaz. Esto permite verificarlas con pruebas automáticas (ver test_calculos.py).
"""

from __future__ import annotations

import pandas as pd

from catalogos import EVENTOS_FRECUENCIA, METAS, UMBRAL_ALERTA


# ---------------------------------------------------------------------------
# Utilitario base
# ---------------------------------------------------------------------------

def porcentaje(numerador: float, denominador: float) -> float:
    """Porcentaje seguro: devuelve 0.0 si el denominador es cero o inválido."""
    try:
        if not denominador:
            return 0.0
        return round((float(numerador) / float(denominador)) * 100, 2)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0


# ---------------------------------------------------------------------------
# Índices de accidentabilidad
# ---------------------------------------------------------------------------

def indice_frecuencia(accidentes_incapacitantes: int, accidentes_fatales: int,
                      horas_hombre: float) -> float:
    if not horas_hombre:
        return 0.0
    total = float(accidentes_incapacitantes) + float(accidentes_fatales)
    return round(total * 1_000_000 / float(horas_hombre), 2)


def indice_severidad(dias_perdidos: float, dias_cargados: float,
                     horas_hombre: float) -> float:
    if not horas_hombre:
        return 0.0
    total = float(dias_perdidos) + float(dias_cargados)
    return round(total * 1_000_000 / float(horas_hombre), 2)


def indice_accidentabilidad(indice_frec: float, indice_sev: float) -> float:
    return round((float(indice_frec) * float(indice_sev)) / 1000, 2)


def tasa_incidencia_enfermedades(diagnosticos: int, n_trabajadores: int) -> float:
    """Tasa de prevalencia y/o incidencia de enfermedades relacionadas al trabajo."""
    return porcentaje(diagnosticos, n_trabajadores)


def indicador_combinado_inspecciones(insp_ejecutadas: int, insp_programadas: int,
                                     obs_cerradas: int, obs_totales: int) -> float:
    """Indicador ponderado 50/50 empleado por Pana Autos en sus objetivos."""
    parte_insp = porcentaje(insp_ejecutadas, insp_programadas) * 0.5
    parte_obs = porcentaje(obs_cerradas, obs_totales) * 0.5
    return round(parte_insp + parte_obs, 2)


# ---------------------------------------------------------------------------
# Agregación desde los registros
# ---------------------------------------------------------------------------

def _filtrar(df: pd.DataFrame, area=None, subarea=None, meses=None) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    if area and area != "Todas":
        out = out[out["area"] == area]
    if subarea and subarea != "Todas":
        out = out[out["subarea"] == subarea]
    if meses:
        out = out[out["mes"].isin(meses)]
    return out


def resumen_accidentabilidad(eventos: pd.DataFrame, horas: pd.DataFrame,
                             area=None, subarea=None, meses=None) -> dict:
    """Consolida los índices de resultado para el filtro indicado."""
    ev = _filtrar(eventos, area, subarea, meses)
    hh = _filtrar(horas, area, subarea, meses)

    horas_hombre = float(hh["horas_hombre"].sum()) if not hh.empty else 0.0
    n_trabajadores = int(hh["n_trabajadores"].max()) if not hh.empty else 0

    if ev.empty:
        conteo = {}
        dias_perdidos = 0.0
        dias_cargados = 0.0
    else:
        conteo = ev["tipo_evento"].value_counts().to_dict()
        dias_perdidos = float(ev["dias_perdidos"].sum())
        dias_cargados = float(ev["dias_cargados"].sum())

    incapacitantes = int(conteo.get("Accidente incapacitante", 0))
    fatales = int(conteo.get("Accidente mortal", 0))
    leves = int(conteo.get("Accidente leve", 0))
    incidentes = int(conteo.get("Incidente", 0)) + int(conteo.get("Incidente peligroso", 0))
    enfermedades = int(conteo.get("Enfermedad ocupacional", 0))

    i_f = indice_frecuencia(incapacitantes, fatales, horas_hombre)
    i_s = indice_severidad(dias_perdidos, dias_cargados, horas_hombre)

    return {
        "horas_hombre": horas_hombre,
        "n_trabajadores": n_trabajadores,
        "accidentes_incapacitantes": incapacitantes,
        "accidentes_mortales": fatales,
        "accidentes_leves": leves,
        "incidentes": incidentes,
        "enfermedades_ocupacionales": enfermedades,
        "dias_perdidos": dias_perdidos,
        "dias_cargados": dias_cargados,
        "indice_frecuencia": i_f,
        "indice_severidad": i_s,
        "indice_accidentabilidad": indice_accidentabilidad(i_f, i_s),
        "tasa_incidencia_enfermedades": tasa_incidencia_enfermedades(
            enfermedades, n_trabajadores),
    }


def resumen_programas(programas: pd.DataFrame, tipo: str | None = None,
                      area=None, subarea=None, meses=None) -> dict:
    """Cumplimiento de un programa: ejecutado sobre programado."""
    pr = _filtrar(programas, area, subarea, meses)
    if tipo and not pr.empty:
        pr = pr[pr["tipo_programa"] == tipo]

    programado = int(pr["programado"].sum()) if not pr.empty else 0
    ejecutado = int(pr["ejecutado"].sum()) if not pr.empty else 0
    return {
        "programado": programado,
        "ejecutado": ejecutado,
        "cumplimiento": porcentaje(ejecutado, programado),
    }


def serie_mensual_indices(eventos: pd.DataFrame, horas: pd.DataFrame,
                          orden_meses: list, area=None, subarea=None) -> pd.DataFrame:
    """Devuelve IF, IS e IA mes a mes para graficar tendencias."""
    filas = []
    for mes in orden_meses:
        r = resumen_accidentabilidad(eventos, horas, area, subarea, meses=[mes])
        filas.append({
            "Mes": mes,
            "Índice de frecuencia": r["indice_frecuencia"],
            "Índice de severidad": r["indice_severidad"],
            "Índice de accidentabilidad": r["indice_accidentabilidad"],
        })
    return pd.DataFrame(filas).set_index("Mes")


def comparativo_por_area(eventos: pd.DataFrame, horas: pd.DataFrame,
                         areas: list, meses=None) -> pd.DataFrame:
    """Compara los índices entre áreas para el periodo seleccionado."""
    filas = []
    for area in areas:
        r = resumen_accidentabilidad(eventos, horas, area=area, meses=meses)
        if r["horas_hombre"] == 0:
            continue
        filas.append({
            "Área": area,
            "Índice de frecuencia": r["indice_frecuencia"],
            "Índice de severidad": r["indice_severidad"],
            "Índice de accidentabilidad": r["indice_accidentabilidad"],
            "Horas-hombre": r["horas_hombre"],
        })
    return pd.DataFrame(filas)


def comparativo_por_subarea(eventos: pd.DataFrame, horas: pd.DataFrame,
                            subareas: list, meses=None) -> pd.DataFrame:
    filas = []
    for sub in subareas:
        r = resumen_accidentabilidad(eventos, horas, subarea=sub, meses=meses)
        if r["horas_hombre"] == 0:
            continue
        filas.append({
            "Subárea": sub,
            "Índice de frecuencia": r["indice_frecuencia"],
            "Índice de accidentabilidad": r["indice_accidentabilidad"],
            "Horas-hombre": r["horas_hombre"],
        })
    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# Evaluación contra metas
# ---------------------------------------------------------------------------

def evaluar_meta(clave: str, valor: float) -> str:
    """Clasifica un indicador como 'Cumple', 'En alerta' o 'No cumple'."""
    cfg = METAS.get(clave)
    if cfg is None:
        return "Sin meta"
    meta = float(cfg["meta"])
    valor = float(valor)

    if cfg["sentido"] == "mayor":
        if valor >= meta:
            return "Cumple"
        if valor >= meta * UMBRAL_ALERTA:
            return "En alerta"
        return "No cumple"

    # sentido == "menor": conviene un valor bajo
    if valor <= meta:
        return "Cumple"
    if valor <= meta / UMBRAL_ALERTA:
        return "En alerta"
    return "No cumple"


SEMAFORO = {"Cumple": "🟢", "En alerta": "🟡", "No cumple": "🔴", "Sin meta": "⚪"}


def tablero_indicadores(valores: dict) -> pd.DataFrame:
    """
    Construye el tablero completo de indicadores.
    'valores' es un diccionario {clave_indicador: valor_calculado}.
    """
    filas = []
    for clave, cfg in METAS.items():
        if clave not in valores:
            continue
        valor = round(float(valores[clave]), 2)
        estado = evaluar_meta(clave, valor)
        filas.append({
            "Familia": cfg["familia"],
            "Indicador": cfg["etiqueta"],
            "Valor": valor,
            "Unidad": cfg["unidad"],
            "Meta": cfg["meta"],
            "Estado": f"{SEMAFORO[estado]} {estado}",
        })
    return pd.DataFrame(filas)
