from datetime import datetime
from basedatos_json import leer_json, guardar_json, generar_id

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_ASISTENCIA_ALUMNOS = "datos/asistencia_alumnos.json"


def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_plantillas(plantillas):
    print("\n=== PLANTILLAS DISPONIBLES ===")
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']} | "
                f"Plantilla: {plantilla['nombre_plantilla']}")

def mostrar_salones(salones, id_carrera):
    print("\n=== SALONES DE LA CARRERA ===")
    encontrados = 0

    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            encontrados += 1
            print(
                f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | "
                f"Turno: {salon['turno']}")

    if encontrados == 0:
        print("No hay salones para esta carrera.")


def obtener_horario(horarios, id_plantilla, id_salon):
    for horario in horarios:
        if (
            horario["estado"] == "Activo"
            and horario["id_plantilla"] == id_plantilla
            and horario["id_salon"] == id_salon):
            return horario
    return None

def mostrar_horario(horario):
    print("\n=== HORARIO DEL SALÓN ===")

    for dia in horario["dias_horas"]:
        print(
            f"{dia['orden']}. {dia['dia']} | "
            f"{dia['hora_inicio']} - {dia['hora_fin']}")

def obtener_alumnos_del_salon(alumnos, asignaciones, id_salon):
    resultado = []

    for asignacion in asignaciones:
        if asignacion["estado"] == "Activo" and asignacion["id_salon"] == id_salon:
            alumno = buscar_por_id(alumnos, "id_alumno", asignacion["id_alumno"])
            if alumno:
                resultado.append(alumno)
    return resultado


def asistencia_ya_registrada(asistencias, id_alumno, fecha, id_horario, orden_dia):
    for asistencia in asistencias:
        if (
            asistencia["estado"] == "Activo"
            and asistencia["id_alumno"] == id_alumno
            and asistencia["fecha"] == fecha
            and asistencia["id_horario"] == id_horario
            and asistencia["orden_dia"] == orden_dia):
            return True
    return False


def pedir_estado_asistencia(nombre_alumno):
    while True:
        print(f"\nAlumno: {nombre_alumno}")
        print("1. Presente")
        print("2. Tarde")
        print("3. Falta")
        print("4. Justificado")

        opcion = input("Seleccione estado: ")

        if opcion == "1":
            return "Presente"
        elif opcion == "2":
            return "Tarde"
        elif opcion == "3":
            return "Falta"
        elif opcion == "4":
            return "Justificado"
        else:
            print("Opción inválida.")

def registrar_asistencia_alumnos():
    print("\n====================================")
    print("     REGISTRAR ASISTENCIA ALUMNOS")
    print("====================================")

    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    horarios = leer_json(RUTA_HORARIOS)
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    asistencias = leer_json(RUTA_ASISTENCIA_ALUMNOS)

    if len(plantillas) == 0:
        print("Primero debe crear plantillas.")
        return

    if len(horarios) == 0:
        print("Primero debe configurar horarios.")
        return

    mostrar_plantillas(plantillas)

    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)

    if plantilla is None:
        print("Plantilla no válida.")
        return

    print(f"\nCarrera: {plantilla['nombre_carrera']}")

    mostrar_salones(salones, plantilla["id_carrera"])

    try:
        id_salon = int(input("\nIngrese ID de salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    salon = buscar_por_id(salones, "id_salon", id_salon)

    if salon is None or salon["id_carrera"] != plantilla["id_carrera"]:
        print("Salón no válido.")
        return

    horario = obtener_horario(horarios, id_plantilla, id_salon)

    if horario is None:
        print("Este salón no tiene horario configurado para esta plantilla.")
        return

    mostrar_horario(horario)

    try:
        orden_dia = int(input("\nSeleccione el número del día/horario: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    horario_dia = None

    for dia in horario["dias_horas"]:
        if dia["orden"] == orden_dia:
            horario_dia = dia
            break

    if horario_dia is None:
        print("Horario no válido.")
        return

    fecha = input("Fecha de asistencia (YYYY-MM-DD) o ENTER para hoy: ")

    if fecha.strip() == "":
        fecha = datetime.now().strftime("%Y-%m-%d")

    alumnos_salon = obtener_alumnos_del_salon(alumnos, asignaciones, id_salon)

    if len(alumnos_salon) == 0:
        print("No hay alumnos asignados a este salón.")
        return

    print("\n=== REGISTRO DE ASISTENCIA ===")

    for alumno in alumnos_salon:
        if asistencia_ya_registrada(
            asistencias,
            alumno["id_alumno"],
            fecha,
            horario["id_horario"],
            orden_dia):
            print(f"\n{alumno['nombres']} {alumno['apellidos']} ya tiene asistencia registrada.")
            continue

        estado_asistencia = pedir_estado_asistencia(
            alumno["nombres"] + " " + alumno["apellidos"])

        nueva_asistencia = {
            "id_asistencia_alumno": generar_id(asistencias, "id_asistencia_alumno"),
            "fecha": fecha,
            "id_plantilla": plantilla["id_plantilla"],
            "nombre_plantilla": plantilla["nombre_plantilla"],
            "id_carrera": plantilla["id_carrera"],
            "nombre_carrera": plantilla["nombre_carrera"],
            "id_salon": salon["id_salon"],
            "nombre_salon": salon["nombre_salon"],
            "turno": salon["turno"],
            "id_horario": horario["id_horario"],
            "orden_dia": horario_dia["orden"],
            "dia": horario_dia["dia"],
            "hora_inicio": horario_dia["hora_inicio"],
            "hora_fin": horario_dia["hora_fin"],
            "id_alumno": alumno["id_alumno"],
            "nombre_alumno": alumno["nombres"] + " " + alumno["apellidos"],
            "dni": alumno["dni"],
            "asistencia": estado_asistencia,
            "estado": "Activo"}

        asistencias.append(nueva_asistencia)
        guardar_json(RUTA_ASISTENCIA_ALUMNOS, asistencias)

    print("\nAsistencia de alumnos registrada correctamente.")