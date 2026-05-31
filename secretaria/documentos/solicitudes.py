from basedatos_json import (leer_json,guardar_json,generar_id)
from secretaria.utilidades import (imprimir_titulo)

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_SOLICITUDES = "datos/solicitudes.json"

def mostrar_alumnos(alumnos):
    imprimir_titulo("=== ALUMNOS DISPONIBLES ===")
    encontrados = 0
    for alumno in alumnos:
        if alumno["estado"] == "Activo":
            print(f"ID: {alumno['id_alumno']} | "
                f"{alumno['nombres']} "
                f"{alumno['apellidos']} | "
                f"DNI: {alumno['dni']}")
            encontrados += 1
    if encontrados == 0:
        print("No hay alumnos activos.")

def buscar_alumno(alumnos,id_alumno):
    for alumno in alumnos:
        if (alumno["id_alumno"] == id_alumno and alumno["estado"] == "Activo"):
            return alumno
    return None

def obtener_asignacion(id_alumno,asignaciones):
    for asignacion in asignaciones:
        if (asignacion["id_alumno"] == id_alumno and asignacion["estado"] == "Activo"):
            return asignacion
    return None

def buscar_solicitud(solicitudes,id_solicitud):
    for solicitud in solicitudes:
        if (solicitud["id_solicitud"]== id_solicitud):
            return solicitud
    return None

def mostrar_solicitudes():
    imprimir_titulo("=== LISTA DE SOLICITUDES ===")
    solicitudes = leer_json(RUTA_SOLICITUDES)
    if len(solicitudes) == 0:
        print("No existen solicitudes.")
        return
    for solicitud in solicitudes:
        print(f"ID: "f"{solicitud['id_solicitud']} | "f"Alumno: "
            f"{solicitud['nombre_alumno']} | "f"Tipo: "
            f"{solicitud['tipo_solicitud']} | "
            f"Estado: "f"{solicitud['estado']}")

def mostrar_solicitudes_pendientes():
    imprimir_titulo("=== SOLICITUDES PENDIENTES ===")
    solicitudes = leer_json(RUTA_SOLICITUDES)
    encontrados = 0
    for solicitud in solicitudes:
        if solicitud["estado"] == "Pendiente":
            print(f"ID: "
                f"{solicitud['id_solicitud']} | "
                f"{solicitud['nombre_alumno']} | "
                f"{solicitud['tipo_solicitud']}")
            encontrados += 1
    if encontrados == 0:
        print("No existen pendientes.")

def registrar_solicitud():
    imprimir_titulo("=== REGISTRAR SOLICITUD ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    solicitudes = leer_json(RUTA_SOLICITUDES)
    if len(alumnos) == 0:
        print("No hay alumnos registrados.")
        return
    mostrar_alumnos(alumnos)

#Controlando errores al ingresar ID de alumno
    try:
        id_alumno = int(input("\nIngresar ID del alumno: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno = buscar_alumno(alumnos,id_alumno)
    if alumno is None:
        print("Alumno no encontrado.")
        return
    asignacion = obtener_asignacion(id_alumno,asignaciones)
    if asignacion is None:
        print("El alumno no tiene asignación activa.")
        return
    print("""

=== TIPOS DE SOLICITUD ===

1. Cambio de salón
2. Cambio de turno
3. Retiro
4. Reincorporación
5. Documento académico

""")
    opcion = input("Seleccionar opción: ")
    tipos = {
        "1": "Cambio de salón",
        "2": "Cambio de turno",
        "3": "Retiro",
        "4": "Reincorporación",
        "5": "Documento académico"
    }
    if opcion not in tipos:
        print("Opción inválida.")
        return
    descripcion = input("Descripción de la solicitud: ")
    nueva_solicitud = {
        "id_solicitud":generar_id(solicitudes,"id_solicitud"),
        "id_alumno":alumno["id_alumno"],
        "nombre_alumno":f"{alumno['nombres']} "f"{alumno['apellidos']}",
        "dni":alumno["dni"],
        "tipo_solicitud":tipos[opcion],
        "descripcion":descripcion,
        "carrera":asignacion["nombre_carrera"],
        "salon":asignacion["nombre_salon"],
        "estado":"Pendiente"
    }
    solicitudes.append(nueva_solicitud)
    guardar_json(RUTA_SOLICITUDES,solicitudes)
    imprimir_titulo("=== SOLICITUD REGISTRADA ===")
    print(f"Solicitud ID: "f"{nueva_solicitud['id_solicitud']}")
    print(f"Alumno: "f"{nueva_solicitud['nombre_alumno']}")
    print(f"Estado: "f"{nueva_solicitud['estado']}")

def actualizar_estado():
    imprimir_titulo("=== ACTUALIZAR ESTADO ===")
    solicitudes = leer_json(RUTA_SOLICITUDES)

#Controlando errores al ingresar ID de solicitud
    try:
        id_solicitud = int(input("Ingresar ID solicitud: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    solicitud = buscar_solicitud(solicitudes,id_solicitud)
    if solicitud is None:
        print("Solicitud no encontrada.")
        return
    print("""

1. Aprobada
2. Rechazada
3. Pendiente

""")
    opcion = input("Seleccionar estado: ")
    estados = {
        "1": "Aprobada",
        "2": "Rechazada",
        "3": "Pendiente"
    }
    if opcion not in estados:
        print("Opción inválida.")
        return
    solicitud["estado"] = estados[opcion]
    guardar_json(RUTA_SOLICITUDES,solicitudes)
    print("=== ESTADO ACTUALIZADO CORRECTAMENTE ===")

def buscar_solicitud_por_id():
    imprimir_titulo("=== BUSCAR SOLICITUD ===")
    solicitudes = leer_json(RUTA_SOLICITUDES)

#Controlando errores al ingresar ID de solicitud
    try:
        id_solicitud = int(input("Ingresar ID: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    solicitud = buscar_solicitud(solicitudes,id_solicitud)
    if solicitud is None:
        print("Solicitud no encontrada.")
        return
    imprimir_titulo("=== DATOS DE SOLICITUD ===")
    for clave, valor in solicitud.items():
        print(f"{clave}: {valor}")

def menu_solicitudes():
    while True:
        imprimir_titulo("=== MENU SOLICITUDES ===")
        print("1. Registrar solicitud")
        print("2. Mostrar solicitudes")
        print("3. Mostrar pendientes")
        print("4. Buscar solicitud")
        print("5. Actualizar estado")
        print("6. Volver")
        opcion = input("\nSeleccionar una opción: ")
        match opcion:
            case "1":registrar_solicitud()
            case "2":mostrar_solicitudes()
            case "3":mostrar_solicitudes_pendientes()
            case "4":buscar_solicitud_por_id()
            case "5":actualizar_estado()
            case "6":
                print("Regresando al menú de documentos...")
                break
            case _:
                print("Opción inválida.")

