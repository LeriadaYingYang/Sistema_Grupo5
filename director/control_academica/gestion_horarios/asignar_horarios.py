from basedatos_json import leer_json,guardar_json,generar_id
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASIGNACIONES = "datos/horarios_profesores.json"


def cargar_datos(ruta):
    try:
        datos = leer_json(ruta)
        if not isinstance(datos, list):
            return []
        return datos
    except Exception as e:
        print(f"Error al leer datos: {e}")
        return []


def validar_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor <= 0:
                print("Debe ingresar un número mayor a cero.")
                continue
            return valor
        except ValueError:
            print("Debe ingresar un número válido.")


def buscar_por_id(lista,campo_id,valor_id):
    if not isinstance(lista, list):
        return None
    for item in lista:
        if (item.get(campo_id) == valor_id
            and item.get("estado") == "Activo"):
            return item
    return None


def mostrar_profesores(profesores):
    imprimir_titulo("PROFESORES DISPONIBLES")
    encontrados = 0
    for profesor in profesores:
        if profesor.get("estado") == "Activo":
            encontrados += 1
            print(f"ID: "
                f"{profesor.get('id_profesor','N/A')} | "
                f"{profesor.get('nombres','')} "
                f"{profesor.get('apellidos','')}")
    if encontrados == 0:
        print("No existen profesores activos.")


def mostrar_horarios(horarios):
    imprimir_titulo("HORARIOS DISPONIBLES")
    encontrados = 0
    for horario in horarios:
        if horario.get("estado") == "Activo":
            encontrados += 1
            print(
                f"ID Horario: "
                f"{horario.get('id_horario','N/A')} | "
                f"Plantilla: "
                f"{horario.get('nombre_plantilla','N/A')} | "
                f"Carrera: "
                f"{horario.get('nombre_carrera','N/A')} | "
                f"Salón: "
                f"{horario.get('nombre_salon','N/A')} | "
                f"Turno: "
                f"{horario.get('turno','N/A')}"
            )
    if encontrados == 0:
        print("No existen horarios activos.")


def asignacion_ya_existe(asignaciones,id_profesor,id_horario):
    for asignacion in asignaciones:
        if (
            asignacion.get("estado") == "Activo"
            and asignacion.get("id_profesor") == id_profesor
            and asignacion.get("id_horario") == id_horario):
            return True
    return False


def asignar_horarios_profesores():
    imprimir_titulo("ASIGNAR HORARIOS A PROFESORES")
    profesores = cargar_datos(RUTA_PROFESORES)
    horarios = cargar_datos(RUTA_HORARIOS)
    asignaciones = cargar_datos(RUTA_ASIGNACIONES)
    profesores_activos = [
        p for p in profesores
        if p.get("estado") == "Activo"]
    horarios_activos = [
        h for h in horarios
        if h.get("estado") == "Activo"]
    if not profesores_activos:
        print("No existen profesores activos.")
        return
    if not horarios_activos:
        print("No existen horarios activos.")
        return
    mostrar_profesores(profesores_activos)
    id_profesor = validar_entero("\nIngrese ID del profesor: ")
    profesor = buscar_por_id(profesores,"id_profesor",id_profesor)
    if profesor is None:
        print("Profesor no encontrado o inactivo.")
        return
    mostrar_horarios(horarios_activos)
    id_horario = validar_entero("\nIngrese ID del horario: ")
    horario = buscar_por_id(horarios,"id_horario",id_horario)
    if horario is None:
        print("Horario no encontrado o inactivo.")
        return
    if asignacion_ya_existe(asignaciones,id_profesor,id_horario):
        print("Este profesor ya tiene asignado ese horario.")
        return
    try:
        nueva_asignacion = {
            "id_asignacion_horario":
                generar_id(asignaciones,"id_asignacion_horario"),
            "id_profesor":
                profesor.get("id_profesor"),
            "nombre_profesor":
                f"{profesor.get('nombres','')} "
                f"{profesor.get('apellidos','')}",
            "id_horario":horario.get("id_horario"),
            "id_plantilla":horario.get("id_plantilla"),
            "nombre_plantilla":horario.get("nombre_plantilla"),
            "id_carrera":horario.get("id_carrera"),
            "nombre_carrera":horario.get("nombre_carrera"),
            "id_salon":horario.get("id_salon"),
            "nombre_salon":horario.get("nombre_salon"),
            "turno":horario.get("turno"),
            "estado":"Activo"}
        asignaciones.append(nueva_asignacion)
        guardar_json(RUTA_ASIGNACIONES,asignaciones)
        print("\nHorario asignado correctamente.")
    except Exception as e:
        print(f"Error al guardar "
            f"la asignación: {e}")