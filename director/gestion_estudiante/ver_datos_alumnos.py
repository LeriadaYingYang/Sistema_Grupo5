from basedatos_json import leer_json
from director.utilidades import imprimir_titulo, pedir_entero, pausa

RUTA_ALUMNOS      = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"


def _obtener_asignacion(id_alumno, asignaciones):  # Busca la asignación activa del alumno para mostrar su carrera y salón
    return next(
        (a for a in asignaciones
         if a["id_alumno"] == id_alumno and a["estado"] == "Activo"),
        None
    )

def _mostrar_alumno(alumno, asignacion):  # Imprime los datos del alumno y, si existe, su asignación actual
    print("\n-----------------------------")
    print(f"ID      : {alumno['id_alumno']}")
    print(f"Nombre  : {alumno['nombres']} {alumno['apellidos']}")
    print(f"DNI     : {alumno['dni']}")
    print(f"Correo  : {alumno['correo']}")
    print(f"Celular : {alumno['celular']}")
    if asignacion:
        print(f"Carrera : {asignacion['nombre_carrera']}")
        print(f"Salón   : {asignacion['nombre_salon']}")
        print(f"Turno   : {asignacion['turno']}")
    else:
        print("Carrera : No asignada")
        print("Salón   : No asignado")

def _alumnos_activos(alumnos):  # Devuelve únicamente los alumnos que siguen activos
    return (a for a in alumnos if a["estado"] == "Activo")

def _mostrar_alumnos(lista, alumnos, asignaciones, mensaje_vacio):  # Recorre la lista y muestra cada alumno con su asignación
    encontrados = 0
    for alumno in lista:
        _mostrar_alumno(alumno, _obtener_asignacion(alumno["id_alumno"], asignaciones))
        encontrados += 1
    if encontrados == 0:
        print(mensaje_vacio)

# Opciones del menú principal.

def _ver_todos(alumnos, asignaciones):  # Lista todos los alumnos activos con los datos de su asignación actual
    _mostrar_alumnos(
        _alumnos_activos(alumnos), alumnos, asignaciones,
        "No hay alumnos activos registrados."
    )
    pausa()

def _ver_por_carrera_y_salon(alumnos, asignaciones):  # Filtra alumnos primero por carrera y luego por salón
    # Se arma un catálogo de carreras con alumnos activos para que el usuario elija.
    carreras_vistas = {}
    for a in asignaciones:
        if a["estado"] == "Activo":
            carreras_vistas.setdefault(a["id_carrera"], a["nombre_carrera"])

    if not carreras_vistas:
        print("No hay alumnos asignados a carreras.")
        return

    imprimir_titulo("CARRERAS CON ALUMNOS")
    for id_c, nombre_c in carreras_vistas.items():
        print(f"ID: {id_c} | Carrera: {nombre_c}")

    # La carrera seleccionada define qué salones se mostrarán después.
    id_carrera = pedir_entero("\nIngrese ID de carrera: ")
    if id_carrera is None or id_carrera not in carreras_vistas:
        print("Carrera no encontrada.")
        return

    # Ahora se listan solo los salones que pertenecen a esa carrera.
    salones_vistos = {}
    for a in asignaciones:
        if a["estado"] == "Activo" and a["id_carrera"] == id_carrera:
            salones_vistos.setdefault(
                a["id_salon"],
                {"nombre_salon": a["nombre_salon"], "turno": a["turno"]}
            )

    if not salones_vistos:
        print("No hay salones con alumnos para esa carrera.")
        return

    print("\n--- SALONES DE LA CARRERA ---")
    for id_s, datos in salones_vistos.items():
        print(f"ID: {id_s} | Salón: {datos['nombre_salon']} | Turno: {datos['turno']}")

    # Con el salón elegido se filtra a los alumnos exactos que coinciden.
    id_salon = pedir_entero("\nIngrese ID de salón: ")
    if id_salon is None:
        return

    imprimir_titulo("ALUMNOS DEL SALÓN")
    filtrados = [
        alumno for alumno in _alumnos_activos(alumnos)
        if (asig := _obtener_asignacion(alumno["id_alumno"], asignaciones))
        and asig["id_carrera"] == id_carrera
        and asig["id_salon"] == id_salon
    ]
    _mostrar_alumnos(filtrados, alumnos, asignaciones, "No hay alumnos en ese salón.")
    pausa()

def _buscar_por_nombre(alumnos, asignaciones):  # Busca alumnos activos por coincidencia parcial de nombre o apellido
    texto = input("Ingrese nombre o apellido a buscar: ").strip().lower()
    filtrados = [
        a for a in _alumnos_activos(alumnos)
        if texto in f"{a['nombres']} {a['apellidos']}".lower()
    ]
    _mostrar_alumnos(filtrados, alumnos, asignaciones, "No se encontraron alumnos con ese nombre.")
    pausa()

def _buscar_por_dni(alumnos, asignaciones):  # Busca un alumno activo usando su DNI exacto
    dni = input("Ingrese DNI del alumno: ").strip()
    filtrados = [a for a in _alumnos_activos(alumnos) if a["dni"] == dni]
    _mostrar_alumnos(filtrados, alumnos, asignaciones, "No se encontró un alumno con ese DNI.")
    pausa()

# Menú principal.

_OPCIONES = {
    "1": ("Ver todos los alumnos",          _ver_todos),
    "2": ("Ver alumnos por carrera y salón", _ver_por_carrera_y_salon),
    "3": ("Buscar alumno por nombre",        _buscar_por_nombre),
    "4": ("Buscar alumno por DNI",           _buscar_por_dni),
}

def menu_ver_datos_alumnos():  # Muestra el menú de consulta y ejecuta la opción seleccionada
    while True:
        # Se recargan los datos en cada vuelta para mostrar siempre la información más reciente.
        alumnos      = leer_json(RUTA_ALUMNOS)
        asignaciones = leer_json(RUTA_ASIGNACIONES)

        imprimir_titulo("VER DATOS DE ALUMNOS")
        for clave, (etiqueta, _) in _OPCIONES.items():
            print(f"{clave}. {etiqueta}")
        print("5. Volver al menú director")

        # El usuario decide cómo quiere consultar los registros.
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "5":
            print("\nVolviendo al menú director")
            break
        elif opcion in _OPCIONES:
            _OPCIONES[opcion][1](alumnos, asignaciones)
        else:
            print("Opción inválida.")
