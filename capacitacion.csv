"""
Sistema de Gestión de Seguridad y Salud en el Trabajo — Pana Autos
Herramienta computacional para el procesamiento y análisis de indicadores SST.

Ejecución:
    streamlit run app.py

Trabajo académico. Los datos precargados son simulados.
"""

from __future__ import annotations

import datetime as dt

import pandas as pd
import streamlit as st

import calculos as calc
import datos as db
import plan as contenido_plan
from catalogos import (AREAS, GES, MESES, METAS, SUBAREAS, TIPOS_EVENTO,
                       TIPOS_PROGRAMA)

st.set_page_config(page_title="SG-SST Pana Autos", page_icon="🛠️", layout="wide")


# ---------------------------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------------------------

def cargar_todo() -> dict:
    return {clave: db.cargar(clave) for clave in db.ARCHIVOS}


if not db.hay_datos():
    db.generar_datos_ejemplo()

datos = cargar_todo()


# ---------------------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------------------

st.sidebar.title("SG-SST Pana Autos")
st.sidebar.caption("Periodo 2026")

seccion = st.sidebar.radio(
    "Secciones",
    ["Tablero general",
     "Plan Anual de SST",
     "Registro de accidentabilidad",
     "Horas-hombre y dotación",
     "Programas anuales",
     "Capacitación",
     "Liderazgo y gestión",
     "Indicadores y metas",
     "Datos y exportación"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filtros")
f_area = st.sidebar.selectbox("Área", ["Todas"] + AREAS)
subareas_disp = ["Todas"] + SUBAREAS
f_subarea = st.sidebar.selectbox("Subárea", subareas_disp)
f_meses = st.sidebar.multiselect("Meses", MESES, default=MESES)

if not f_meses:
    f_meses = MESES


# ---------------------------------------------------------------------------
# Cálculo del tablero de indicadores
# ---------------------------------------------------------------------------

def calcular_indicadores(datos: dict, area, subarea, meses) -> tuple[dict, dict]:
    """Devuelve (resumen_accidentabilidad, valores_para_tablero)."""
    resumen = calc.resumen_accidentabilidad(
        datos["eventos"], datos["horas"], area, subarea, meses)

    insp = calc.resumen_programas(datos["programas"], "Inspecciones", area, subarea, meses)
    obs = calc.resumen_programas(datos["programas"], "Observaciones preventivas",
                                 area, subarea, meses)
    sim = calc.resumen_programas(datos["programas"], "Simulacros", area, subarea, meses)

    # Capacitación
    cap = datos["capacitacion"]
    if not cap.empty:
        cap_f = cap[cap["mes"].isin(meses)]
        if area != "Todas":
            cap_f = cap_f[cap_f["area"] == area]
        if subarea != "Todas":
            cap_f = cap_f[cap_f["subarea"] == subarea]
    else:
        cap_f = cap

    cap_prog = int(cap_f["programadas"].sum()) if not cap_f.empty else 0
    cap_ejec = int(cap_f["ejecutadas"].sum()) if not cap_f.empty else 0
    convocados = int(cap_f["trabajadores_convocados"].sum()) if not cap_f.empty else 0
    capacitados = int(cap_f["trabajadores_capacitados"].sum()) if not cap_f.empty else 0
    aprobados = int(cap_f["trabajadores_aprobados"].sum()) if not cap_f.empty else 0
    horas_dictadas = float(cap_f["horas_dictadas"].sum()) if not cap_f.empty else 0.0

    # Liderazgo (registrado a nivel de área)
    lid = datos["liderazgo"]
    if not lid.empty:
        lid_f = lid[lid["mes"].isin(meses)]
        if area != "Todas":
            lid_f = lid_f[lid_f["area"] == area]
    else:
        lid_f = lid
    lid_prog = int(lid_f["programado"].sum()) if not lid_f.empty else 0
    lid_ejec = int(lid_f["ejecutado"].sum()) if not lid_f.empty else 0

    # Gestión del sistema (a nivel compañía)
    ges = datos["gestion"]
    ges_f = ges[ges["mes"].isin(meses)] if not ges.empty else ges
    if not ges_f.empty:
        req_total = int(ges_f["requisitos_legales_total"].mean())
        req_cumpl = int(ges_f["requisitos_legales_cumplidos"].mean())
        proc_total = int(ges_f["procedimientos_total"].mean())
        proc_rev = int(ges_f["procedimientos_revisados"].mean())
        acc_creadas = int(ges_f["acciones_creadas"].sum())
        acc_cerradas = int(ges_f["acciones_cerradas"].sum())
    else:
        req_total = req_cumpl = proc_total = proc_rev = acc_creadas = acc_cerradas = 0

    valores = {
        "indice_accidentabilidad": resumen["indice_accidentabilidad"],
        "cumplimiento_inspecciones": insp["cumplimiento"],
        "cierre_observaciones": obs["cumplimiento"],
        "indicador_combinado_inspecciones": calc.indicador_combinado_inspecciones(
            insp["ejecutado"], insp["programado"], obs["ejecutado"], obs["programado"]),
        "cierre_acciones_correctivas": calc.porcentaje(acc_cerradas, acc_creadas),
        "cumplimiento_capacitacion": calc.porcentaje(cap_ejec, cap_prog),
        "cobertura_capacitacion": calc.porcentaje(capacitados, convocados),
        "eficacia_capacitacion": calc.porcentaje(aprobados, capacitados),
        "horas_capacitacion_trabajador": round(
            horas_dictadas / resumen["n_trabajadores"], 2) if resumen["n_trabajadores"] else 0.0,
        "cumplimiento_simulacros": sim["cumplimiento"],
        "brigadistas_capacitados": calc.porcentaje(aprobados, capacitados),
        "equipos_emergencia_operativos": insp["cumplimiento"],
        "cumplimiento_liderazgo": calc.porcentaje(lid_ejec, lid_prog),
        "cumplimiento_legal": calc.porcentaje(req_cumpl, req_total),
        "procedimientos_revisados": calc.porcentaje(proc_rev, proc_total),
    }
    return resumen, valores


resumen, valores = calcular_indicadores(datos, f_area, f_subarea, f_meses)


# ---------------------------------------------------------------------------
# Secciones
# ---------------------------------------------------------------------------

if seccion == "Tablero general":
    st.title("Tablero de indicadores SST")
    st.caption(f"Área: {f_area} · Subárea: {f_subarea} · {len(f_meses)} mes(es) seleccionado(s)")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Índice de frecuencia", resumen["indice_frecuencia"])
    c2.metric("Índice de severidad", resumen["indice_severidad"])
    c3.metric("Índice de accidentabilidad", resumen["indice_accidentabilidad"])
    c4.metric("Horas-hombre", f"{resumen['horas_hombre']:,.0f}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accidentes incapacitantes", resumen["accidentes_incapacitantes"])
    c2.metric("Accidentes leves", resumen["accidentes_leves"])
    c3.metric("Incidentes", resumen["incidentes"])
    c4.metric("Días perdidos", int(resumen["dias_perdidos"]))

    st.markdown("---")
    st.subheader("Indicadores bajo meta")
    tablero = calc.tablero_indicadores(valores)
    bajo_meta = tablero[tablero["Estado"].str.contains("No cumple|En alerta")]
    if bajo_meta.empty:
        st.success("Todos los indicadores del filtro seleccionado se encuentran en meta.")
    else:
        st.dataframe(bajo_meta, width="stretch", hide_index=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Tendencia mensual")
        serie = calc.serie_mensual_indices(
            datos["eventos"], datos["horas"], MESES,
            None if f_area == "Todas" else f_area,
            None if f_subarea == "Todas" else f_subarea)
        st.line_chart(serie[["Índice de frecuencia", "Índice de accidentabilidad"]])

    with col_b:
        st.subheader("Comparación entre áreas")
        comp = calc.comparativo_por_area(datos["eventos"], datos["horas"], AREAS, f_meses)
        if comp.empty:
            st.info("No hay datos para el periodo seleccionado.")
        else:
            st.bar_chart(comp.set_index("Área")["Índice de frecuencia"])

    st.subheader("Comparación entre subáreas")
    comp_sub = calc.comparativo_por_subarea(datos["eventos"], datos["horas"], SUBAREAS, f_meses)
    if comp_sub.empty:
        st.info("No hay datos para el periodo seleccionado.")
    else:
        st.bar_chart(comp_sub.set_index("Subárea")["Índice de accidentabilidad"])


elif seccion == "Plan Anual de SST":
    st.title("Plan Anual de Seguridad y Salud en el Trabajo")
    st.caption("Pana Autos — Periodo 2026")

    t1, t2, t3 = st.tabs(["Estructura del Plan", "Objetivos, metas e indicadores", "Fórmulas"])

    with t1:
        st.markdown("#### Cuerpo del Plan")
        for capitulo, subcapitulos in contenido_plan.ESTRUCTURA_PLAN:
            if subcapitulos:
                with st.expander(capitulo):
                    for s in subcapitulos:
                        st.write(s)
            else:
                st.markdown(f"**{capitulo}**")
        st.markdown("#### Anexos")
        for a in contenido_plan.ANEXOS_PLAN:
            st.write(a)

    with t2:
        st.markdown(
            "Cada objetivo del Plan está asociado a un indicador que este "
            "aplicativo calcula automáticamente a partir de los registros.")
        filas = []
        for o in contenido_plan.OBJETIVOS:
            valor = valores.get(o["clave"])
            estado = calc.evaluar_meta(o["clave"], valor) if valor is not None else "Sin dato"
            filas.append({
                "Objetivo": o["objetivo"],
                "Meta": o["meta"],
                "Indicador": o["indicador"],
                "Valor actual": valor,
                "Estado": f"{calc.SEMAFORO.get(estado, '⚪')} {estado}",
                "Responsable": o["responsable"],
            })
        st.dataframe(pd.DataFrame(filas), width="stretch", hide_index=True)

    with t3:
        st.markdown("Fórmulas empleadas por el aplicativo:")
        for nombre, formula in contenido_plan.FORMULAS:
            st.markdown(f"**{nombre}**")
            st.code(formula, language=None)


elif seccion == "Registro de accidentabilidad":
    st.title("Registro de incidentes, accidentes y enfermedades ocupacionales")

    with st.form("form_evento", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        fecha = c1.date_input("Fecha del evento", value=dt.date(2026, 1, 15))
        mes = c2.selectbox("Mes de reporte", MESES)
        tipo = c3.selectbox("Tipo de evento", TIPOS_EVENTO)

        c1, c2, c3 = st.columns(3)
        area = c1.selectbox("Área", AREAS)
        subarea = c2.selectbox("Subárea", SUBAREAS)
        ges = c3.selectbox("Grupo de exposición similar", GES)

        descripcion = st.text_input("Descripción del evento")

        c1, c2, c3, c4 = st.columns(4)
        parte = c1.text_input("Parte del cuerpo afectada", value="No aplica")
        dias_perdidos = c2.number_input("Días perdidos", min_value=0, value=0)
        dias_cargados = c3.number_input("Días cargados", min_value=0, value=0)
        estado_inv = c4.selectbox("Investigación", ["Pendiente", "En proceso", "Cerrada"])

        if st.form_submit_button("Registrar evento"):
            db.agregar_fila("eventos", {
                "fecha": fecha.isoformat(), "mes": mes, "area": area, "subarea": subarea,
                "ges": ges, "tipo_evento": tipo, "descripcion": descripcion,
                "parte_afectada": parte, "dias_perdidos": dias_perdidos,
                "dias_cargados": dias_cargados, "estado_investigacion": estado_inv,
            })
            st.success("Evento registrado. Los indicadores se recalcularon.")
            st.rerun()

    st.markdown("---")
    st.subheader("Índices calculados con el filtro actual")
    c1, c2, c3 = st.columns(3)
    c1.metric("Índice de frecuencia", resumen["indice_frecuencia"])
    c2.metric("Índice de severidad", resumen["indice_severidad"])
    c3.metric("Índice de accidentabilidad", resumen["indice_accidentabilidad"])

    st.subheader("Eventos registrados")
    ev = datos["eventos"]
    if not ev.empty:
        ev_f = ev[ev["mes"].isin(f_meses)]
        if f_area != "Todas":
            ev_f = ev_f[ev_f["area"] == f_area]
        if f_subarea != "Todas":
            ev_f = ev_f[ev_f["subarea"] == f_subarea]
        st.dataframe(ev_f, width="stretch", hide_index=True)

        st.markdown("**Distribución por tipo de evento**")
        st.bar_chart(ev_f["tipo_evento"].value_counts())

        st.markdown("**Distribución por parte del cuerpo afectada**")
        partes = ev_f[ev_f["parte_afectada"] != "No aplica"]["parte_afectada"].value_counts()
        if not partes.empty:
            st.bar_chart(partes)
    else:
        st.info("Aún no hay eventos registrados.")


elif seccion == "Horas-hombre y dotación":
    st.title("Horas-hombre trabajadas y dotación")
    st.caption("Base de cálculo de todos los índices de resultado.")

    with st.form("form_horas", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        mes = c1.selectbox("Mes", MESES)
        area = c2.selectbox("Área", AREAS)
        subarea = c3.selectbox("Subárea", SUBAREAS)
        c1, c2 = st.columns(2)
        n_trab = c1.number_input("N.° de trabajadores", min_value=0, value=40)
        hh = c2.number_input("Horas-hombre trabajadas", min_value=0.0, value=7600.0, step=100.0)
        if st.form_submit_button("Registrar"):
            db.agregar_fila("horas", {
                "mes": mes, "area": area, "subarea": subarea,
                "n_trabajadores": n_trab, "horas_hombre": hh})
            st.success("Registro guardado.")
            st.rerun()

    st.subheader("Registros")
    st.dataframe(datos["horas"], width="stretch", hide_index=True)

    if not datos["horas"].empty:
        hh_mes = (datos["horas"].groupby("mes")["horas_hombre"].sum()
                  .reindex(MESES).fillna(0))
        st.subheader("Horas-hombre por mes")
        st.bar_chart(hh_mes)


elif seccion == "Programas anuales":
    st.title("Programas anuales de SST")
    st.caption("Inspecciones, simulacros, salud ocupacional, monitoreos y observaciones.")

    with st.form("form_programa", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        mes = c1.selectbox("Mes", MESES)
        area = c2.selectbox("Área", AREAS)
        subarea = c3.selectbox("Subárea", SUBAREAS)
        c1, c2 = st.columns(2)
        tipo = c1.selectbox("Programa", TIPOS_PROGRAMA)
        actividad = c2.text_input("Actividad")
        c1, c2, c3 = st.columns(3)
        programado = c1.number_input("Programado", min_value=0, value=1)
        ejecutado = c2.number_input("Ejecutado", min_value=0, value=0)
        responsable = c3.text_input("Responsable", value="Jefe de SST")
        if st.form_submit_button("Registrar actividad"):
            db.agregar_fila("programas", {
                "mes": mes, "area": area, "subarea": subarea, "tipo_programa": tipo,
                "actividad": actividad, "programado": programado,
                "ejecutado": ejecutado, "responsable": responsable})
            st.success("Actividad registrada.")
            st.rerun()

    st.markdown("---")
    st.subheader("Cumplimiento por programa")
    filas = []
    for tipo in TIPOS_PROGRAMA:
        r = calc.resumen_programas(
            datos["programas"], tipo,
            None if f_area == "Todas" else f_area,
            None if f_subarea == "Todas" else f_subarea, f_meses)
        filas.append({"Programa": tipo, "Programado": r["programado"],
                      "Ejecutado": r["ejecutado"], "Cumplimiento (%)": r["cumplimiento"]})
    df_cump = pd.DataFrame(filas)
    st.dataframe(df_cump, width="stretch", hide_index=True)
    st.bar_chart(df_cump.set_index("Programa")["Cumplimiento (%)"])

    st.subheader("Detalle de actividades")
    st.dataframe(datos["programas"], width="stretch", hide_index=True)


elif seccion == "Capacitación":
    st.title("Programa Anual de Capacitación en SST")
    st.caption("Se mide cumplimiento, cobertura y eficacia, no solo la cantidad de charlas.")

    with st.form("form_cap", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        mes = c1.selectbox("Mes", MESES)
        area = c2.selectbox("Área", AREAS)
        subarea = c3.selectbox("Subárea", SUBAREAS)
        tema = st.text_input("Tema de la capacitación")
        c1, c2, c3 = st.columns(3)
        programadas = c1.number_input("Capacitaciones programadas", min_value=0, value=1)
        ejecutadas = c2.number_input("Capacitaciones ejecutadas", min_value=0, value=1)
        horas = c3.number_input("Horas dictadas", min_value=0.0, value=2.0, step=0.5)
        c1, c2, c3 = st.columns(3)
        convocados = c1.number_input("Trabajadores convocados", min_value=0, value=30)
        capacitados = c2.number_input("Trabajadores capacitados", min_value=0, value=27)
        aprobados = c3.number_input("Trabajadores aprobados", min_value=0, value=24)
        if st.form_submit_button("Registrar capacitación"):
            db.agregar_fila("capacitacion", {
                "mes": mes, "area": area, "subarea": subarea, "tema": tema,
                "programadas": programadas, "ejecutadas": ejecutadas,
                "trabajadores_convocados": convocados,
                "trabajadores_capacitados": capacitados,
                "trabajadores_aprobados": aprobados, "horas_dictadas": horas})
            st.success("Capacitación registrada.")
            st.rerun()

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cumplimiento del programa", f"{valores['cumplimiento_capacitacion']} %")
    c2.metric("Cobertura", f"{valores['cobertura_capacitacion']} %")
    c3.metric("Eficacia", f"{valores['eficacia_capacitacion']} %")
    c4.metric("Horas por trabajador", valores["horas_capacitacion_trabajador"])

    st.subheader("Registros de capacitación")
    st.dataframe(datos["capacitacion"], width="stretch", hide_index=True)


elif seccion == "Liderazgo y gestión":
    st.title("Liderazgo, participación y gestión del sistema")

    t1, t2 = st.tabs(["Liderazgo de la línea de mando", "Gestión del SG-SST"])

    with t1:
        st.caption("Indicadores inspirados en los KPI de liderazgo de los planes mineros, "
                   "adaptados a la realidad de Pana Autos.")
        with st.form("form_lid", clear_on_submit=True):
            c1, c2 = st.columns(2)
            mes = c1.selectbox("Mes", MESES)
            area = c2.selectbox("Área", AREAS)
            actividad = st.text_input("Actividad de liderazgo")
            c1, c2, c3 = st.columns(3)
            programado = c1.number_input("Programado", min_value=0, value=1)
            ejecutado = c2.number_input("Ejecutado", min_value=0, value=1)
            responsable = c3.text_input("Responsable", value="Jefatura de área")
            if st.form_submit_button("Registrar"):
                db.agregar_fila("liderazgo", {
                    "mes": mes, "area": area, "actividad": actividad,
                    "programado": programado, "ejecutado": ejecutado,
                    "responsable": responsable})
                st.success("Actividad registrada.")
                st.rerun()

        st.metric("Cumplimiento de actividades de liderazgo",
                  f"{valores['cumplimiento_liderazgo']} %")
        lid = datos["liderazgo"]
        if not lid.empty:
            resumen_lid = (lid.groupby("actividad")[["programado", "ejecutado"]]
                           .sum().reset_index())
            resumen_lid["Cumplimiento (%)"] = resumen_lid.apply(
                lambda r: calc.porcentaje(r["ejecutado"], r["programado"]), axis=1)
            st.dataframe(resumen_lid, width="stretch", hide_index=True)

    with t2:
        with st.form("form_gest", clear_on_submit=True):
            mes = st.selectbox("Mes", MESES)
            c1, c2 = st.columns(2)
            req_total = c1.number_input("Requisitos legales totales", min_value=0, value=34)
            req_cumpl = c2.number_input("Requisitos legales cumplidos", min_value=0, value=32)
            c1, c2 = st.columns(2)
            proc_total = c1.number_input("Procedimientos del SG-SST", min_value=0, value=27)
            proc_rev = c2.number_input("Procedimientos revisados", min_value=0, value=24)
            c1, c2 = st.columns(2)
            acc_creadas = c1.number_input("Acciones (OPS/NC) creadas", min_value=0, value=8)
            acc_cerradas = c2.number_input("Acciones (OPS/NC) cerradas", min_value=0, value=7)
            if st.form_submit_button("Registrar"):
                db.agregar_fila("gestion", {
                    "mes": mes, "requisitos_legales_total": req_total,
                    "requisitos_legales_cumplidos": req_cumpl,
                    "procedimientos_total": proc_total,
                    "procedimientos_revisados": proc_rev,
                    "acciones_creadas": acc_creadas, "acciones_cerradas": acc_cerradas})
                st.success("Registro guardado.")
                st.rerun()

        c1, c2, c3 = st.columns(3)
        c1.metric("Cumplimiento legal", f"{valores['cumplimiento_legal']} %")
        c2.metric("Procedimientos revisados", f"{valores['procedimientos_revisados']} %")
        c3.metric("Cierre de acciones", f"{valores['cierre_acciones_correctivas']} %")
        st.dataframe(datos["gestion"], width="stretch", hide_index=True)


elif seccion == "Indicadores y metas":
    st.title("Sistema de indicadores SST")
    st.caption("Seis familias de indicadores, evaluadas contra las metas del Plan Anual.")

    tablero = calc.tablero_indicadores(valores)
    for familia in ["Resultado", "Preventivo", "Capacitación", "Emergencias",
                    "Liderazgo", "Gestión"]:
        sub = tablero[tablero["Familia"] == familia]
        if sub.empty:
            continue
        st.subheader(f"Indicadores de {familia.lower()}")
        st.dataframe(sub.drop(columns=["Familia"]), width="stretch",
                     hide_index=True)

    st.markdown("---")
    st.subheader("Criterio de evaluación")
    st.markdown(
        "- 🟢 **Cumple**: el indicador alcanza la meta establecida.\n"
        "- 🟡 **En alerta**: se encuentra dentro del 15 % por debajo de la meta.\n"
        "- 🔴 **No cumple**: se encuentra por debajo de ese umbral.\n\n"
        "En los indicadores donde conviene un valor bajo, como el índice de "
        "accidentabilidad, el criterio se aplica en sentido inverso.")


elif seccion == "Datos y exportación":
    st.title("Datos y exportación")
    st.caption("Los registros se almacenan en archivos CSV dentro de la carpeta /datos.")

    nombres = {
        "eventos": "Eventos (incidentes y accidentes)",
        "horas": "Horas-hombre y dotación",
        "programas": "Programas anuales",
        "capacitacion": "Capacitación",
        "liderazgo": "Liderazgo",
        "gestion": "Gestión del sistema",
    }

    for clave, etiqueta in nombres.items():
        df = datos[clave]
        with st.expander(f"{etiqueta} — {len(df)} registros"):
            st.dataframe(df, width="stretch", hide_index=True)
            st.download_button(
                f"Descargar {clave}.csv",
                df.to_csv(index=False).encode("utf-8"),
                file_name=f"{clave}.csv", mime="text/csv", key=f"dl_{clave}")

    st.markdown("---")
    st.subheader("Reporte consolidado de indicadores")
    tablero = calc.tablero_indicadores(valores)
    st.download_button(
        "Descargar tablero de indicadores (CSV)",
        tablero.to_csv(index=False).encode("utf-8"),
        file_name="tablero_indicadores.csv", mime="text/csv")

    st.markdown("---")
    st.subheader("Mantenimiento")
    c1, c2 = st.columns(2)
    if c1.button("Restaurar datos de ejemplo"):
        db.borrar_todo()
        db.generar_datos_ejemplo()
        st.success("Datos de ejemplo restaurados.")
        st.rerun()
    if c2.button("Borrar todos los datos"):
        db.borrar_todo()
        st.warning("Datos eliminados. Al recargar se generarán datos de ejemplo.")
        st.rerun()


st.sidebar.markdown("---")
st.sidebar.caption(
    "Trabajo académico. Los datos precargados son simulados y no corresponden "
    "a la operación real de Pana Autos.")
