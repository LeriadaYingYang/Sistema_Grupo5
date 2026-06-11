from basedatos_json import leer_json, guardar_json, generar_id
from gestion_academica.utilidades import imprimir_titulo

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"

def mostrar_alumnos_no_asignados(alumnos, asignaciones):  #muestra alumnos activos que aún no tienen asignación
    imprimir_titulo("ALUMNOS DISPONIBLES NO ASIGNADOS")
    encontrados = 0  #cuenta los alumnos disponibles
    for alumno in alumnos:
        if alumno["estado"] != "Activo":
            continue
        ya_asignado = False  #indica si el alumno ya tiene una asignación activa
        for asignacion in asignaciones:
            if (asignacion["id_alumno"] == alumno["id_alumno"]
                and asignacion["estado"] == "Activo"):
                ya_asignado = True
                break
        if not ya_asignado:
            encontrados += 1
            print(f"ID: {alumno['id_alumno']} | "
                f"{alumno['nombres']} {alumno['apellidos']} | DNI: {alumno['dni']}")
    if encontrados == 0:
        print("Todos los alumnos ya están asignados.")

def mostrar_plantillas(plantillas):  #muestra las plantillas activas disponibles
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    for p in plantillas:
        if p["estado"] == "Activo":
            print(f"ID: {p['id_plantilla']} | "
                f"{p['nombre_plantilla']} | "
                f"{p['nombre_carrera']}")

def mostrar_carreras(carreras):  #muestra las carreras activas disponibles
    imprimir_titulo("CARRERAS DISPONIBLES")
    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | Carrera: {carrera['nombre']}")

def mostrar_salones_por_carrera(salones, id_carrera):  #muestra los salones activos de una carrera
    imprimir_titulo("SALONES DISPONIBLES PARA ESTA CARRERA")
    hay_salones = False  #indica si existen salones para la carrera
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            hay_salones = True
            print(f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | Turno: {salon['turno']}")
    if not hay_salones:
        print("No hay salones registrados para esta carrera.")

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def alumno_ya_asignado(asignaciones, id_alumno):  #verifica si un alumno ya tiene asignación activa
    for asignacion in asignaciones:
        if (asignacion["id_alumno"] == id_alumno
            and asignacion["estado"] == "Activo"):
            return True
    return False

def asignar_alumno():  #asigna un alumno a una plantilla, carrera y salón
    imprimir_titulo("ASIGNAR ALUMNO A CARRERA Y SALÓN")
    alumnos = leer_json(RUTA_ALUMNOS)  #carga los alumnos registrados
    carreras = leer_json(RUTA_CARRERAS)  #carga las carreras registradas
    salones = leer_json(RUTA_SALONES)  #carga los salones registrados
    asignaciones = leer_json(RUTA_ASIGNACIONES)  #carga las asignaciones registradas
    plantillas = leer_json(RUTA_PLANTILLAS)  #carga las plantillas registradas
    if len(alumnos) == 0:
        print("Primero debe registrar alumnos.")
        return
    hay_disponibles = False  #indica si existen alumnos disponibles para asignar
    for alumno in alumnos:
        if alumno["estado"] != "Activo":
            continue
        if not alumno_ya_asignado(asignaciones, alumno["id_alumno"]):
            hay_disponibles = True
            break
    if not hay_disponibles:
        print("No hay alumnos disponibles para asignar.")
        return
    if len(plantillas) == 0:
        print("Primero debe registrar plantillas.")
        return
    if len(carreras) == 0:
        print("Primero debe registrar carreras.")
        return
    if len(salones) == 0:
        print("Primero debe registrar salones.")
        return
    mostrar_alumnos_no_asignados(alumnos, asignaciones)  #muestra alumnos sin asignación
    try:
        id_alumno = int(input("\nIngrese ID del alumno: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return
    alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)  #busca el alumno seleccionado
    if alumno is None:
        print("Alumno no encontrado.")
        return
    if alumno_ya_asignado(asignaciones, id_alumno):
        print("Este alumno ya tiene una asignación activa.")
        return
    mostrar_plantillas(plantillas)  #muestra plantillas disponibles
    try:
        id_plantilla = int(input("\nIngrese ID de la plantilla: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)  #busca la plantilla seleccionada
    if plantilla is None:
        print("Plantilla no encontrada.")
        return
    mostrar_carreras(carreras)  #muestra carreras disponibles
    try:
        id_carrera = int(input("\nIngrese ID de la carrera: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)  #busca la carrera seleccionada
    if carrera is None:
        print("Carrera no encontrada.")
        return
    if carrera["id_carrera"] != plantilla["id_carrera"]:
        print("Error: la carrera no coincide con la plantilla.")
        return
    mostrar_salones_por_carrera(salones, id_carrera)  #muestra salones de la carrera
    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return
    salon = buscar_por_id(salones, "id_salon", id_salon)  #busca el salón seleccionado
    if salon is None:
        print("Salón no encontrado.")
        return
    if salon["id_carrera"] != carrera["id_carrera"]:
        print("Error: el salón no pertenece a esa carrera.")
        return
    nueva_asignacion = {  #crea el registro de asignación del alumno
        "id_asignacion_alumno": generar_id(asignaciones, "id_asignacion_alumno"),
        "id_alumno": alumno["id_alumno"],
        "nombre_alumno": alumno["nombres"] + " " + alumno["apellidos"],
        "dni": alumno["dni"],
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"],
        "turno": salon["turno"],
        "estado": "Activo"}
    asignaciones.append(nueva_asignacion)  #agrega la asignación a la lista
    guardar_json(RUTA_ASIGNACIONES, asignaciones)  #guarda la asignación en el archivo json
    print("\nAlumno asignado correctamente.")
    print(f"Alumno: {nueva_asignacion['nombre_alumno']}")
    print(f"Plantilla: {nueva_asignacion['nombre_plantilla']}")
    print(f"Carrera: {nueva_asignacion['nombre_carrera']}")
    print(f"Salón: {nueva_asignacion['nombre_salon']}")