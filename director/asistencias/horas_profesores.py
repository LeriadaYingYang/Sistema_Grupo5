from datetime import datetime
from basedatos_json import leer_json

RUTA_ASISTENCIA_PROFESORES = "datos/asistencia_profesores.json"


def obtener_unicos(lista):
    resultado = []

    for item in lista:
        if item not in resultado:
            resultado.append(item)
    return resultado

def mostrar_profesores(asistencias):
    print("\n=== PROFESORES CON ASISTENCIA ===")

    profesores = []

    for asistencia in asistencias:
        if asistencia["estado"] == "Activo":
            profesor = {
                "id_profesor": asistencia["id_profesor"],
                "nombre_profesor": asistencia["nombre_profesor"]}

            if profesor not in profesores:
                profesores.append(profesor)
                print(f"ID: {profesor['id_profesor']} | {profesor['nombre_profesor']}")

def filtrar_por_profesor(asistencias, id_profesor):
    return [
        a for a in asistencias
        if a["estado"] == "Activo" and a["id_profesor"] == id_profesor]

def mostrar_plantillas(asistencias):
    print("\n=== PLANTILLAS REGISTRADAS ===")

    plantillas = []

    for a in asistencias:
        plantilla = {
            "id_plantilla": a["id_plantilla"],
            "nombre_plantilla": a["nombre_plantilla"]}

        if plantilla not in plantillas:
            plantillas.append(plantilla)
            print(f"ID: {plantilla['id_plantilla']} | {plantilla['nombre_plantilla']}")

def filtrar_por_plantilla(asistencias, id_plantilla):
    return [
        a for a in asistencias
        if a["id_plantilla"] == id_plantilla]

def mostrar_salones(asistencias):
    print("\n=== SALONES REGISTRADOS ===")

    salones = []

    for a in asistencias:
        salon = {
            "id_salon": a["id_salon"],
            "nombre_salon": a["nombre_salon"],
            "turno": a["turno"]}

        if salon not in salones:
            salones.append(salon)
            print(
                f"ID: {salon['id_salon']} | "
                f"{salon['nombre_salon']} | Turno: {salon['turno']}")

def filtrar_por_salon(asistencias, id_salon):
    return [
        a for a in asistencias
        if a["id_salon"] == id_salon]

def mostrar_modulos(asistencias):
    print("\n=== MÓDULOS REGISTRADOS ===")

    modulos = []

    for a in asistencias:
        modulo = {
            "id_modulo": a["id_modulo"],
            "nombre_modulo": a["nombre_modulo"],
            "nombre_unidad": a["nombre_unidad"]}

        if modulo not in modulos:
            modulos.append(modulo)
            print(
                f"ID: {modulo['id_modulo']} | "
                f"Unidad: {modulo['nombre_unidad']} | "
                f"Módulo: {modulo['nombre_modulo']}")

def filtrar_por_modulo(asistencias, id_modulo):
    return [
        a for a in asistencias
        if a["id_modulo"] == id_modulo]

def mostrar_detalle(asistencias):
    total = 0

    for a in asistencias:
        total += a["horas_trabajadas"]

        print("\n-----------------------------")
        print(f"Fecha: {a['fecha']}")
        print(f"Profesor: {a['nombre_profesor']}")
        print(f"Plantilla: {a['nombre_plantilla']}")
        print(f"Salón: {a['nombre_salon']} | Turno: {a['turno']}")
        print(f"Unidad: {a['nombre_unidad']}")
        print(f"Módulo: {a['nombre_modulo']}")
        print(f"Día: {a['dia']}")
        print(f"Entrada: {a['hora_entrada']}")
        print(f"Salida: {a['hora_salida']}")
        print(f"Horas: {a['horas_trabajadas']}")

    print(f"\nTOTAL DE HORAS: {round(total, 2)}")

def obtener_fechas_registradas(asistencias):
    fechas = []

    for a in asistencias:
        if a["fecha"] not in fechas:
            fechas.append(a["fecha"])

    return sorted(fechas)

def obtener_meses_registrados(asistencias):
    meses = []

    for a in asistencias:
        mes = a["fecha"][:7]
        if mes not in meses:
            meses.append(mes)

    return sorted(meses)

