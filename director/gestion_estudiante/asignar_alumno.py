from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, pedir_entero, pausa

RUTA_ALUMNOS      = "datos/alumnos.json"
RUTA_CARRERAS     = "datos/carreras.json"
RUTA_SALONES      = "datos/salones.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_PLANTILLAS   = "datos/plantillas_academicas.json"


def _buscar_activo(lista, campo_id, valor_id):  # retorna el primer registro activo que coincida con el id dado
    return next(
        (item for item in lista
         if item[campo_id] == valor_id and item["estado"] == "Activo"),
        None
    )

def _alumno_ya_asignado(asignaciones, id_alumno):  # verifica si el alumno tiene una asignación activa
    return any(
        a["id_alumno"] == id_alumno and a["estado"] == "Activo"
        for a in asignaciones
    )

# funciones de visualización

def _mostrar_alumnos_no_asignados(alumnos, asignaciones):  # muestra alumnos activos sin asignación activa
    imprimir_titulo("ALUMNOS DISPONIBLES NO ASIGNADOS")
    encontrados = sum(
        1 for a in alumnos
        if a["estado"] == "Activo" and not _alumno_ya_asignado(asignaciones, a["id_alumno"])
        and not print(f"ID: {a['id_alumno']} | {a['nombres']} {a['apellidos']} | DNI: {a['dni']}")
    )
    if encontrados == 0:
        print("Todos los alumnos ya están asignados.")

def _mostrar_lista(titulo, items, campos):  # muestra una lista genérica con título y campos indicados
    imprimir_titulo(titulo)
    for item in items:
        if item["estado"] == "Activo":
            linea = " | ".join(f"{etiqueta}: {item[campo]}" for etiqueta, campo in campos)
            print(linea)

def _mostrar_salones_por_carrera(salones, id_carrera):  # muestra salones activos de una carrera específica
    imprimir_titulo("SALONES DISPONIBLES PARA ESTA CARRERA")
    disponibles = [
        s for s in salones
        if s["estado"] == "Activo" and s["id_carrera"] == id_carrera
    ]
    if not disponibles:
        print("No hay salones registrados para esta carrera.")
        return
    for s in disponibles:
        print(f"ID: {s['id_salon']} | Salón: {s['nombre_salon']} | Turno: {s['turno']}")

## Logica principal del alumno 
def asignar_alumno():  # asigna un alumno a una plantilla, carrera y salón
    print("--- ASIGNACIÓN DE ALUMNO ---")
    print("Seleccione el alumno, plantilla, carrera y salón para la asignación.\n")
    pausa()
    imprimir_titulo("ASIGNAR ALUMNO A CARRERA Y SALÓN")

    alumnos      = leer_json(RUTA_ALUMNOS)
    carreras     = leer_json(RUTA_CARRERAS)
    salones      = leer_json(RUTA_SALONES)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    plantillas   = leer_json(RUTA_PLANTILLAS)

    # validaciones previas
    checks = [
        (not alumnos,                                       "Primero debe registrar alumnos."),
        (not plantillas,                                    "Primero debe registrar plantillas."),
        (not carreras,                                      "Primero debe registrar carreras."),
        (not salones,                                       "Primero debe registrar salones."),
        (not any(
            a["estado"] == "Activo" and not _alumno_ya_asignado(asignaciones, a["id_alumno"])
            for a in alumnos
        ),                                                   "No hay alumnos disponibles para asignar."),
    ]
    for condicion, mensaje in checks:
        if condicion:
            print(mensaje)
            return

    # selección de alumno
    _mostrar_alumnos_no_asignados(alumnos, asignaciones)
    id_alumno = pedir_entero("\nIngrese ID del alumno: ")
    if id_alumno is None:
        return
    alumno = _buscar_activo(alumnos, "id_alumno", id_alumno)
    if alumno is None:
        print("Alumno no encontrado.")
        return
    if _alumno_ya_asignado(asignaciones, id_alumno):
        print("Este alumno ya tiene una asignación activa.")
        return

    # selección de plantilla
    _mostrar_lista("PLANTILLAS DISPONIBLES", plantillas,
                   [("ID", "id_plantilla"), ("Nombre", "nombre_plantilla"), ("Carrera", "nombre_carrera")])
    id_plantilla = pedir_entero("\nIngrese ID de la plantilla: ")
    if id_plantilla is None:
        return
    plantilla = _buscar_activo(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None:
        print("Plantilla no encontrada.")
        return

    # selección de carrera
    _mostrar_lista("CARRERAS DISPONIBLES", carreras,
                   [("ID", "id_carrera"), ("Carrera", "nombre")])
    id_carrera = pedir_entero("\nIngrese ID de la carrera: ")
    if id_carrera is None:
        return
    carrera = _buscar_activo(carreras, "id_carrera", id_carrera)
    if carrera is None:
        print("Carrera no encontrada.")
        return
    if carrera["id_carrera"] != plantilla["id_carrera"]:
        print("Error: la carrera no coincide con la plantilla seleccionada.")
        return

    # selección de salón
    _mostrar_salones_por_carrera(salones, id_carrera)
    id_salon = pedir_entero("\nIngrese ID del salón: ")
    if id_salon is None:
        return
    salon = _buscar_activo(salones, "id_salon", id_salon)
    if salon is None:
        print("Salón no encontrado.")
        return
    if salon["id_carrera"] != carrera["id_carrera"]:
        print("Error: el salón no pertenece a esa carrera.")
        return

    # crear y guardar asignación
    nueva_asignacion = {
        "id_asignacion_alumno": generar_id(asignaciones, "id_asignacion_alumno"),
        "id_alumno":      alumno["id_alumno"],
        "nombre_alumno":  f"{alumno['nombres']} {alumno['apellidos']}",
        "dni":            alumno["dni"],
        "id_plantilla":   plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera":     carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "id_salon":       salon["id_salon"],
        "nombre_salon":   salon["nombre_salon"],
        "turno":          salon["turno"],
        "estado":         "Activo",
    }
    asignaciones.append(nueva_asignacion)
    guardar_json(RUTA_ASIGNACIONES, asignaciones)

    print("\nAlumno asignado correctamente.")
    print(f"Alumno  : {nueva_asignacion['nombre_alumno']}")
    print(f"Plantilla: {nueva_asignacion['nombre_plantilla']}")
    print(f"Carrera : {nueva_asignacion['nombre_carrera']}")
    print(f"Salón   : {nueva_asignacion['nombre_salon']}")
    pausa()
