from basedatos_json import leer_json, guardar_json, generar_id
from gestion_academica.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CARGOS_EXTRAS = "datos/cargos_extras.json"

def buscar_por_id(lista, campo_id, valor_id):  # busca un registro activo utilizando su identificador
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_plantillas(plantillas):  # muestra las plantillas disponibles para asignar cargos extras
    imprimir_titulo("PLANTILLAS")

    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"{plantilla['nombre_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']}")

def mostrar_salones(salones, id_carrera):  #muestra los salones que pertenecen a la carrera seleccionada
    imprimir_titulo("SALONES")
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            print(
                f"ID: {salon['id_salon']} | "
                f"{salon['nombre_salon']} | "
                f"Turno: {salon['turno']}")

def mostrar_alumnos_salon(alumnos, asignaciones, id_salon):  # muestra los alumnos asignados al salón seleccionado
    imprimir_titulo("ALUMNOS DEL SALÓN")
    encontrados = 0
    for asignacion in asignaciones:
        if asignacion["estado"] == "Activo" and asignacion["id_salon"] == id_salon:
            alumno = buscar_por_id(
                alumnos,
                "id_alumno",
                asignacion["id_alumno"])
            if alumno:
                encontrados += 1
                print(
                    f"ID: {alumno['id_alumno']} | "
                    f"{alumno['nombres']} {alumno['apellidos']} | "
                    f"DNI: {alumno['dni']}")
    if encontrados == 0:
        print("No hay alumnos asignados a este salón.")

def pedir_monto():  #solicita y valida el monto del cargo extra
    try:
        return float(input("Monto del cargo extra: S/ "))
    except ValueError:
        print("Monto inválido.")
        return None

def crear_cargo_extra_carrera():  #crea un cargo extra que será aplicado a toda la carrera
    plantillas = leer_json(RUTA_PLANTILLAS)
    cargos = leer_json(RUTA_CARGOS_EXTRAS)
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
    nombre = input("Nombre del cargo extra: ")
    monto = pedir_monto()
    if monto is None:
        return
    nuevo = {
        "id_cargo_extra": generar_id(cargos, "id_cargo_extra"),
        "nombre": nombre,
        "monto": monto,
        "aplica_a": "Carrera",
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera": plantilla["id_carrera"],
        "nombre_carrera": plantilla["nombre_carrera"],
        "id_salon": None,
        "nombre_salon": None,
        "id_alumno": None,
        "nombre_alumno": None,
        "estado": "Activo"}
    cargos.append(nuevo)  #agrega el cargo extra a la lista de cargos registrados
    guardar_json(RUTA_CARGOS_EXTRAS, cargos)  #guarda el cargo extra en el archivo json
    print("\nCargo extra para carrera creado correctamente.")

def crear_cargo_extra_salon():  #crea un cargo extra para todos los alumnos de un salón
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    cargos = leer_json(RUTA_CARGOS_EXTRAS)
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
    nombre = input("Nombre del cargo extra: ")
    monto = pedir_monto()
    if monto is None:
        return
    nuevo = {
        "id_cargo_extra": generar_id(cargos, "id_cargo_extra"),
        "nombre": nombre,
        "monto": monto,
        "aplica_a": "Salón",
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera": plantilla["id_carrera"],
        "nombre_carrera": plantilla["nombre_carrera"],
        "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"],
        "turno": salon["turno"],
        "id_alumno": None,
        "nombre_alumno": None,
        "estado": "Activo"}
    cargos.append(nuevo)  #agrega el cargo extra para el salón seleccionado
    guardar_json(RUTA_CARGOS_EXTRAS, cargos)  #guarda el cargo extra en el archivo json
    print("\nCargo extra para salón creado correctamente.")

def crear_cargo_extra_alumno():  #crea un cargo extra para un alumno específico
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    cargos = leer_json(RUTA_CARGOS_EXTRAS)
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
    mostrar_alumnos_salon(alumnos, asignaciones, id_salon)
    try:
        id_alumno = int(input("\nIngrese ID del alumno: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)
    if alumno is None:
        print("Alumno no válido.")
        return
    nombre = input("Nombre del cargo extra: ")
    monto = pedir_monto()
    if monto is None:
        return
    nuevo = {
        "id_cargo_extra": generar_id(cargos, "id_cargo_extra"),
        "nombre": nombre,
        "monto": monto,
        "aplica_a": "Alumno",
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera": plantilla["id_carrera"],
        "nombre_carrera": plantilla["nombre_carrera"],
        "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"],
        "turno": salon["turno"],
        "id_alumno": alumno["id_alumno"],
        "nombre_alumno": alumno["nombres"] + " " + alumno["apellidos"],
        "estado": "Activo"}

    cargos.append(nuevo)  #agrega el cargo extra al alumno seleccionado
    guardar_json(RUTA_CARGOS_EXTRAS, cargos)  #guarda el cargo extra en el archivo json
    print("\nCargo extra para alumno creado correctamente.")

def menu_cargos_extras():  #muestra el menú para registrar cargos extras por carrera, salón o alumno
    while True:
        print("""
--- CARGOS EXTRAS ---
1. Cargo extra para toda una carrera
2. Cargo extra para un salón
3. Cargo extra para un alumno específico
4. Volver
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":  #registra un cargo extra para toda la carrera
            crear_cargo_extra_carrera()
        elif opcion == "2":  #registra un cargo extra para un salón completo
            crear_cargo_extra_salon()
        elif opcion == "3":  #registra un cargo extra para un alumno específico
            crear_cargo_extra_alumno()
        elif opcion == "4":  #vuelve al menú anterior
            break
        else:
            print("Opción inválida.")