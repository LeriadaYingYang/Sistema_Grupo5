from datetime import datetime
from basedatos_json import leer_json, guardar_json, generar_id
from gestion_academica.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASISTENCIA_PROFESORES = "datos/asistencia_profesores.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_MODULOS = "datos/modulos.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_profesores(profesores):  #muestra los profesores disponibles
    imprimir_titulo("PROFESORES DISPONIBLES")
    for profesor in profesores:
        if profesor["estado"] == "Activo":
            print(f"ID: {profesor['id_profesor']} | {profesor['nombres']} {profesor['apellidos']}")

def obtener_asignaciones_profesor(asignaciones, id_profesor):  #obtiene las asignaciones del profesor
    resultado = []
    for asignacion in asignaciones:
        if asignacion["estado"] == "Activo" and asignacion["id_profesor"] == id_profesor:
            resultado.append(asignacion)
    return resultado

def mostrar_plantillas_del_profesor(plantillas, asignaciones_profesor):  #muestra plantillas del profesor
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    ids_carrera = []
    for asignacion in asignaciones_profesor:
        if asignacion["id_carrera"] not in ids_carrera:
            ids_carrera.append(asignacion["id_carrera"])
    encontrados = 0
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo" and plantilla["id_carrera"] in ids_carrera:
            encontrados += 1
            print(f"ID: {plantilla['id_plantilla']} | Carrera: {plantilla['nombre_carrera']} | Plantilla: {plantilla['nombre_plantilla']}")
    if encontrados == 0:
        print("No hay plantillas disponibles para este profesor.")

def mostrar_salones_profesor_por_plantilla(asignaciones_profesor, plantilla):  #muestra salones del profesor
    imprimir_titulo("SALONES DEL PROFESOR")
    encontrados = 0
    for asignacion in asignaciones_profesor:
        if asignacion["id_carrera"] == plantilla["id_carrera"]:
            encontrados += 1
            print(f"ID salón: {asignacion['id_salon']} | "
                f"Carrera: {asignacion['nombre_carrera']} | "
                f"Salón: {asignacion['nombre_salon']} | "
                f"Turno: {asignacion['turno']}")
    if encontrados == 0:
        print("El profesor no tiene salones para esta plantilla.")

def obtener_horario(horarios, id_plantilla, id_salon):  #obtiene el horario del salón
    for horario in horarios:
        if horario["estado"] == "Activo" and horario["id_plantilla"] == id_plantilla and horario["id_salon"] == id_salon:
            return horario
    return None

def mostrar_modulos(modulos, id_plantilla, id_salon):  #muestra los módulos disponibles
    imprimir_titulo("MÓDULOS DISPONIBLES")
    encontrados = 0
    for modulo in modulos:
        if (modulo["estado"] == "Activo"
            and modulo.get("id_plantilla") == id_plantilla
            and modulo.get("id_salon") == id_salon):
            encontrados += 1
            print(f"ID: {modulo['id_modulo']} | Unidad: {modulo['nombre_unidad']} | Módulo: {modulo['nombre_modulo']}")
    if encontrados == 0:
        print("No hay módulos registrados para esta plantilla y salón.")

def mostrar_horario(horario):  #muestra el horario del salón
    imprimir_titulo("HORARIO DEL SALÓN")
    for dia in horario["dias_horas"]:
        print(f"{dia['orden']}. {dia['dia']} | {dia['hora_inicio']} - {dia['hora_fin']}")

def asistencia_profesor_ya_registrada(asistencias, id_profesor, fecha, id_horario, orden_dia):  #verifica si ya existe asistencia
    for asistencia in asistencias:
        if (asistencia["estado"] == "Activo"
            and asistencia["id_profesor"] == id_profesor
            and asistencia["fecha"] == fecha
            and asistencia["id_horario"] == id_horario
            and asistencia["orden_dia"] == orden_dia):
            return True
    return False

def calcular_horas(hora_entrada, hora_salida):  #calcula horas trabajadas
    try:
        entrada = datetime.strptime(hora_entrada, "%H:%M")
        salida = datetime.strptime(hora_salida, "%H:%M")
        diferencia = salida - entrada
        horas = diferencia.total_seconds() / 3600
        if horas < 0:
            return 0
        return round(horas, 2)
    except ValueError:
        return 0