def ver_por_dia(asistencias):
    fechas = obtener_fechas_registradas(asistencias)

    if len(fechas) == 0:
        print("No hay fechas registradas.")
        return

    print("\n=== FECHAS REGISTRADAS ===")

    for i, fecha in enumerate(fechas, start=1):
        print(f"{i}. {fecha}")

    try:
        opcion = int(input("\nSeleccione una fecha: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    if opcion < 1 or opcion > len(fechas):
        print("Opción inválida.")
        return

    fecha_elegida = fechas[opcion - 1]

    resultado = [
        a for a in asistencias
        if a["fecha"] == fecha_elegida]

    print(f"\n=== HORAS DEL DÍA {fecha_elegida} ===")
    mostrar_detalle(resultado)


def obtener_semana_del_mes(fecha):
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
    return ((fecha_dt.day - 1) // 7) + 1


def ver_por_semana(asistencias):
    meses = obtener_meses_registrados(asistencias)

    if len(meses) == 0:
        print("No hay meses registrados.")
        return

    print("\n=== MESES REGISTRADOS ===")

    for i, mes in enumerate(meses, start=1):
        print(f"{i}. {mes}")

    try:
        opcion_mes = int(input("\nSeleccione un mes: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    if opcion_mes < 1 or opcion_mes > len(meses):
        print("Opción inválida.")
        return

    mes_elegido = meses[opcion_mes - 1]

    semanas = []

    for a in asistencias:
        if a["fecha"].startswith(mes_elegido):
            semana = obtener_semana_del_mes(a["fecha"])

            if semana not in semanas:
                semanas.append(semana)

    semanas = sorted(semanas)

    print("\n=== SEMANAS CON REGISTROS ===")

    for semana in semanas:
        print(f"{semana}. Semana {semana}")

    try:
        semana_elegida = int(input("\nSeleccione semana: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    resultado = []

    for a in asistencias:
        if (
            a["fecha"].startswith(mes_elegido)
            and obtener_semana_del_mes(a["fecha"]) == semana_elegida):
            resultado.append(a)

    if len(resultado) == 0:
        print("No hay registros para esa semana.")
        return

    print(f"\n=== HORAS DE {mes_elegido} - SEMANA {semana_elegida} ===")
    mostrar_detalle(resultado)

def ver_por_mes(asistencias):
    meses = obtener_meses_registrados(asistencias)

    if len(meses) == 0:
        print("No hay meses registrados.")
        return

    print("\n=== MESES REGISTRADOS ===")

    for i, mes in enumerate(meses, start=1):
        print(f"{i}. {mes}")

    try:
        opcion = int(input("\nSeleccione un mes: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    if opcion < 1 or opcion > len(meses):
        print("Opción inválida.")
        return

    mes_elegido = meses[opcion - 1]

    resultado = [
        a for a in asistencias
        if a["fecha"].startswith(mes_elegido)]

    print(f"\n=== HORAS DEL MES {mes_elegido} ===")
    mostrar_detalle(resultado)

def ver_horas_profesores():
    print("\n====================================")
    print("   HORAS TRABAJADAS DE PROFESORES")
    print("====================================")

    asistencias = leer_json(RUTA_ASISTENCIA_PROFESORES)

    if len(asistencias) == 0:
        print("No hay asistencias de profesores registradas.")
        return

    mostrar_profesores(asistencias)

    try:
        id_profesor = int(input("\nIngrese ID del profesor: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    asistencias_filtradas = filtrar_por_profesor(asistencias, id_profesor)

    if len(asistencias_filtradas) == 0:
        print("No hay registros para este profesor.")
        return

    mostrar_plantillas(asistencias_filtradas)

    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    asistencias_filtradas = filtrar_por_plantilla(asistencias_filtradas, id_plantilla)

    if len(asistencias_filtradas) == 0:
        print("No hay registros para esta plantilla.")
        return

    mostrar_salones(asistencias_filtradas)

    try:
        id_salon = int(input("\nIngrese ID de salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    asistencias_filtradas = filtrar_por_salon(asistencias_filtradas, id_salon)

    if len(asistencias_filtradas) == 0:
        print("No hay registros para este salón.")
        return

    mostrar_modulos(asistencias_filtradas)

    try:
        id_modulo = int(input("\nIngrese ID de módulo: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    asistencias_filtradas = filtrar_por_modulo(asistencias_filtradas, id_modulo)

    if len(asistencias_filtradas) == 0:
        print("No hay registros para este módulo.")
        return

    while True:
        print("""
====================================
      REPORTE DE HORAS PROFESOR
====================================

1. Ver por día registrado
2. Ver por semana del mes
3. Ver por mes completo
4. Volver
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_por_dia(asistencias_filtradas)

        elif opcion == "2":
            ver_por_semana(asistencias_filtradas)

        elif opcion == "3":
            ver_por_mes(asistencias_filtradas)

        elif opcion == "4":
            break

        else:
            print("Opción inválida.")