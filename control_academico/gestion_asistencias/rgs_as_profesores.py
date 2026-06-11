from datetime import datetime
from basedatos_json import leer_json,guardar_json,generar_id
from control_academico.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASISTENCIAS = "datos/asistencia_profesores.json"

def cargar_datos():
    return (leer_json(RUTA_PROFESORES),leer_json(RUTA_MODULOS),leer_json(RUTA_HORARIOS),leer_json(RUTA_ASISTENCIAS))

def buscar_por_id(lista, campo_id, valor_id):
    return next(
        (item for item in lista
            if item[campo_id] == valor_id and item["estado"] == "Activo"),None)

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero.")

def pedir_fecha():
    while True:
        fecha = input("Ingrese fecha (AAAA-MM-DD): ").strip()
        try:
            datetime.strptime(fecha,"%Y-%m-%d")
            return fecha
        except ValueError:
            print("Formato inválido. Use AAAA-MM-DD.")

def validar_hora(hora):
    try:
        datetime.strptime(hora,"%H:%M")
        return True
    except ValueError:
        return False

def pedir_hora(mensaje):
    while True:
        hora = input(mensaje).strip()
        if validar_hora(hora):
            return hora
        print("Formato inválido. Use HH:MM.")

def mostrar_profesores(profesores):
    imprimir_titulo("=== PROFESORES DISPONIBLES ===")
    profesores_activos = [profesor for profesor in profesores
        if profesor["estado"] == "Activo"]
    if not profesores_activos:
        print("No existen profesores registrados.")
        return False
    for profesor in profesores_activos:
        print(f"ID: {profesor['id_profesor']} | "
            f"{profesor['nombres']} "
            f"{profesor['apellidos']}")
    return True

def mostrar_modulos(modulos):
    imprimir_titulo("=== MÓDULOS DISPONIBLES ===")
    modulos_activos = [modulo for modulo in modulos
        if modulo["estado"] == "Activo"]
    if not modulos_activos:
        print("No existen módulos registrados.")
        return False
    for modulo in modulos_activos:
        print(f"ID: {modulo['id_modulo']} | "
            f"Unidad: "
            f"{modulo['nombre_unidad']} | "
            f"Módulo: "
            f"{modulo['nombre_modulo']}")
    return True

def mostrar_horarios(horarios):
    imprimir_titulo("=== HORARIOS DISPONIBLES ===")
    horarios_activos = [horario for horario in horarios
        if horario["estado"] == "Activo"]
    if not horarios_activos:
        print("No existen horarios configurados.")
        return False
    for horario in horarios_activos:
        print(f"ID: {horario['id_horario']} | "
            f"{horario['nombre_carrera']} | "
            f"{horario['nombre_salon']} | "
            f"{horario['turno']}")
    return True

def mostrar_dias_horario(horario):
    imprimir_titulo("=== DÍAS DEL HORARIO ===")
    for dia in horario["dias_horas"]:
        print(f"{dia['orden']}. "
            f"{dia['dia']} | "
            f"{dia['hora_inicio']} - "
            f"{dia['hora_fin']}")

def obtener_dia_horario(horario,orden_dia):
    return next((dia for dia in horario["dias_horas"]
            if dia["orden"] == orden_dia),None)

def calcular_horas_trabajadas(hora_entrada,hora_salida):
    entrada = datetime.strptime(hora_entrada,"%H:%M")
    salida = datetime.strptime(hora_salida,"%H:%M")
    return round((salida - entrada).total_seconds() / 3600,2)

def asistencia_ya_registrada(asistencias,fecha,id_profesor,id_horario,orden_dia):
    return any(asistencia["estado"] == "Activo" and asistencia["fecha"] == fecha and asistencia["id_profesor"]
        == id_profesor and asistencia["id_horario"] == id_horario and asistencia["orden_dia"]
        == orden_dia for asistencia in asistencias)

def crear_asistencia_profesor(asistencias,profesor,modulo,horario,dia_horario,fecha,hora_entrada,hora_salida):
    horas_trabajadas = (calcular_horas_trabajadas(hora_entrada,hora_salida))
    return {"id_asistencia_profesor":generar_id(asistencias,"id_asistencia_profesor"),
        "fecha": fecha,
        "id_profesor":profesor["id_profesor"],
        "nombre_profesor":f"{profesor['nombres']} "f"{profesor['apellidos']}",
        "id_plantilla":horario["id_plantilla"],
        "nombre_plantilla":horario["nombre_plantilla"],
        "id_carrera":horario["id_carrera"],
        "nombre_carrera":horario["nombre_carrera"],
        "id_salon":horario["id_salon"],
        "nombre_salon":horario["nombre_salon"],
        "turno":horario["turno"],
        "id_modulo":modulo["id_modulo"],
        "nombre_modulo":modulo["nombre_modulo"],
        "nombre_unidad":modulo["nombre_unidad"],
        "id_horario":horario["id_horario"],
        "orden_dia":dia_horario["orden"],
        "dia":dia_horario["dia"],
        "hora_programada_inicio":dia_horario["hora_inicio"],
        "hora_programada_fin":dia_horario["hora_fin"],
        "hora_entrada":hora_entrada,
        "hora_salida":hora_salida,
        "horas_trabajadas":horas_trabajadas,
        "estado":"Activo"}

def registrar_asistencia_profesores():
    imprimir_titulo("=== REGISTRAR ASISTENCIA PROFESORES ===")
    (profesores,modulos,horarios,asistencias) = cargar_datos()
    if not mostrar_profesores(profesores):
        return
    id_profesor = pedir_entero("\nIngrese ID profesor: ")
    profesor = buscar_por_id(profesores,"id_profesor",id_profesor)
    if profesor is None:
        print("Profesor no encontrado.")
        return
    if not mostrar_modulos(modulos):
        return
    id_modulo = pedir_entero("\nIngrese ID módulo: ")
    modulo = buscar_por_id(modulos,"id_modulo",id_modulo)
    if modulo is None:
        print("Módulo no encontrado.")
        return
    if not mostrar_horarios(horarios):
        return
    id_horario = pedir_entero("\nIngrese ID horario: ")
    horario = buscar_por_id(horarios,"id_horario",id_horario)
    if horario is None:
        print("Horario no encontrado.")
        return
    mostrar_dias_horario(horario)
    orden_dia = pedir_entero("\nSeleccione día: ")
    dia_horario = (
        obtener_dia_horario(horario,orden_dia))
    if dia_horario is None:
        print("Día inválido.")
        return
    fecha = pedir_fecha()
    hora_entrada = pedir_hora("Hora de entrada (HH:MM): ")
    hora_salida = pedir_hora("Hora de salida (HH:MM): ")
    if calcular_horas_trabajadas(hora_entrada,hora_salida) <= 0:
        print("La hora de salida debe ser mayor que la hora de entrada.")
        return
    if asistencia_ya_registrada(asistencias,fecha,profesor["id_profesor"],horario["id_horario"],orden_dia):
        print("La asistencia ya fue registrada.")
        return
    nueva_asistencia = (crear_asistencia_profesor(asistencias,profesor,
            modulo,horario,dia_horario,fecha,hora_entrada,hora_salida))
    asistencias.append(nueva_asistencia)
    guardar_json(RUTA_ASISTENCIAS,asistencias)
    print("\nAsistencia registrada correctamente.")