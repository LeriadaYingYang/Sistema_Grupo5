from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASIGNACIONES = "datos/horarios_profesores.json"

def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_profesores(profesores):
    imprimir_titulo("PROFESORES DISPONIBLES")
    encontrados = 0
    for profesor in profesores:
        if profesor["estado"] == "Activo":
            encontrados += 1
            print(
                f"ID: {profesor['id_profesor']} | "
                f"{profesor['nombres']} {profesor['apellidos']}"
            )
    if encontrados == 0:
        print("No existen profesores activos.")

def mostrar_horarios(horarios):
    imprimir_titulo("HORARIOS DISPONIBLES")
    encontrados = 0
    for horario in horarios:
        if horario["estado"] == "Activo":
            encontrados += 1
            print(
                f"ID Horario: {horario['id_horario']} | "
                f"Plantilla: {horario['nombre_plantilla']} | "
                f"Carrera: {horario['nombre_carrera']} | "
                f"Salón: {horario['nombre_salon']} | "
                f"Turno: {horario['turno']}"
            )
    if encontrados == 0:
        print("No existen horarios registrados.")

def asignacion_ya_existe(asignaciones, id_profesor, id_horario):
    for asignacion in asignaciones:
        if (asignacion["estado"] == "Activo" and asignacion["id_profesor"] == id_profesor and asignacion["id_horario"] == id_horario):
            return True
    return False

def asignar_horarios_profesores():
    imprimir_titulo("ASIGNAR HORARIOS A PROFESORES")
    profesores = leer_json(RUTA_PROFESORES)
    horarios = leer_json(RUTA_HORARIOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    if len(profesores) == 0:
        print("No existen profesores registrados.")
        return
    if len(horarios) == 0:
        print("No existen horarios registrados.")
        return
    mostrar_profesores(profesores)
    try:
        id_profesor = int(input("\nIngrese ID del profesor: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    profesor = buscar_por_id(profesores,"id_profesor",id_profesor)
    if profesor is None:
        print("Profesor no encontrado.")
        return
    mostrar_horarios(horarios)
    try:
        id_horario = int(input("\nIngrese ID del horario: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    horario = buscar_por_id(horarios,"id_horario",id_horario)
    if horario is None:
        print("Horario no encontrado.")
        return
    if asignacion_ya_existe(asignaciones,id_profesor,id_horario):
        print("Este profesor ya tiene asignado ese horario.")
        return
    nueva_asignacion = {
        "id_asignacion_horario": generar_id(asignaciones,"id_asignacion_horario"),
        "id_profesor": profesor["id_profesor"],
        "nombre_profesor":profesor["nombres"] + " " +profesor["apellidos"],
        "id_horario": horario["id_horario"],
        "id_plantilla": horario["id_plantilla"],
        "nombre_plantilla": horario["nombre_plantilla"],
        "id_carrera": horario["id_carrera"],
        "nombre_carrera": horario["nombre_carrera"],
        "id_salon": horario["id_salon"],
        "nombre_salon": horario["nombre_salon"],
        "turno": horario["turno"],
        "estado": "Activo"
    }
    asignaciones.append(nueva_asignacion)
    guardar_json(RUTA_ASIGNACIONES,asignaciones)
    print("\nHorario asignado correctamente.")