def registrar_asistencia_profesores():  #registra la asistencia de profesores
    imprimir_titulo("REGISTRAR ASISTENCIA PROFESORES")
    profesores = leer_json(RUTA_PROFESORES)
    asignaciones = leer_json(RUTA_PROFESORES_SALONES)
    plantillas = leer_json(RUTA_PLANTILLAS)
    horarios = leer_json(RUTA_HORARIOS)
    modulos = leer_json(RUTA_MODULOS)
    asistencias = leer_json(RUTA_ASISTENCIA_PROFESORES)
    if len(profesores) == 0:
        print("Primero debe registrar profesores.")
        return
    if len(asignaciones) == 0:
        print("Primero debe asignar profesores a salones.")
        return
    if len(plantillas) == 0:
        print("Primero debe crear plantillas académicas.")
        return
    if len(horarios) == 0:
        print("Primero debe configurar horarios.")
        return
    if len(modulos) == 0:
        print("Primero debe registrar módulos.")
        return
    mostrar_profesores(profesores)
    try:
        id_profesor = int(input("\nIngrese ID del profesor: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    profesor = buscar_por_id(profesores, "id_profesor", id_profesor)
    if profesor is None:
        print("Profesor no encontrado.")
        return
    asignaciones_profesor = obtener_asignaciones_profesor(asignaciones, id_profesor)
    if len(asignaciones_profesor) == 0:
        print("Este profesor no tiene salones asignados.")
        return
    mostrar_plantillas_del_profesor(plantillas, asignaciones_profesor)
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None:
        print("Plantilla no válida.")
        return
    mostrar_salones_profesor_por_plantilla(asignaciones_profesor, plantilla)
    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    asignacion_elegida = None
    for asignacion in asignaciones_profesor:
        if asignacion["id_salon"] == id_salon and asignacion["id_carrera"] == plantilla["id_carrera"]:
            asignacion_elegida = asignacion
            break
    if asignacion_elegida is None:
        print("El profesor no está asignado a ese salón para esta plantilla.")
        return
    horario = obtener_horario(horarios, id_plantilla, id_salon)
    if horario is None:
        print("Este salón no tiene horario configurado para esta plantilla.")
        return
    mostrar_modulos(modulos, id_plantilla, id_salon)
    try:
        id_modulo = int(input("\nIngrese ID de módulo: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    modulo = buscar_por_id(modulos, "id_modulo", id_modulo)
    if modulo is None or modulo.get("id_plantilla") != id_plantilla or modulo.get("id_salon") != id_salon:
        print("Módulo no válido.")
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
    if asistencia_profesor_ya_registrada(asistencias, profesor["id_profesor"], fecha, horario["id_horario"], orden_dia):
        print("Este profesor ya tiene asistencia registrada para este horario.")
        return
    hora_entrada = input("Hora de entrada real (HH:MM): ")
    hora_salida = input("Hora de salida real (HH:MM): ")
    horas_trabajadas = calcular_horas(hora_entrada, hora_salida)
    if horas_trabajadas == 0:
        print("Hora inválida o salida menor que entrada.")
        return
    nueva_asistencia = {
        "id_asistencia_profesor": generar_id(asistencias, "id_asistencia_profesor"),
        "fecha": fecha,
        "id_profesor": profesor["id_profesor"],
        "nombre_profesor": profesor["nombres"] + " " + profesor["apellidos"],
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera": asignacion_elegida["id_carrera"],
        "nombre_carrera": asignacion_elegida["nombre_carrera"],
        "id_salon": asignacion_elegida["id_salon"],
        "nombre_salon": asignacion_elegida["nombre_salon"],
        "turno": asignacion_elegida["turno"],
        "id_modulo": modulo["id_modulo"],
        "nombre_modulo": modulo["nombre_modulo"],
        "nombre_unidad": modulo["nombre_unidad"],
        "id_horario": horario["id_horario"],
        "orden_dia": horario_dia["orden"],
        "dia": horario_dia["dia"],
        "hora_programada_inicio": horario_dia["hora_inicio"],
        "hora_programada_fin": horario_dia["hora_fin"],
        "hora_entrada": hora_entrada,
        "hora_salida": hora_salida,
        "horas_trabajadas": horas_trabajadas,
        "estado": "Activo"}
    asistencias.append(nueva_asistencia)
    guardar_json(RUTA_ASISTENCIA_PROFESORES, asistencias)
    print("\nAsistencia del profesor registrada correctamente.")
    print(f"Profesor: {nueva_asistencia['nombre_profesor']}")
    print(f"Plantilla: {nueva_asistencia['nombre_plantilla']}")
    print(f"Salón: {nueva_asistencia['nombre_salon']} - {nueva_asistencia['turno']}")
    print(f"Módulo: {nueva_asistencia['nombre_modulo']}")
    print(f"Horas trabajadas: {nueva_asistencia['horas_trabajadas']}")