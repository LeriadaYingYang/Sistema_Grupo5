from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA_ALUMNOS = "datos/asistencia_alumnos.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_SALONES = "datos/salones.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"


def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_plantillas(plantillas):  #muestra las plantillas disponibles
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']} | "
                f"Plantilla: {plantilla['nombre_plantilla']}")

def mostrar_salones(salones, id_carrera):  #muestra los salones de la carrera
    imprimir_titulo("SALONES DE LA CARRERA")
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            print(
                f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | "
                f"Turno: {salon['turno']}")

def buscar_alumno_aproximado_en_asistencias(asistencias):  #busca alumnos por nombre o dni
    texto = input("\nIngrese nombre, apellido o DNI del alumno: ").lower()
    encontrados = []
    for asistencia in asistencias:
        nombre = asistencia["nombre_alumno"].lower()
        dni = asistencia["dni"]
        if texto in nombre or texto in dni:
            alumno = {
                "id_alumno": asistencia["id_alumno"],
                "nombre_alumno": asistencia["nombre_alumno"],
                "dni": asistencia["dni"]}
            if alumno not in encontrados:
                encontrados.append(alumno)
    if len(encontrados) == 0:
        print("No se encontraron alumnos.")
        return None
    imprimir_titulo("ALUMNOS ENCONTRADOS")
    for alumno in encontrados:
        print(
            f"ID: {alumno['id_alumno']} | "
            f"{alumno['nombre_alumno']} | "
            f"DNI: {alumno['dni']}")
    try:
        id_alumno = int(input("\nIngrese ID del alumno: "))
    except ValueError:
        print("Debe ingresar un número.")
        return None
    for alumno in encontrados:
        if alumno["id_alumno"] == id_alumno:
            return alumno
    print("Alumno no válido.")
    return None

def filtrar_por_plantilla_y_salon(asistencias):  #filtra asistencias por plantilla y salón
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    mostrar_plantillas(plantillas)
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return []
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None:
        print("Plantilla no válida.")
        return []
    mostrar_salones(salones, plantilla["id_carrera"])
    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return []
    salon = buscar_por_id(salones, "id_salon", id_salon)
    if salon is None or salon["id_carrera"] != plantilla["id_carrera"]:
        print("Salón no válido.")
        return []
    return [
        asistencia
        for asistencia in asistencias
        if asistencia["estado"] == "Activo"
        and asistencia["id_plantilla"] == id_plantilla
        and asistencia["id_salon"] == id_salon]

def imprimir_asistencia(asistencia):  #muestra el detalle de una asistencia
    print("\n-----------------------------")
    print(f"Fecha: {asistencia['fecha']}")
    print(f"Alumno: {asistencia['nombre_alumno']}")
    print(f"DNI: {asistencia['dni']}")
    print(f"Carrera: {asistencia['nombre_carrera']}")
    print(f"Plantilla: {asistencia['nombre_plantilla']}")
    print(f"Salón: {asistencia['nombre_salon']}")
    print(f"Turno: {asistencia['turno']}")
    print(f"Día: {asistencia['dia']}")
    print(f"Horario: {asistencia['hora_inicio']} - {asistencia['hora_fin']}")
    print(f"Asistencia: {asistencia['asistencia']}")

def ver_por_alumno():  #muestra asistencia de un alumno
    asistencias = leer_json(RUTA_ASISTENCIA_ALUMNOS)
    if len(asistencias) == 0:
        print("No hay asistencias registradas.")
        return
    alumno = buscar_alumno_aproximado_en_asistencias(asistencias)
    if alumno is None:
        return
    imprimir_titulo("ASISTENCIA DEL ALUMNO")
    encontrados = 0
    for asistencia in asistencias:
        if asistencia["estado"] == "Activo" and asistencia["id_alumno"] == alumno["id_alumno"]:
            encontrados += 1
            imprimir_asistencia(asistencia)
    if encontrados == 0:
        print("No hay asistencia para este alumno.")

def ver_por_salon():  #muestra asistencia por salón
    asistencias = leer_json(RUTA_ASISTENCIA_ALUMNOS)
    if len(asistencias) == 0:
        print("No hay asistencias registradas.")
        return
    asistencias_filtradas = filtrar_por_plantilla_y_salon(asistencias)
    if len(asistencias_filtradas) == 0:
        print("No hay asistencias para ese salón.")
        return
    fecha = input("\nFiltrar por fecha YYYY-MM-DD (ENTER para ver todas): ").strip()
    imprimir_titulo("ASISTENCIAS DEL SALÓN")
    encontrados = 0
    for asistencia in asistencias_filtradas:
        if fecha == "" or asistencia["fecha"] == fecha:
            encontrados += 1
            imprimir_asistencia(asistencia)
    if encontrados == 0:
        print("No hay asistencias con ese filtro.")

def ver_por_fecha():  #muestra asistencia por fecha
    asistencias = leer_json(RUTA_ASISTENCIA_ALUMNOS)
    if len(asistencias) == 0:
        print("No hay asistencias registradas.")
        return
    fecha = input("Ingrese fecha a buscar (YYYY-MM-DD): ")
    asistencias_fecha = [
        asistencia
        for asistencia in asistencias
        if asistencia["estado"] == "Activo"
        and asistencia["fecha"] == fecha]
    if len(asistencias_fecha) == 0:
        print("No hay asistencias en esa fecha.")
        return
    opcion = input("¿Desea buscar un alumno específico? (si/no): ").lower()
    if opcion == "si":
        alumno = buscar_alumno_aproximado_en_asistencias(asistencias_fecha)
        if alumno is None:
            return
        asistencias_fecha = [
            asistencia
            for asistencia in asistencias_fecha
            if asistencia["id_alumno"] == alumno["id_alumno"]]
    imprimir_titulo("ASISTENCIAS POR FECHA")
    for asistencia in asistencias_fecha:
        imprimir_asistencia(asistencia)

def ver_resumen_porcentaje():  # muestra resumen de asistencia
    asistencias = leer_json(RUTA_ASISTENCIA_ALUMNOS)
    if len(asistencias) == 0:
        print("No hay asistencias registradas.")
        return
    asistencias_filtradas = filtrar_por_plantilla_y_salon(asistencias)
    if len(asistencias_filtradas) == 0:
        print("No hay asistencias para ese filtro.")
        return
    opcion = input("¿Desea ver resumen de un alumno específico? (si/no): ").lower()
    if opcion == "si":
        alumno = buscar_alumno_aproximado_en_asistencias(asistencias_filtradas)
        if alumno is None:
            return
        asistencias_filtradas = [
            asistencia
            for asistencia in asistencias_filtradas
            if asistencia["id_alumno"] == alumno["id_alumno"]]
    imprimir_titulo("RESUMEN DE ASISTENCIA")
    resumen = {}
    for asistencia in asistencias_filtradas:
        if asistencia["estado"] != "Activo":
            continue
        id_alumno = asistencia["id_alumno"]
        if id_alumno not in resumen:
            resumen[id_alumno] = {
                "nombre_alumno": asistencia["nombre_alumno"],
                "total": 0,
                "presentes": 0,
                "tardes": 0,
                "faltas": 0,
                "justificados": 0}
        resumen[id_alumno]["total"] += 1
        if asistencia["asistencia"] == "Presente":
            resumen[id_alumno]["presentes"] += 1
        elif asistencia["asistencia"] == "Tarde":
            resumen[id_alumno]["tardes"] += 1
        elif asistencia["asistencia"] == "Falta":
            resumen[id_alumno]["faltas"] += 1
        elif asistencia["asistencia"] == "Justificado":
            resumen[id_alumno]["justificados"] += 1
    for datos in resumen.values():
        porcentaje = round(((datos["presentes"]+ datos["tardes"]+ datos["justificados"])/ datos["total"]) * 100,2)
        print("\n-----------------------------")
        print(f"Alumno: {datos['nombre_alumno']}")
        print(f"Total registros: {datos['total']}")
        print(f"Presentes: {datos['presentes']}")
        print(f"Tardes: {datos['tardes']}")
        print(f"Faltas: {datos['faltas']}")
        print(f"Justificados: {datos['justificados']}")
        print(f"Porcentaje asistencia: {porcentaje}%")

def menu_ver_asistencia_alumnos():  #muestra el menú de consultas de asistencia
    while True:
        print("""
--- VER ASISTENCIA DE ALUMNOS ---

1. Ver por alumno
2. Ver por salón
3. Ver por fecha
4. Ver resumen de asistencia
5. Volver
""")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            ver_por_alumno()
        elif opcion == "2":
            ver_por_salon()
        elif opcion == "3":
            ver_por_fecha()
        elif opcion == "4":
            ver_resumen_porcentaje()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")